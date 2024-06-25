#!/usr/bin/python3
"""
Contains class BaseModel.
"""

from datetime import datetime
import models
from os import getenv
from sqlalchemy import Column, String, DateTime, create_engine
from sqlalchemy.ext.declarative import declarative_base
import uuid

time_format = "%Y-%m-%dT%H:%M:%S.%f"

Base = declarative_base() if models.storage_t == "db" else object


class BaseModel:
    """The BaseModel class from which future classes will be derived"""
    if models.storage_t == "db":
        id = Column(String(60), primary_key=True)
        created_at = Column(DateTime, default=datetime.utcnow)
        updated_at = Column(DateTime, default=datetime.utcnow)

    def __init__(self, *args, **kwargs):
        """Initialization of the base model"""
        self.id = kwargs.get("id", str(uuid.uuid4()))
        self.created_at = self._parse_datetime(
            kwargs.get("created_at", datetime.utcnow()))
        self.updated_at = self._parse_datetime(
            kwargs.get("updated_at", datetime.utcnow()))

        for key, value in kwargs.items():
            if key not in ("__class__", "id", "created_at", "updated_at"):
                setattr(self, key, value)

    @staticmethod
    def _parse_datetime(value):
        """Parse datetime from string if necessary"""
        return datetime.strptime(value, time_format) if isinstance(value, str) else value

    def __str__(self):
        """String representation of the BaseModel class"""
        return f"[{self.__class__.__name__}] ({self.id}) {self.__dict__}"

    def save(self):
        """Updates the attribute 'updated_at' with the current datetime"""
        self.updated_at = datetime.utcnow()
        models.storage.new(self)
        models.storage.save()

    def to_dict(self):
        """Returns a dictionary containing all keys/values of the instance"""
        instance_dict = self.__dict__.copy()
        instance_dict["created_at"] = self.created_at.strftime(time_format)
        instance_dict["updated_at"] = self.updated_at.strftime(time_format)
        instance_dict["__class__"] = self.__class__.__name__
        instance_dict.pop("_sa_instance_state", None)
        return instance_dict

    def delete(self):
        """Delete the current instance from the storage"""
        models.storage.delete(self)
