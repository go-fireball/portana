from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.db import get_db
from app.models.position import Position

router = APIRouter()


@router.get("/")
def list_positions(db: Session = Depends(get_db)):
    positions = db.query(Position).all()
    return [
        {
            "position_id": str(p.position_id),
            "account_id": str(p.account_id),
            "symbol": p.symbol,
            "quantity": float(str(p.quantity)),
            "avg_cost": float(str(p.avg_cost)) if p.avg_cost is not None else None
        }
        for p in positions
    ]
