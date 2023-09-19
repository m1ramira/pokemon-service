from bson import ObjectId
from motor import motor_asyncio
from pydantic.json_schema import JsonSchemaValue
from pydantic_core import core_schema

from src.database.settings import settings

client = motor_asyncio.AsyncIOMotorClient(
    settings.MONGO_URI,
    serverSelectionTimeoutMS=10000,
)
db = client.pokemon_db


class PyObjectId(ObjectId):
    @classmethod
    def __get_validators__(cls):
        yield cls.validate

    @classmethod
    def validate(cls, v):
        if not ObjectId.is_valid(v):
            raise ValueError("Invalid object id.")
        return ObjectId(v)

    @classmethod
    def __get_pydantic_json_schema__(cls, _core_schema, handler) -> JsonSchemaValue:
        return handler(core_schema.str_schema())
