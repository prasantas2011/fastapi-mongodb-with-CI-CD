from typing import Optional, List
from pydantic import BaseModel, Field,ConfigDict
from app.database import PyObjectId

class OrderItem(BaseModel):
    product_id: str
    quantity: int

class Order(BaseModel):
    id: Optional[PyObjectId] = Field(alias="_id")
    user_id: str
    items: List[OrderItem]
    total: float

    model_config = ConfigDict(
        populate_by_name=True,
        arbitrary_types_allowed=True,
        json_encoders={PyObjectId: str}
    )
