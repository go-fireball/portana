from collections import defaultdict
from datetime import date
from decimal import Decimal

from sqlalchemy.orm import Session

from app.db import SessionLocal
from app.models.account import Account
from app.models.position import Position
from app.models.position_snapshots import PositionSnapshot
from app.models.transaction import Transaction
from app.models.user import User

session: Session = SessionLocal()


def recalculate_positions(email: str):
    user = session.query(User).filter_by(email=email).first()
    if not user:
        raise ValueError(f"No user found with email: {email}")

    accounts = session.query(Account).filter_by(user_id=user.user_id).all()
    if not accounts:
        print("No accounts found for user.")
        return

    # Clear existing positions and snapshots for simplicity
    session.query(Position).filter(Position.account_id.in_([acc.account_id for acc in accounts])).delete(
        synchronize_session=False)
    session.query(PositionSnapshot).filter(
        PositionSnapshot.account_id.in_([acc.account_id for acc in accounts])).delete(synchronize_session=False)

    for account in accounts:
        txns = (
            session.query(Transaction)
            .filter_by(account_id=account.account_id)
            .order_by(Transaction.date.asc())
            .all()
        )

        symbol_data = defaultdict(lambda: {"qty": Decimal(0), "total_cost": Decimal(0)})

        for txn in txns:
            symbol = txn.symbol
            qty = Decimal(txn.quantity)
            price = Decimal(txn.price) if txn.price else Decimal(0)

            if txn.action.lower() in ["buy", "buy_to_open"]:
                symbol_data[symbol]["total_cost"] += qty * price
                symbol_data[symbol]["qty"] += qty
            elif txn.action.lower() in ["sell", "sell_to_close"]:
                symbol_data[symbol]["qty"] -= qty
                symbol_data[symbol]["total_cost"] -= qty * price

        for symbol, data in symbol_data.items():
            quantity = data["qty"]
            total_cost = data["total_cost"]
            if quantity == 0:
                continue
            avg_cost = total_cost / quantity if quantity else None

            pos = Position(
                account_id=account.account_id,
                symbol=symbol,
                quantity=quantity,
                avg_cost=avg_cost,
                last_updated=date.today()
            )
            session.add(pos)

            snapshot = PositionSnapshot(
                account_id=account.account_id,
                symbol=symbol,
                quantity=quantity,
                avg_cost=avg_cost,
                as_of_date=date.today()
            )
            session.add(snapshot)

    session.commit()
    print(f"Recalculated positions and snapshots for user: {email}")
