import enum
import uuid

from app.db.base import Base
from sqlalchemy import Boolean, Column, DateTime, Enum, ForeignKey, String
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.sql import func


class UserRole(str, enum.Enum):
    admin = "Admin"
    broker = "Broker"


class User(Base):
    __tablename__ = "users"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4, index=True)
    email = Column(String, unique=True, index=True, nullable=False)
    password_hash = Column(String, nullable=False)
    role = Column(Enum(UserRole), default=UserRole.broker)
    firm_id = Column(UUID(as_uuid=True), ForeignKey("firms.id", use_alter=True))
    is_email_verified = Column(Boolean, default=False)
    is_2fa_enabled = Column(Boolean, default=False)
    last_login_at = Column(DateTime(timezone=True))
    refresh_token = Column(String, nullable=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
