# app/schemas/user_hub.py
from pydantic import BaseModel, EmailStr
from uuid import UUID
from datetime import datetime
from typing import Optional

class UserHubBase(BaseModel):
    name: str
    email: EmailStr
    category: str
    description: Optional[str] = None
    url: Optional[str] = None
    status: Optional[bool] = False  # Default to inactive

class UserHubCreate(UserHubBase):
    pass

class UserHubUpdate(UserHubBase):
    name: Optional[str] = None
    email: Optional[EmailStr] = None
    category: Optional[str] = None

class UserHubOut(UserHubBase):
    id: UUID
    created_at: datetime
    updated_at: Optional[datetime]

    class Config:
        orm_mode = True