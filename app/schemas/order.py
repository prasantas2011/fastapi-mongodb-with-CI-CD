from pydantic import BaseModel
from typing import List
from datetime import datetime
from .product import ProductResponse
from .user import UserResponse

class ProductItem(BaseModel):
    product_id: str
    quantity: int

class OrderCreate(BaseModel):
    user_id: str
    products: List[ProductItem]

class OrderProduct(BaseModel):
    product_id: str
    quantity: int
    product_details: ProductResponse

class OrderResponse(BaseModel):
    id: str
    user: UserResponse
    products: List[OrderProduct]
    status: str
    created_at: datetime
