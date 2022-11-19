from unittest import TestCase
from faker import Faker
from bson import ObjectId
from invoice import repositories
from mongomock import MongoClient


# Replacing the pymongo with the mongomock
repositories.MongoClient = MongoClient


class BaseTest(TestCase):

    def __init__(self, method_name):
        super().__init__(method_name)
        self.faker = Faker()

    @staticmethod
    def generate_object_id() -> ObjectId:
        return ObjectId()

    def generate_id(self) -> str:
        return str(self.generate_object_id())
