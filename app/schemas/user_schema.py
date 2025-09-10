from pydantic import BaseModel, EmailStr
from app.database import PyObjectId

class UserSchema(BaseModel):
    email: EmailStr
    name: str
    password: str

    class Config:
        populate_by_name = True
        arbitrary_types_allowed = True
        json_encoders = {PyObjectId: str}
