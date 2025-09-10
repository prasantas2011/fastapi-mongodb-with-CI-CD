from typing import Optional
from pydantic import BaseModel, EmailStr, Field,ConfigDict
from app.database import PyObjectId

class User(BaseModel):
    id: Optional[PyObjectId] = Field(alias="_id")
    email: EmailStr
    name: str
    password: str  # stored as hash

    model_config = ConfigDict(
        populate_by_name=True,
        arbitrary_types_allowed=True,
        json_encoders={PyObjectId: str}
    )
