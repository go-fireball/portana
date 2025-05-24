import uuid

from sqlalchemy import Column, String, Numeric, Date, ForeignKey, JSON, Enum as SqlEnum
from sqlalchemy.dialects.postgresql import UUID

from app.db import Base
from app.models.transaction_type import TransactionType


class Transaction(Base):
    __tablename__ = "transactions"

    transaction_id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    account_id = Column(UUID(as_uuid=True), ForeignKey("accounts.account_id"), nullable=False)
    symbol = Column(String, nullable=False)

    action = Column(SqlEnum(TransactionType, native_enum=False), nullable=False)
    instrument_type = Column(String, nullable=False)  # 'stock', 'option', etc.
    quantity = Column(Numeric, nullable=False)
    price = Column(Numeric, nullable=True)
    date = Column(Date, nullable=False)

    option_details = Column(JSON, nullable=True)
    journal_details = Column(JSON, nullable=True)
