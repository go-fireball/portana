import uuid

from sqlalchemy import Column, String, Numeric, Date, ForeignKey, Enum as SqlEnum
from sqlalchemy.dialects.postgresql import UUID

from app.db import Base
from app.models.transaction_type import TransactionType


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
    action = Column(SqlEnum(TransactionType, native_enum=False), nullable=False)

    def __repr__(self):
        return f"<PositionSnapshot(account_id={self.account_id}, symbol={self.symbol}, quantity={self.quantity}, action={self.action})>"
