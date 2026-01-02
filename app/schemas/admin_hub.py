# app/schemas/admin_hub.py
from pydantic import BaseModel
from uuid import UUID
from datetime import datetime
from typing import Optional

class AdminHubBase(BaseModel):
    page_heading: Optional[str] = "Hub"
    page_subtext: Optional[str] = "Explore Categories of Interest"
    category: str
    description: Optional[str] = None
    image_url: Optional[str] = None

class AdminHubCreate(AdminHubBase):
    pass

class AdminHubUpdate(AdminHubBase):
    pass

class AdminHubOut(AdminHubBase):
    id: UUID
    created_at: datetime
    updated_at: Optional[datetime]

    class Config:
        orm_mode = True