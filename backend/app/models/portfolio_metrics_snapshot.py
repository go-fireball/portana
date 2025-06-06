from sqlalchemy import Column, Date, UUID, ForeignKey, Numeric, DateTime, func

from app.db import Base


class PortfolioMetricsSnapshot(Base):
    __tablename__ = "portfolio_metrics_snapshot"

    snapshot_date = Column(Date, primary_key=True)
    account_id = Column(UUID, ForeignKey("accounts.account_id"), primary_key=True)

    portfolio_value = Column(Numeric)
    benchmark_value = Column(Numeric)
    portfolio_daily_return = Column(Numeric)
    benchmark_daily_return = Column(Numeric)
    cash_balance = Column(Numeric)

    twr_to_date = Column(Numeric)
    rolling_return_7d = Column(Numeric)
    rolling_return_30d = Column(Numeric)
    sharpe_to_date = Column(Numeric)
    drawdown_to_date = Column(Numeric)

    created_at = Column(DateTime, default=func.now())
