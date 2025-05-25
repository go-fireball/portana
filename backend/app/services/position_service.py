from collections import defaultdict
from datetime import date
from decimal import Decimal

from sqlalchemy.orm import Session

from app.db import SessionLocal
from app.models import TransactionType
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

        symbol_data = defaultdict(lambda: {"qty": Decimal(0), "total_cost": Decimal(0),
                                           "first_action": None})

        for txn in txns:
            symbol = txn.symbol
            qty = Decimal(txn.quantity)
            price = Decimal(txn.price) if txn.price else Decimal(0)

            action = txn.action.lower()
            if txn.instrument_type == "option":
                # For options, we store the first opening action (BUY TO OPEN / SELL TO OPEN)
                if symbol_data[symbol]["first_action"] is None:  # This doesn't work as expected
                    if action in ["buy", "buy_to_open", "sell_to_open"]:
                        symbol_data[symbol]["first_action"] = action
            else:
                # For stocks, we store "BUY" as the first action, which opens the position
                if symbol_data[symbol]["first_action"] is None:
                    symbol_data[symbol]["first_action"] = TransactionType.BUY.value

            if action in ["buy", "buy_to_open"]:
                symbol_data[symbol]["total_cost"] += qty * price
                symbol_data[symbol]["qty"] += qty
            elif action in ["sell", "sell_to_close"]:
                symbol_data[symbol]["qty"] -= qty
                symbol_data[symbol]["total_cost"] -= qty * price
            elif action == "sell_to_open":  # writing options
                symbol_data[symbol]["qty"] += qty
                symbol_data[symbol]["total_cost"] -= qty * price  # credit
            elif action == "buy_to_close":  # closing written option
                symbol_data[symbol]["qty"] -= qty
                symbol_data[symbol]["total_cost"] += qty * price  # debit

        for symbol, data in symbol_data.items():
            quantity = data["qty"]
            total_cost = data["total_cost"]
            first_action = data["first_action"]
            first_action = str(first_action) if first_action else TransactionType.BUY.value
            if quantity == 0:
                continue
            avg_cost = total_cost / quantity if quantity else None
            avg_cost = round(avg_cost, 5) if avg_cost else None
            quantity = round(quantity, 5)

            pos = Position(
                account_id=account.account_id,
                symbol=symbol,
                quantity=quantity,
                avg_cost=avg_cost,
                last_updated=date.today(),
                action=first_action
            )
            session.add(pos)

            snapshot = PositionSnapshot(
                account_id=account.account_id,
                symbol=symbol,
                quantity=quantity,
                avg_cost=avg_cost,
                as_of_date=date.today(),
                action=first_action
            )
            session.add(snapshot)

    session.commit()
    print(f"Recalculated positions and snapshots for user: {email}")
