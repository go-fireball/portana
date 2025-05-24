import uuid

from sqlalchemy import Column, String, Numeric, Date, ForeignKey
from sqlalchemy.dialects.postgresql import UUID

from app.db import Base


class Position(Base):
    __tablename__ = "positions"

    position_id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    account_id = Column(UUID(as_uuid=True), ForeignKey("accounts.account_id"), nullable=False)
    symbol = Column(String, nullable=False)
    quantity = Column(Numeric, nullable=False)
    avg_cost = Column(Numeric, nullable=True)  # updated on each new buy/sell
    last_updated = Column(Date, nullable=False)  # when this snapshot was last recalculated
