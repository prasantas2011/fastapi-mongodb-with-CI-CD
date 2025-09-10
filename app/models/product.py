from typing import Optional
from pydantic import BaseModel, Field
from app.database import PyObjectId

class Product(BaseModel):
    id: Optional[PyObjectId] = Field(alias="_id")
    name: str
    description: str
    price: float
    stock: int

    class Config:
        populate_by_name = True
        arbitrary_types_allowed = True
        json_encoders = {PyObjectId: str}
