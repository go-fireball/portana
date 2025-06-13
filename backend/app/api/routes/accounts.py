from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.db import SessionLocal, get_db
from app.models import Position
from app.models.account import Account
from uuid import UUID

router = APIRouter()


@router.get("/")
def list_accounts(db: Session = Depends(get_db)):
    results = db.query(Account.account_id, Account.account_number).all()
    return {
        "accounts": [
            {"account_id": str(account_id), "account_number": account_number}
            for account_id, account_number in results
        ]
    }


@router.get("/{account_id}/positions")
def get_positions_by_account(account_id: UUID, db: Session = Depends(get_db)):
    positions = db.query(Position).filter_by(account_id=account_id).all()
    return [
        {
            "position_id": str(p.position_id),
            "symbol": p.symbol,
            "quantity": float(str(p.quantity)),
            "avg_cost": float(str(p.avg_cost)) if p.avg_cost is not None else None
        }
        for p in positions
    ]
