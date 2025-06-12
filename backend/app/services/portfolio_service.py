from datetime import timedelta, date
from uuid import UUID

import numpy as np
import pandas as pd
from sqlalchemy.orm import Session, InstrumentedAttribute
from sqlalchemy.sql import func

from app.db import SessionLocal
from app.models import TransactionType, PortfolioMetricsSnapshot, User, Account
from app.models.position_snapshots import PositionSnapshot
from app.models.transaction import Transaction

session: Session = SessionLocal()


def get_portfolio_series(account_id: str, from_date: date) -> pd.Series:
    """
    Returns a Pandas Series mapping each snapshot date to the total portfolio value
    for the given account, starting from the specified date (exclusive).
    """
    rows = session.query(
        PositionSnapshot.as_of_date,
        func.sum(PositionSnapshot.total_value)
    ).filter(
        PositionSnapshot.account_id == account_id,
        PositionSnapshot.as_of_date > from_date
    ).group_by(
        PositionSnapshot.as_of_date
    ).order_by(
        PositionSnapshot.as_of_date
    ).all()

    return pd.Series({row.as_of_date: float(row[1]) for row in rows})


def get_cash_flows(account_id: UUID, from_date: date) -> pd.Series:
    result = (
        session.query(Transaction.date, Transaction.action, Transaction.quantity)
        .filter_by(account_id=account_id)
        .filter_by(symbol="CASH")
        .filter(Transaction.date >= from_date)
        .filter(Transaction.action.in_([TransactionType.BUY, TransactionType.SELL]))
        .order_by(Transaction.date)
        .all()
    )

    cash_flow_map = {}

    for txn_date, action, quantity in result:
        qty = float(quantity)
        flow = qty if action == TransactionType.BUY else -qty
        cash_flow_map.setdefault(txn_date, 0.0)
        cash_flow_map[txn_date] += flow

    return pd.Series(cash_flow_map).sort_index()


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


def to_float(x):
    if isinstance(x, (float, int)):
        return round(float(x), 5)
    if isinstance(x, np.generic):  # includes np.float64, np.int64, etc.
        return round(x.item(), 5)
    return round(x,5)


def update_portfolio_metrics(email: str):
    user = session.query(User).filter_by(email=email).first()
    if not user:
        raise ValueError(f"No user with email {email}")

    accounts = session.query(Account).filter_by(user_id=user.user_id).all()

    for account in accounts:
        last_snapshot = session.query(func.max(PortfolioMetricsSnapshot.snapshot_date)) \
            .filter_by(account_id=account.account_id).scalar()
        start_date = last_snapshot + timedelta(days=1) if last_snapshot else date(2000, 1, 1)

        portfolio_series = get_portfolio_series(str(account.account_id), start_date)
        if portfolio_series.empty:
            continue

        cash_flows = get_cash_flows(account.account_id, start_date)
        daily_returns = compute_daily_returns(portfolio_series)
        twr = compute_twr(portfolio_series, cash_flows)
        sharpe = compute_sharpe_ratio(daily_returns)
        drawdown = compute_max_drawdown(portfolio_series)

        for i in range(1, len(portfolio_series)):
            snapshot_date = portfolio_series.index[i]
            value = portfolio_series.iloc[i]
            cash = 0
            cash_row = session.query(PositionSnapshot).filter_by(
                account_id=account.account_id,
                as_of_date=snapshot_date,
                symbol="CASH"
            ).first()
            if cash_row:
                cash = float(str(cash_row.quantity))

            rolling_7d = portfolio_series.iloc[max(0, i - 6):i + 1].pct_change().add(1).prod() - 1
            rolling_30d = portfolio_series.iloc[max(0, i - 29):i + 1].pct_change().add(1).prod() - 1

            session.merge(PortfolioMetricsSnapshot(
                snapshot_date=snapshot_date,
                account_id=account.account_id,
                portfolio_value=to_float(value),
                benchmark_value=None,  # Expected type 'Decimal | float', got 'None' instead
                portfolio_daily_return=to_float(daily_returns.get(snapshot_date)),
                benchmark_daily_return=None, # Expected type 'Decimal | float', got 'None' instead
                cash_balance=to_float(cash),
                twr_to_date=to_float(twr),
                rolling_return_7d=to_float(rolling_7d),
                rolling_return_30d=to_float(rolling_30d),
                sharpe_to_date=to_float(sharpe),
                drawdown_to_date=to_float(drawdown),
            ))

        session.commit()
        print(f"✅ Metrics updated for account {account.account_id}")


if __name__ == "__main__":
    update_portfolio_metrics('venkatachalapatee@gmail.com')


