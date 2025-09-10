from fastapi import APIRouter, HTTPException, Query
from typing import List
from app.schemas.product import ProductCreate, ProductResponse
from app.crud import product as product_crud
from app.utils.helpers import doc_to_product_response

router = APIRouter(prefix="/products", tags=["Products"])

@router.post("/", response_model=ProductResponse)
async def create_product(product: ProductCreate):
    created = await product_crud.create_product(product.dict())
    return doc_to_product_response(created)

@router.get("/", response_model=List[ProductResponse])
async def list_products(skip: int = 0, limit: int = 10, search: str = Query("", description="Search by product name")):
    products = await product_crud.list_products(skip=skip, limit=limit, search=search)
    return [doc_to_product_response(p) for p in products]
