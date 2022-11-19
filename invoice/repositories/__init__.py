from pymongo import MongoClient
from invoice.logger import Logger
from logging import getLogger
from bson import ObjectId


class MongoConnection:

    _instance = None

    def __init__(self, db_config: dict):
        if MongoConnection._instance != None:
            raise Exception('This class is a singleton!')

        else:
            MongoConnection._instance = self.create_connection(db_config)

    @staticmethod 
    def get_instance(db_config: dict):

        if MongoConnection._instance == None:
            MongoConnection(db_config)

        return MongoConnection._instance

    @staticmethod 
    def create_connection(db_config: dict):
        return MongoClient(
            db_config.get('host', '127.0.0.1'),
            username=db_config.get('username'),
            password=db_config.get('password')
        )[db_config.get('db', 'invoice')]


class BaseRepository:

    def __init__(self):
        # Setup the logger
        self.logger = Logger(
            getLogger(__name__),
            dict(prefix=getattr(self, 'LOG_PREFIX', getattr(self, 'LOG_PREFIX', self.__class__.__name__)))
        )

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
        return ObjectId(identifier)
