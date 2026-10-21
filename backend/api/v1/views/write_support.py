"""Input validation shared by the write routes; no schema changes."""

import re

from flask import jsonify, request

from models import db


MAX_TEXT_BYTES = 65535
MAX_RESOURCE_ID = 2147483647


def api_error(message, status=400):
    return jsonify({"status": "error", "message": message}), status


def json_object(optional=False):
    if optional and not request.get_data(cache=True):
        return {}, None
    data = request.get_json(silent=True)
    if not isinstance(data, dict):
        return None, api_error("Corps JSON invalide.")
    return data, None


def required_text(data, field, *, max_length=None, text_column=False, trim=True):
    value = data.get(field)
    if not isinstance(value, str) or not value.strip():
        return None, api_error(f"{field} doit etre une chaine non vide.")
    value = value.strip() if trim else value
    if max_length is not None and len(value) > max_length:
        return None, api_error(f"{field} est trop long.")
    try:
        encoded = value.encode("utf-8")
    except UnicodeEncodeError:
        return None, api_error(f"{field} contient des caracteres invalides.")
    if text_column and len(encoded) > MAX_TEXT_BYTES:
        return None, api_error(f"{field} est trop long.")
    return value, None


def get_resource(model, identifier):
    if not 1 <= identifier <= MAX_RESOURCE_ID:
        return None
    return db.session.get(model, identifier)


def is_unique_conflict(error, *, mysql_keys, sqlite_columns):
    original = getattr(error, "orig", error)
    arguments = getattr(original, "args", ())

    if not arguments:
        return False

    if arguments[0] in (1062, "1062"):
        if len(arguments) < 2 or not isinstance(arguments[1], str):
            return False
        message = arguments[1]
        match = re.search(
            r"""\bfor\s+key\s+(?P<quote>['"`])(?P<key>[^'"`]+)(?P=quote)\s*$""",
            message,
            flags=re.IGNORECASE,
        )
        if match is None:
            return False
        key = match.group("key").rsplit(".", 1)[-1]
        return key in mysql_keys

    prefix = "UNIQUE constraint failed: "
    message = arguments[0]
    if isinstance(message, str) and message.startswith(prefix):
        columns = frozenset(
            part.strip() for part in message[len(prefix):].split(",")
        )
        return columns in sqlite_columns

    return False
