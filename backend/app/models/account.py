import uuid

from sqlalchemy import Column, String, ForeignKey, DateTime, func
from sqlalchemy.dialects.postgresql import UUID

from app.db import Base


class Account(Base):
    __tablename__ = "accounts"

    account_id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    user_id = Column(UUID(as_uuid=True), ForeignKey("users.user_id"), nullable=False)
    brokerage = Column(String, nullable=False)
    account_number = Column(String, nullable=True)
    nickname = Column(String, nullable=True)
    created_at = Column(DateTime, default=func.now())

