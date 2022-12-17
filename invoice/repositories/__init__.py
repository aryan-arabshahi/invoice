from typing import Any
from pymongo import MongoClient
from invoice import config
from invoice.logger import Logger
from logging import getLogger
from bson import ObjectId
from invoice.utils import env


class MongoClientSingleton:

    _instance = None

    def __init__(self):
        if MongoClientSingleton._instance is not None:
            raise Exception('This class is a singleton!')

        else:
            MongoClientSingleton._instance = self.create_connection()

    @staticmethod 
    def get_instance():

        if MongoClientSingleton._instance is None:
            MongoClientSingleton()

        return MongoClientSingleton._instance

    @staticmethod 
    def create_connection():
        return MongoClient(
            env('MONGODB_HOST') or config.get('mongodb.host'),
            username=env('MONGODB_USERNAME') or config.get('mongodb.username'),
            password=env('MONGODB_PASSWORD') or config.get('mongodb.password')
        )


class BaseRepository:

    def __init__(self):
        # Setup the logger
        self.logger = Logger(
            getLogger(__name__),
            dict(prefix=getattr(self, 'LOG_PREFIX', getattr(self, 'LOG_PREFIX', self.__class__.__name__)))
        )

        self._client = self.get_client()
        self.collection = self.get_collection()

    @staticmethod
    def get_client() -> MongoClient:
        """Get the DB client

        Returns:
            MongoClient
        """
        db_name = env('MONGODB_DATABASE') or config.get('mongodb.db')
        return MongoClientSingleton.get_instance()[db_name]

    def get_collection(self, collection_name: str = None) -> Any:
        """Get the collection

        Keyword Arguments:
            collection_name (str) -- The collection name (default None)

        Returns:
            Any
        """
        if not collection_name and hasattr(self, 'COLLECTION'):
            collection_name = getattr(self, 'COLLECTION')

        return self._client[collection_name] if collection_name else None

    @staticmethod
    def normalize_primary_key(data: dict) -> dict:
        """Normalize the primary key for the dataclasses

        Change the _id to id

        Arguments:
            data {dict}

        Returns:
            dict
        """
        if not data.get('id'):
            document_id = data.pop('_id', None)
            if document_id is not None:
                data['id'] = str(document_id)

        return data

    @staticmethod
    def str_to_object_id(identifier: str) -> ObjectId:
        """Convert the string to the object ID

        Arguments:
            identifier (str) -- The stringified ID.
        
        Returns:
            ObjectId
        """
        return ObjectId(identifier)
