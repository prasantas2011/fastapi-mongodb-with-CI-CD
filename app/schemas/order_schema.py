from pydantic import BaseModel,ConfigDict
from typing import List
from app.database import PyObjectId

class OrderItem(BaseModel):
    product_id: str
    quantity: int

class OrderSchema(BaseModel):
    user_id: str
    items: List[OrderItem]
    total: float

    model_config = ConfigDict(
        populate_by_name=True,
        arbitrary_types_allowed=True,
        json_encoders={PyObjectId: str}
    )
