from fastapi import APIRouter, Depends, HTTPException
from app.schemas.order_schema import OrderSchema, OrderItem
from app.database import db
from bson import ObjectId
from app.auth import get_current_user

router = APIRouter(prefix="/orders", tags=["Orders"])

@router.post("/", response_model=OrderSchema)
async def create_order(order: OrderSchema, user=Depends(get_current_user)):
    # Calculate total
    total = 0
    for item in order.items:
        product = await db["products"].find_one({"_id": ObjectId(item.product_id)})
        if not product:
            raise HTTPException(404, f"Product {item.product_id} not found")
        if product["stock"] < item.quantity:
            raise HTTPException(400, f"Not enough stock for {product['name']}")
        total += product["price"] * item.quantity
        # Reduce stock
        await db["products"].update_one(
            {"_id": ObjectId(item.product_id)},
            {"$inc": {"stock": -item.quantity}}
        )

    order_dict = order.dict(by_alias=True)
    order_dict.pop("id", None)
    order_dict["user_id"] = str(user["_id"])
    order_dict["total"] = total
    result = await db["orders"].insert_one(order_dict)
    order_dict["_id"] = result.inserted_id
    return order_dict

@router.get("/", response_model=list[OrderSchema])
async def list_orders(user=Depends(get_current_user)):
    return await db["orders"].find({"user_id": str(user["_id"])}).to_list(100)
