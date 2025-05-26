from sqlalchemy import Column, String, Date, Numeric, PrimaryKeyConstraint
from app.db import Base


class Price(Base):
    __tablename__ = "prices"

    symbol = Column(String, nullable=False)
    price_date = Column(Date, nullable=False)
    price = Column(Numeric, nullable=False)

    __table_args__ = (
        PrimaryKeyConstraint('symbol', 'price_date', name='pk_prices_symbol_date'),
    )
