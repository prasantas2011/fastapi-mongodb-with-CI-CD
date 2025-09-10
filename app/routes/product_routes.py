from fastapi import APIRouter, HTTPException, Depends
from app.schemas.product_schema import ProductSchema
from app.database import db
from bson import ObjectId
from app.auth import get_current_user

router = APIRouter(prefix="/products", tags=["Products"])

@router.post("/", response_model=ProductSchema)
async def create_product(product: ProductSchema, user=Depends(get_current_user)):
    product_dict = product.dict(by_alias=True)
    product_dict.pop("id", None)
    result = await db["products"].insert_one(product_dict)
    product_dict["_id"] = result.inserted_id
    return product_dict

@router.get("/", response_model=list[ProductSchema])
async def list_products():
    return await db["products"].find().to_list(100)

@router.get("/{product_id}", response_model=ProductSchema)
async def get_product(product_id: str):
    product = await db["products"].find_one({"_id": ObjectId(product_id)})
    if not product:
        raise HTTPException(404, "Product not found")
    return product

@router.put("/{product_id}", response_model=ProductSchema)
async def update_product(product_id: str, product: ProductSchema, user=Depends(get_current_user)):
    update_data = {k: v for k, v in product.dict(by_alias=True).items() if v is not None}
    result = await db["products"].update_one({"_id": ObjectId(product_id)}, {"$set": update_data})
    if result.modified_count == 0:
        raise HTTPException(404, "Product not found")
    return await db["products"].find_one({"_id": ObjectId(product_id)})

@router.delete("/{product_id}")
async def delete_product(product_id: str, user=Depends(get_current_user)):
    result = await db["products"].delete_one({"_id": ObjectId(product_id)})
    if result.deleted_count == 0:
        raise HTTPException(404, "Product not found")
    return {"message": "Product deleted"}
