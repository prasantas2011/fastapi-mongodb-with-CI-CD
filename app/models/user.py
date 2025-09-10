from typing import Optional
from pydantic import BaseModel, EmailStr, Field
from app.database import PyObjectId

class User(BaseModel):
    id: Optional[PyObjectId] = Field(alias="_id")
    email: EmailStr
    name: str
    password: str  # stored as hash

    class Config:
        populate_by_name = True
        arbitrary_types_allowed = True
        json_encoders = {PyObjectId: str}
