"""database  setup for FastAPI project."""
from motor.motor_asyncio import AsyncIOMotorClient
from bson import ObjectId


MONGO_URL = "mongodb://localhost:27017"
client = AsyncIOMotorClient(MONGO_URL)
db = client["ecommerce_db"]

# Helper to handle ObjectId in FastAPI + Pydantic

class PyObjectId(ObjectId):
    """
    PyObjectId connection helper class.

    Provides methods to connect to the database and access collections.
    """
    @classmethod
    def __get_validators__(cls):
        """
        Pydantic __get_validators__ compatible method.
        generate class variable
        """
        yield cls.validate

    @classmethod
    def validate(cls, v):
        """
        Pydantic validate compatible method.
        Returns ObjectId
        """
        if not ObjectId.is_valid(v):
            raise ValueError("Invalid ObjectId")
        return ObjectId(v)

    @classmethod
    def __get_pydantic_json_schema__(cls):
        """
        Pydantic v2 compatible method.
        Returns OpenAPI/JSON Schema as a string type.
        """
        return {"type": "string"}
    