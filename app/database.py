from motor.motor_asyncio import AsyncIOMotorClient
from bson import ObjectId


MONGO_URL = "mongodb://localhost:27017"
client = AsyncIOMotorClient(MONGO_URL)
db = client["ecommerce_db"]

# Helper to handle ObjectId in FastAPI + Pydantic

class PyObjectId(ObjectId):
    @classmethod
    def __get_validators__(cls):
        yield cls.validate

    @classmethod
    def validate(cls, v, info=None):
        if not ObjectId.is_valid(v):
            raise ValueError("Invalid ObjectId")
        return ObjectId(v)

    @classmethod
    def __get_pydantic_json_schema__(cls, core_schema, handler):
        """
        Pydantic v2 compatible method.
        Returns OpenAPI/JSON Schema as a string type.
        """
        return {"type": "string"}

