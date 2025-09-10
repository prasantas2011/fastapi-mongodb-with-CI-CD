from app.databasenew import db
from bson import ObjectId
from datetime import datetime
from fastapi import HTTPException

async def create_order(order_data: dict):
    order_data["user_id"] = ObjectId(order_data["user_id"])
    order_data["products"] = [{"product_id": ObjectId(p["product_id"]), "quantity": p["quantity"]} for p in order_data["products"]]
    order_data["status"] = "pending"
    order_data["created_at"] = datetime.utcnow()
    result = await db.orders.insert_one(order_data)
    order_data["_id"] = result.inserted_id
    return order_data

async def get_order(order_id: str):
    pipeline = [
        {"$match": {"_id": ObjectId(order_id)}},
        {"$lookup": {"from": "users", "localField": "user_id", "foreignField": "_id", "as": "user"}},
        {"$unwind": "$user"},
        {"$unwind": "$products"},
        {"$lookup": {"from": "products", "localField": "products.product_id", "foreignField": "_id", "as": "products.product_details"}},
        {"$unwind": "$products.product_details"},
        {"$group": {
            "_id": "$_id",
            "user": {"$first": "$user"},
            "created_at": {"$first": "$created_at"},
            "status": {"$first": "$status"},
            "products": {"$push": "$products"}
        }}
    ]
    order = await db.orders.aggregate(pipeline).to_list(length=1)
    return order[0] if order else None

async def list_orders(skip: int = 0, limit: int = 10, search: str = ""):
    pipeline = [
        {"$lookup": {"from": "users", "localField": "user_id", "foreignField": "_id", "as": "user"}},
        {"$unwind": "$user"},
        {"$unwind": "$products"},
        {"$lookup": {"from": "products", "localField": "products.product_id", "foreignField": "_id", "as": "products.product_details"}},
        {"$unwind": "$products.product_details"},
        {"$group": {
            "_id": "$_id",
            "user": {"$first": "$user"},
            "created_at": {"$first": "$created_at"},
            "status": {"$first": "$status"},
            "products": {"$push": "$products"}
        }},
        {"$sort": {"created_at": -1}},
        {"$skip": skip},
        {"$limit": limit}
    ]
    if search:
        pipeline.insert(0, {"$match": {"user.name": {"$regex": search, "$options": "i"}}})
    orders = await db.orders.aggregate(pipeline).to_list(length=limit)
    return orders

async def getEmailByID(user_id):
    result = await db.users.find_one({"_id": ObjectId(user_id)})
    if not result:
        raise HTTPException(status_code=404, detail="User not found")
    
    # convert for response
    user = {
        "id": str(result["_id"]),
        "email": result["email"],
        "name": result["name"]
    }
    return result["email"]

async def getProduct(product_id):
    result = await db.products.find_one({"_id": ObjectId(product_id)})
    if not result:
        raise HTTPException(status_code=404, detail="User not found")
    
    # convert for response
    user = {
        "id": str(result["_id"]),
        "name": result["name"],
        "price": result["price"]
    }
    return result["name"]