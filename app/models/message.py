import uuid
from sqlalchemy import Column, String, Boolean, DateTime, ForeignKey, Text
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.sql import func
from app.database import Base

class Message(Base):
    __tablename__ = "messages"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    from_user = Column(UUID(as_uuid=True), ForeignKey("users.id"), nullable=False)
    to_user = Column(UUID(as_uuid=True), ForeignKey("users.id"), nullable=False)
    subject = Column(String, nullable=False)
    body = Column(Text, nullable=False)
    is_read = Column(Boolean, default=False)
    is_trashed = Column(Boolean, default=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
