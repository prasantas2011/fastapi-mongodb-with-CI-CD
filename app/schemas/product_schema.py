from pydantic import BaseModel
from app.database import PyObjectId

class ProductSchema(BaseModel):
    name: str
    description: str
    price: float
    stock: int

    class Config:
        populate_by_name = True
        arbitrary_types_allowed = True
        json_encoders = {PyObjectId: str}
