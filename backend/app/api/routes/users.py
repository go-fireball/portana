from fastapi import APIRouter, Depends
from sqlalchemy import func
from sqlalchemy.orm import Session

from app.db import get_db
from app.models import User, Account, Position, PositionSnapshot, PortfolioMetricsSnapshot

router = APIRouter()


@router.get("/")
def list_users(db: Session = Depends(get_db)):
    results = db.query(User.user_id, User.name, User.email).all()
    return {
        "users": [
            {"id": str(user_id), "name": name, "email": email}
            for user_id, name, email in results
        ]
    }


@router.get("/{user_id}/positions")
def get_positions(user_id: str, db: Session = Depends(get_db)):
    # Get all account_ids for this user
    account_ids = (
        db.query(Account.account_id)
        .filter(Account.user_id == user_id)
        .subquery()
    )

    # Aggregate positions by symbol
    results = (
        db.query(
            Position.symbol,
            func.sum(Position.quantity).label("total_quantity"),
            func.sum(Position.quantity * Position.avg_cost).label("total_cost")
        )
        .filter(Position.account_id.in_(account_ids))
        .group_by(Position.symbol)
        .all()
    )

    return {
        "positions": [
            {
                "symbol": symbol,
                "quantity": round(float(quantity), 4),
                "total_cost": round(float(total_cost), 4)
            }
            for symbol, quantity, total_cost in results
        ]
    }


@router.get("/{user_id}/portfolio/summary")
def portf(user_id: str, db: Session = Depends(get_db)):
    # Step 1: Get all account_ids for the user
    account_ids = (
        db.query(Account.account_id)
        .filter(Account.user_id == user_id)
        .subquery()
    )
    results = (
        db.query(
            PositionSnapshot.as_of_date,
            func.sum(PositionSnapshot.total_value).label("portfolio_value")
        )
        .filter(PositionSnapshot.account_id.in_(account_ids))
        .group_by(PositionSnapshot.as_of_date)
        .order_by(PositionSnapshot.as_of_date.asc())
        .all()
    )
    return {
        "portfolio": [
            {
                "as_of_date": as_of_date.isoformat(),
                "total_value": float(portfolio_value)
            }
            for as_of_date, portfolio_value in results
        ]
    }


@router.get("/{user_id}/portfolio/rolling-returns")
def get_rolling_returns(user_id: str, db: Session = Depends(get_db)):
    results = (
        db.query(
            PortfolioMetricsSnapshot.snapshot_date,
            PortfolioMetricsSnapshot.account_id,
            Account.account_number.label("account_number"),
            PortfolioMetricsSnapshot.rolling_return_7d,
            PortfolioMetricsSnapshot.rolling_return_30d
        )
        .join(Account, PortfolioMetricsSnapshot.account_id == Account.account_id)
        .filter(Account.user_id == user_id)
        .order_by(PortfolioMetricsSnapshot.snapshot_date.asc())
        .all()
    )

    return {
        "returns": [
            {
                "snapshot_date": snapshot_date.isoformat(),
                "account_id": str(account_id),
                "account_number": account_number,
                "rolling_return_7d": float(rolling_7d or 0),
                "rolling_return_30d": float(rolling_30d or 0),
            }
            for snapshot_date, account_id, account_number, rolling_7d, rolling_30d in results
        ]
    }
