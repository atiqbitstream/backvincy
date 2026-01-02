# app/models/admin_hub.py
from sqlalchemy import Column, String, Text, DateTime
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.sql import func
import uuid

from app.db.base import Base

class AdminHub(Base):
    __tablename__ = "admin_hub"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    page_heading = Column(String(100), default="Hub", nullable=True)
    page_subtext = Column(Text, default="Explore Categories of Interest", nullable=True)
    category = Column(String(100), nullable=False)  # category title (e.g., Meditation)
    description = Column(Text, nullable=True)  # category description
    image_url = Column(String(255), nullable=True)  # optional image URL
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())