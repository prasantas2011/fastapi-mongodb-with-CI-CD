from app.databasenew import db
from bson import ObjectId

async def create_product(product: dict):
    result = await db.products.insert_one(product)
    product["_id"] = result.inserted_id
    return product

async def list_products(skip: int = 0, limit: int = 10, search: str = ""):
    query = {"name": {"$regex": search, "$options": "i"}} if search else {}
    cursor = db.products.find(query).skip(skip).limit(limit)
    return [p async for p in cursor]

async def update_stock(product_id: str, quantity: int):
    await db.products.update_one({"_id": ObjectId(product_id)}, {"$inc": {"stock": quantity}})
