from pydantic import BaseModel,EmailStr
from typing import Optional
from models.role import Role  # Импорт модели Role

class UserRegisterSchema(BaseModel):
    email: EmailStr
    password: str
    name: str
    role: Optional[str] = "user"

class UserLoginSchema(BaseModel):
    email: EmailStr
    password: str