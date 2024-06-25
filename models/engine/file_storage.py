#!/usr/bin/python3
"""
Defines the FileStorage class
"""

import json
from models.amenity import Amenity
from models.base_model import BaseModel
from models.city import City
from models.place import Place
from models.review import Review
from models.state import State
from models.user import User

# Dictionary mapping class names to their respective classes
classes = {
    "Amenity": Amenity,
    "BaseModel": BaseModel,
    "City": City,
    "Place": Place,
    "Review": Review,
    "State": State,
    "User": User
}


class FileStorage:
    """Serializes instances to a JSON file and deserializes back to instances"""

    __file_path = "file.json"  # Path to the JSON file
    __objects = {}  # Dictionary to store all objects by <class name>.id

    def all(self, cls=None):
        """Returns the dictionary __objects, optionally filtered by class"""
        if cls:
            return {key: value for key, value in self.__objects.items() if cls == value.__class__ or cls == value.__class__.__name__}
        return self.__objects

    def new(self, obj):
        """Sets in __objects the obj with key <obj class name>.id"""
        if obj:
            key = f"{obj.__class__.__name__}.{obj.id}"
            self.__objects[key] = obj

    def save(self):
        """Serializes __objects to the JSON file (path: __file_path)"""
        json_objects = {key: obj.to_dict()
                        for key, obj in self.__objects.items()}
        with open(self.__file_path, 'w') as f:
            json.dump(json_objects, f)

    def reload(self):
        """Deserializes the JSON file to __objects"""
        try:
            with open(self.__file_path, 'r') as f:
                jo = json.load(f)
            self.__objects = {key: classes[val["__class__"]](
                **val) for key, val in jo.items()}
        except Exception:
            pass

    def delete(self, obj=None):
        """Deletes obj from __objects if it’s inside"""
        if obj:
            key = f"{obj.__class__.__name__}.{obj.id}"
            self.__objects.pop(key, None)

    def close(self):
        """Call reload() method for deserializing the JSON file to objects"""
        self.reload()
