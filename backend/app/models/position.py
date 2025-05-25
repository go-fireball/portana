import uuid

from sqlalchemy import Column, String, Numeric, Date, ForeignKey, Enum as SqlEnum
from sqlalchemy.dialects.postgresql import UUID

from app.db import Base
from app.models.transaction_type import TransactionType


class Position(Base):
    __tablename__ = "positions"

    position_id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    account_id = Column(UUID(as_uuid=True), ForeignKey("accounts.account_id"), nullable=False)
    symbol = Column(String, nullable=False)
    quantity = Column(Numeric, nullable=False)
    avg_cost = Column(Numeric, nullable=True)  # updated on each new buy/sell
    last_updated = Column(Date, nullable=False)  # when this snapshot was last recalculated
    action = Column(SqlEnum(TransactionType, native_enum=False), nullable=False)

    def __repr__(self):
        return f"<Position(account_id={self.account_id}, symbol={self.symbol}, quantity={self.quantity}, action={self.action})>"
