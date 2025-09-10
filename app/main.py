from fastapi import FastAPI
from app.routes import user_routes, product_routes, order_routes

app = FastAPI(title="E-Commerce API with FastAPI + MongoDB")

# Register routes
app.include_router(user_routes.router)
app.include_router(product_routes.router)
app.include_router(order_routes.router)

@app.get("/")
async def root():
    return {"message": "E-commerce FastAPI backend running"}
