from fastapi import APIRouter, HTTPException,BackgroundTasks
from app.schemas.user import UserCreate, UserResponse
from app.crud import user as user_crud
from app.utils.helpers import doc_to_user_response
from app.utils.auth import create_access_token
from app.utils.email import send_order_email

router = APIRouter(prefix="/users", tags=["Users"])

@router.post("/register", response_model=UserResponse)
async def register(user: UserCreate,background_tasks :BackgroundTasks):
    created_user = await user_crud.create_user(user.dict())
    background_tasks.add_task(send_order_email, user.email,'','','registration_route')
    return doc_to_user_response(created_user)

@router.post("/login")
async def login(email: str, password: str):
    user = await user_crud.authenticate_user(email, password)
    if not user:
        raise HTTPException(status_code=401, detail="Invalid credentials")
    token = create_access_token({"sub": str(user["_id"]), "role": user.get("role","user")})
    return {"access_token": token, "token_type": "bearer"}

@router.get("/", response_model=list[UserResponse])
async def list_users(skip: int = 0, limit: int = 10):
    users = await user_crud.list_users(skip, limit)
    return [doc_to_user_response(u) for u in users]
