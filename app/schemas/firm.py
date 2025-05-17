from uuid import UUID

from pydantic import BaseModel


class FirmCreate(BaseModel):
    name: str


class FirmOut(BaseModel):
    id: UUID
    name: str
    created_by_user_id: UUID

    model_config = {"from_attributes": True}
