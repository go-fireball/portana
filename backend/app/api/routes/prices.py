from fastapi import APIRouter, Depends
from sqlalchemy import func, and_
from sqlalchemy.orm import Session

from app.db import get_db
from app.models import Price, Account, Position, PositionSnapshot, PortfolioMetricsSnapshot

router = APIRouter()


@router.get("/")
def list_users(db: Session = Depends(get_db)):
    # Subquery: Get the latest date per symbol
    subq = (
        db.query(
            Price.symbol,
            func.max(Price.price_date).label("latest_date")
        )
        .group_by(Price.symbol)
        .subquery()
    )
    results = (
        db.query(Price.symbol, Price.price_date, Price.price)
        .join(subq, and_(
            Price.symbol == subq.c.symbol,
            Price.price_date == subq.c.latest_date
        ))
        .all()
    )
    return {
        "prices": [
            {"symbol": symbol, "price_date": price_date, "price": float(price)}
            for symbol, price_date, price in results
        ]
    }
