import json
from api.models.user import User
from api.models.story import Story
from api.models.theory import Theory
from api.models.comment import Comment

classes = {"User": User, "Story": Story, "Theory": Theory, "Comment": Comment}

class FileStorage:
    """
    Handles JSON serialization and deserialization
    """
    __file_path = "file.json"
    __objects = {}

    def all(self, cls=None):
        """
        Return dictionary of objects
        """
        if cls:
            if isinstance(cls, str):
                cls = classes.get(cls)
            return {k: v for k, v in self.__objects.items() if isinstance(v, cls)}
        return self.__objects

    def new(self, obj):
        """
        Set object in __objects
        """
        if obj:
            key = f"{obj.__class__.__name__}.{obj.id}"
            self.__objects[key] = obj

    def save(self):
        """
        Serialize __objects to JSON file
        """
        json_objects = {}
        for key, val in self.__objects.items():
            json_objects[key] = val.to_dict()
        with open(self.__file_path, 'w') as f:
            json.dump(json_objects, f)

    def reload(self):
        """
        Deserialize JSON file to __objects
        """
        try:
            with open(self.__file_path, 'r') as f:
                jo = json.load(f)
            for key, val in jo.items():
                cls_name = val["__class__"]
                if cls_name in classes:
                    self.__objects[key] = classes[cls_name](**val)
        except FileNotFoundError:
            pass

    def delete(self, obj=None):
        """
        Delete object from __objects
        """
        if obj:
            key = f"{obj.__class__.__name__}.{obj.id}"
            if key in self.__objects:
                del self.__objects[key]

    def get(self, cls, id):
        """
        Retrieve one object by class and id
        """
        if isinstance(cls, str):
            cls = classes.get(cls)
        if cls and id:
            for obj in self.__objects.values():
                if isinstance(obj, cls) and obj.id == id:
                    return obj
        return None

