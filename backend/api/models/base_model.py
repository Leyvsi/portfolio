import uuid
from datetime import datetime
import api.storage

class BaseModel:
    """
    Base class for all models
    """
    def __init__(self, *args, **kwargs):
        """
        Initialize base model attributes
        """
        if kwargs:
            for key, value in kwargs.items():
                if key != "__class__":
                    if key in ["created_at", "updated_at"] and isinstance(value, str):
                        setattr(self, key, datetime.strptime(value, "%Y-%m-%dT%H:%M:%S.%f"))
                    else:
                        setattr(self, key, value)
            if "id" not in kwargs:
                self.id = str(uuid.uuid4())
            if "created_at" not in kwargs:
                self.created_at = datetime.utcnow()
            if "updated_at" not in kwargs:
                self.updated_at = datetime.utcnow()
        else:
            self.id = str(uuid.uuid4())
            self.created_at = datetime.utcnow()
            self.updated_at = datetime.utcnow()

    def save(self):
        """
        Update the updated_at timestamp and save to storage
        """
        self.updated_at = datetime.utcnow()
        api.storage.storage.new(self)
        api.storage.storage.save()

    def delete(self):
        """
        Delete the current instance from storage
        """
        api.storage.storage.delete(self)

    def to_dict(self):
        """
        Return a dictionary representation of the instance
        """
        new_dict = self.__dict__.copy()
        new_dict["__class__"] = self.__class__.__name__
        if isinstance(self.created_at, datetime):
            new_dict["created_at"] = self.created_at.isoformat()
        if isinstance(self.updated_at, datetime):
            new_dict["updated_at"] = self.updated_at.isoformat()
        return new_dict

