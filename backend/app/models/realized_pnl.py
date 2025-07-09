import uuid

from sqlalchemy import Column, String, Date, Numeric, UniqueConstraint
from sqlalchemy import Enum as SqlEnum
from sqlalchemy import ForeignKey
from sqlalchemy.dialects.postgresql import UUID

from app.db import Base
from app.models import TransactionType


class RealizedPnL(Base):
    __tablename__ = "realized_pnl"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    account_id = Column(UUID(as_uuid=True), ForeignKey("accounts.account_id"), nullable=False)

    base_symbol = Column(String, nullable=False)  # e.g. AAPL
    option_symbol = Column(String, nullable=True)  # e.g. AAPL_2025-09-20_150.0_CALL or None for stocks
    date = Column(Date, nullable=False)

    realized_pnl = Column(Numeric, nullable=False)
    quantity_closed = Column(Numeric, nullable=False)
    cost_basis = Column(Numeric, nullable=True)
    proceeds = Column(Numeric, nullable=True)

    action = Column(SqlEnum(TransactionType, native_enum=False), nullable=False)
    instrument_type = Column(String, nullable=False)  # stock/option

    __table_args__ = (
        UniqueConstraint("account_id", "option_symbol", "date", name="uix_realized_pnl_contract"),
    )
