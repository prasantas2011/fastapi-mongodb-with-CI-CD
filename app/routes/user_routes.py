from fastapi import APIRouter, Depends, HTTPException
from fastapi.security import OAuth2PasswordRequestForm
from app.schemas.user_schema import UserSchema
from app.database import db
from app.auth import hash_password, authenticate_user, create_access_token, get_current_user
from datetime import timedelta

router = APIRouter(prefix="/users", tags=["Users"])

@router.post("/register")
async def register(user: UserSchema):
    user_dict = user.dict(by_alias=True)
    user_dict["password"] = hash_password(user.password)
    existing = await db["users"].find_one({"email": user.email})
    if existing:
        raise HTTPException(400, "Email already registered")
    result = await db["users"].insert_one(user_dict)
    return {"id": str(result.inserted_id), "email": user.email}

@router.post("/login")
async def login(form_data: OAuth2PasswordRequestForm = Depends()):
    user = await authenticate_user(form_data.username, form_data.password)
    if not user:
        raise HTTPException(401, "Invalid credentials")
    token = create_access_token(data={"sub": str(user["_id"])}, expires_delta=timedelta(minutes=30))
    return {"access_token": token, "token_type": "bearer"}

@router.get("/me")
async def me(current_user: dict = Depends(get_current_user)):
    return {"id": str(current_user["_id"]), "email": current_user["email"]}
