from pydantic import BaseModel
from typing import Optional
from datetime import datetime

class SnippetBase(BaseModel):
    title: str
    content: str
    is_private: Optional[bool] = True

class SnippetCreate(SnippetBase):
    pass

class SnippetUpdate(SnippetBase):
    pass

class SnippetResponse(SnippetBase):
    id: int
    created_at: datetime
    shared_url: Optional[str] = None

    class Config:
        orm_mode = True
