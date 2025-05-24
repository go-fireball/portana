import uuid

from sqlalchemy import Column, String, Numeric, Date, ForeignKey
from sqlalchemy.dialects.postgresql import UUID

from app.db import Base


class PositionSnapshot(Base):
    __tablename__ = "position_snapshots"

    snapshot_id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    account_id = Column(UUID(as_uuid=True), ForeignKey("accounts.account_id"), nullable=False)
    symbol = Column(String, nullable=False)
    quantity = Column(Numeric, nullable=False)
    avg_cost = Column(Numeric, nullable=True)
    price = Column(Numeric, nullable=True)  # price on that date
    total_value = Column(Numeric, nullable=True)
    as_of_date = Column(Date, nullable=False)  # snapshot date
