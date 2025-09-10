from pydantic import BaseModel
from typing import List
from app.database import PyObjectId

class OrderItem(BaseModel):
    product_id: str
    quantity: int

class OrderSchema(BaseModel):
    user_id: str
    items: List[OrderItem]
    total: float

    class Config:
        populate_by_name = True
        arbitrary_types_allowed = True
        json_encoders = {PyObjectId: str}
