from uuid import UUID

from pydantic import BaseModel, EmailStr


class InviteCreate(BaseModel):
    email: EmailStr
    firm_id: UUID


class InviteOut(BaseModel):
    email: EmailStr
    firm_id: UUID
    invite_token: str

    model_config = {"from_attributes": True}
