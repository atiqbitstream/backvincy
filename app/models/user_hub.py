# app/models/user_hub.py
from sqlalchemy import Column, String, Text, Boolean, DateTime
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.sql import func
import uuid

from app.db.base import Base

class UserHub(Base):
    __tablename__ = "user_hub"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    name = Column(String(100), nullable=False)
    email = Column(String(120), unique=True, index=True, nullable=False)
    category = Column(String(100), nullable=False)  # category title (e.g., Meditation)
    description = Column(Text, nullable=True)
    url = Column(String(255), nullable=True)  # e.g. profile link, social link, etc.
    status = Column(Boolean, default=False)  # Default to inactive, requires admin approval
    created_by = Column(String(100), nullable=True)  # Name of the logged-in user who created this
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())