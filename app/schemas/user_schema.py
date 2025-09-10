from pydantic import BaseModel, EmailStr,ConfigDict
from app.database import PyObjectId

class UserSchema(BaseModel):
    email: EmailStr
    name: str
    password: str

    model_config = ConfigDict(
        populate_by_name=True,
        arbitrary_types_allowed=True,
        json_encoders={PyObjectId: str}
    )
