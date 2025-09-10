from typing import Optional, List
from pydantic import BaseModel, Field
from app.database import PyObjectId

class OrderItem(BaseModel):
    product_id: str
    quantity: int

class Order(BaseModel):
    id: Optional[PyObjectId] = Field(alias="_id")
    user_id: str
    items: List[OrderItem]
    total: float

    class Config:
        populate_by_name = True
        arbitrary_types_allowed = True
        json_encoders = {PyObjectId: str}
