from app.databasenew import db
from passlib.context import CryptContext

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

async def create_user(user: dict):
    user['password'] = pwd_context.hash(user['password'])
    result = await db.users.insert_one(user)
    user["_id"] = result.inserted_id
    return user

async def authenticate_user(email: str, password: str):
    user = await db.users.find_one({"email": email})
    if not user: return None
    if not pwd_context.verify(password, user["password"]):
        return None
    return user

async def list_users(skip: int = 0, limit: int = 10):
    cursor = db.users.find().skip(skip).limit(limit)
    return [u async for u in cursor]
