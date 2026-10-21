"""Compatibility export of the application configured in backend/index.py."""

import os
import sys

backend_dir = os.path.abspath(
    os.path.join(os.path.dirname(__file__), "../../")
)

if backend_dir not in sys.path:
    sys.path.insert(0, backend_dir)

from index import app
