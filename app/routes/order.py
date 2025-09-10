from fastapi import APIRouter, HTTPException, Query,BackgroundTasks
from typing import List
from app.schemas.order import OrderCreate, OrderResponse
from app.crud import order as order_crud
from app.utils.helpers import doc_to_order_response
from app.utils.email import send_email_with_template


router = APIRouter(prefix="/orders", tags=["Orders"])

@router.post("/", response_model=OrderResponse)
async def create_order(order: OrderCreate, background_tasks : BackgroundTasks):
    created = await order_crud.create_order(order.dict())
    aggregated = await order_crud.get_order(str(created["_id"]))
    if not aggregated:
        raise HTTPException(status_code=404, detail="Order not found")
    
    # 2. Schedule email
    items = order.products
    first_product_id = items[0].product_id
    qty = items[0].quantity
    email_id = await order_crud.getEmailByID(order.user_id)
    product_name = await order_crud.getProduct(first_product_id)
    context = {
        "name": "John Doe",
        "items": [
            {"name": "Laptop", "quantity": 1, "price": 1000},
            {"name": "Mouse", "quantity": 2, "price": 50},
        ],
        "total": 1100,
    }
    attachment_path="files/sample.pdf"
    background_tasks.add_task(send_email_with_template, email_id, "Your Order Confirmation","order_confirmation.html",context,attachment_path)

    return doc_to_order_response(aggregated)

@router.get("/", response_model=List[OrderResponse])
async def list_orders(skip: int = 0, limit: int = 10, search: str = Query("", description="Search by user name")):
    orders = await order_crud.list_orders(skip=skip, limit=limit, search=search)
    return [doc_to_order_response(o) for o in orders]

@router.get("/{order_id}", response_model=OrderResponse)
async def get_order(order_id: str):
    order = await order_crud.get_order(order_id)
    if not order:
        raise HTTPException(status_code=404, detail="Order not found")
    return doc_to_order_response(order)
