from pydantic import BaseModel

class ProductCreate(BaseModel):
    name: str
    price: float
    description: str = ""
    stock: int = 0

class ProductResponse(BaseModel):
    id: str
    name: str
    price: float
    description: str
    stock: int
