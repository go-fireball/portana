import pandas as pd
from sqlalchemy.orm import Session
from sqlalchemy.sql import func

from app.db import SessionLocal
from app.models import TransactionType
from app.models.position_snapshots import PositionSnapshot
from app.models.transaction import Transaction

session: Session = SessionLocal()


def get_portfolio_series(account_id: str) -> pd.Series:
    result = (
        session.query(
            PositionSnapshot.as_of_date,
            func.sum(PositionSnapshot.total_value).label("total_value")
        )
        .filter(account_id=account_id)
        .group_by(PositionSnapshot.as_of_date)
        .order_by(PositionSnapshot.as_of_date)
        .all()
    )

    # Convert to pandas Series
    portfolio_series = pd.Series(
        {row.as_of_date: float(row.total_value) for row in result}
    )

    return portfolio_series


def get_cash_flows(account_id: str) -> pd.Series:
    result = (
        session.query(Transaction.date, Transaction.action, Transaction.quantity)
        .filter(account_id=account_id)
        .filter(symbol="CASH")
        .filter(Transaction.action.in_([TransactionType.BUY, TransactionType.SELL]))
        .order_by(Transaction.date)
        .all()
    )

    cash_flow_map = {}

    for row in result:
        qty = float(row.quantity)
        flow = qty if row.action == TransactionType.BUY else -qty
        cash_flow_map.setdefault(row.date, 0.0)
        cash_flow_map[row.date] += flow

    cash_flow_series = pd.Series(cash_flow_map).sort_index()
    return cash_flow_series


def compute_daily_returns(portfolio_series: pd.Series) -> pd.Series:
    return portfolio_series.pct_change().dropna()


def compute_max_drawdown(portfolio_series: pd.Series) -> float:
    cumulative_max = portfolio_series.cummax()
    drawdown = (portfolio_series - cumulative_max) / cumulative_max
    return drawdown.min()


def compute_sharpe_ratio(daily_returns: pd.Series, risk_free_rate=0.05) -> float:
    daily_rf = risk_free_rate / 252  # Convert annual to daily
    excess_returns = daily_returns - daily_rf
    return excess_returns.mean() / excess_returns.std()


def compute_twr(portfolio_series: pd.Series, cash_flows: pd.Series) -> float:
    dates = portfolio_series.index
    twr = 1.0
    prev_value = None

    for date in dates:
        value = portfolio_series[date]
        flow = cash_flows.get(date, 0.0)

        if prev_value is not None:
            # Calculate sub-period return
            r = (value - flow - prev_value) / prev_value
            twr *= (1 + r)

        prev_value = value

    return twr - 1


def compute_cagr(portfolio_series: pd.Series) -> float:
    start_value = portfolio_series.iloc[0]
    end_value = portfolio_series.iloc[-1]
    n_years = (portfolio_series.index[-1] - portfolio_series.index[0]).days / 365.25
    return (end_value / start_value) ** (1 / n_years) - 1
