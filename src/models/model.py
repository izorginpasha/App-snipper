from pydantic import BaseModel, EmailStr
from typing import Optional
from .base import Base
from sqlalchemy import ForeignKey, String, Column, Integer
from sqlalchemy.orm import relationship
from .role import Role


class MyGetFuncResponseSchema(BaseModel):
    app_name: str
    number_of_months: int
    pi: float


class User(Base):
    __tablename__ = "user"
    id = Column(Integer, autoincrement=True, primary_key=True, index=True)
    name = Column(String(256), unique=True, nullable=False)
    email = Column(String(128), unique=True, index=True, nullable=False)
    hashed_password = Column(String(1024), nullable=False)
    salt = Column(String(1024), nullable=False, unique=True, index=True)
    role_id = Column(Integer, ForeignKey('role.id'))
    role = relationship("Role", back_populates="users")

class UserResponse(BaseModel):
    id: int
    name: str
    email: str
    role: Optional[str]  # Если роль нужна в ответе и это строка.

    class Config:
        from_attributes = True # Включаем поддержку SQLAlchemy объектов