from enum import Enum
from uuid import UUID

from pydantic import BaseModel, EmailStr


class UserRole(str, Enum):
    admin = "Admin"
    broker = "Broker"


class UserCreate(BaseModel):
    email: EmailStr
    password: str
    role: UserRole = UserRole.broker
    invite_token: str


class UserOut(BaseModel):
    id: UUID
    email: EmailStr
    role: UserRole

    model_config = {"from_attributes": True}
