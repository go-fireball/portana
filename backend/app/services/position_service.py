from collections import defaultdict
from copy import deepcopy
from datetime import timedelta
from decimal import Decimal
from typing import Type

import dateutil.utils
from sqlalchemy.orm import Session
from sqlalchemy.sql import func

from app.db import SessionLocal
from app.models import TransactionType
from app.models.account import Account
from app.models.position import Position
from app.models.position_snapshots import PositionSnapshot
from app.models.transaction import Transaction
from app.models.user import User

session: Session = SessionLocal()


def recalculate_positions(email: str, initial_load: bool = False):
    user = session.query(User).filter_by(email=email).first()
    if not user:
        raise ValueError(f"No user found with email: {email}")

    accounts = session.query(Account).filter_by(user_id=user.user_id).all()
    if not accounts:
        print("No accounts found for user.")
        return

    for account in accounts:
        txns = (
            session.query(Transaction)
            .filter_by(account_id=account.account_id)
            .order_by(Transaction.date.asc())
            .all()
        )
        if not txns:
            continue

        if initial_load:
            symbol_data = aggregate_transactions(txns, track_cash=False)
            end_date = txns[-1].date
            save_positions(account.account_id, symbol_data, dateutil.utils.today().date())
            save_position_snapshot(account.account_id, symbol_data, dateutil.utils.today().date())
            session.commit()
        else:
            last_snapshot_date = session.query(func.max(PositionSnapshot.as_of_date)).filter_by(
                account_id=account.account_id
            ).scalar()

            start_date = last_snapshot_date + timedelta(days=1) if last_snapshot_date else txns[0].date
            end_date = dateutil.utils.today().date()

            # Start by aggregating until start_date
            prev_txns: list[Type[Transaction]] = [txn for txn in txns if txn.date < start_date]
            symbol_data = aggregate_transactions(prev_txns, track_cash=False)
            previous_day_data = deepcopy(symbol_data)

            current_date = start_date
            while current_date <= end_date:
                day_txns = [txn for txn in txns if txn.date == current_date]
                symbol_data = update_with_day_transactions(previous_day_data, day_txns)

                save_position_snapshot(account.account_id, symbol_data, current_date)
                previous_day_data = deepcopy(symbol_data)
                current_date += timedelta(days=1)
            save_positions(account.account_id, symbol_data, end_date)  # Save only latest position once
        session.commit()

    print(f"✅ Recalculated positions and snapshots for user: {email}")


def aggregate_transactions(txns: list[Type[Transaction]], track_cash: bool = True):
    symbol_data = defaultdict(lambda: {"qty": Decimal(0), "total_cost": Decimal(0), "first_action": None})
    return update_with_day_transactions(symbol_data, txns, track_cash=track_cash)


def update_with_day_transactions(symbol_data, txns: list[Type[Transaction]], track_cash: bool = True):
    symbol_data = deepcopy(symbol_data)  # don't mutate caller’s dict

    for txn in txns:
        symbol = txn.symbol
        qty = Decimal(str(txn.quantity))
        price = Decimal(str(txn.price)) if txn.price else Decimal(0)
        action = txn.action.lower()
        amount = qty * price

        # Special case for direct CASH transactions (deposit/withdrawal)
        if symbol == "CASH":
            if action == "buy":
                symbol_data["CASH"]["qty"] += qty  # deposit
            elif action == "sell":
                symbol_data["CASH"]["qty"] -= qty  # withdrawal
            if symbol_data["CASH"]["first_action"] is None:
                symbol_data["CASH"]["first_action"] = TransactionType.BUY.value
            continue  # ✅ skip further processing

        if symbol_data[symbol]["first_action"] is None:
            if txn.instrument_type == "option" and action in ["buy", "buy_to_open", "sell_to_open"]:
                symbol_data[symbol]["first_action"] = action
            else:
                symbol_data[symbol]["first_action"] = TransactionType.BUY.value

        if action in ["buy", "buy_to_open"]:
            symbol_data[symbol]["total_cost"] += amount
            symbol_data[symbol]["qty"] += qty
            if track_cash:
                symbol_data["CASH"]["qty"] -= amount
        elif action in ["sell", "sell_to_close"]:
            symbol_data[symbol]["qty"] += qty
            symbol_data[symbol]["total_cost"] += amount
            if track_cash:
                symbol_data["CASH"]["qty"] += amount
        elif action == "sell_to_open":
            symbol_data[symbol]["qty"] += qty
            symbol_data[symbol]["total_cost"] += amount
            if track_cash:
                symbol_data["CASH"]["qty"] += amount
        elif action == "buy_to_close":
            symbol_data[symbol]["qty"] -= qty
            symbol_data[symbol]["total_cost"] += amount
            if track_cash:
                symbol_data["CASH"]["qty"] -= amount

    if track_cash and ("CASH" not in symbol_data or symbol_data["CASH"]["first_action"] is None):
        symbol_data["CASH"]["first_action"] = TransactionType.BUY.value

    return symbol_data


def save_positions(account_id, symbol_data, snapshot_date):
    # Delete all existing positions for this account
    session.query(Position).filter_by(account_id=account_id).delete()
    session.flush()  # Ensure deletion happens before inserts

    for symbol, data in symbol_data.items():
        quantity = round(data["qty"], 5)
        total_cost = data["total_cost"]
        first_action = data["first_action"] or TransactionType.BUY.value
        avg_cost = round(total_cost / quantity, 5) if quantity else None

        if quantity == 0:
            continue  # Skip zero-quantity positions

        session.add(Position(
            account_id=account_id,
            symbol=symbol,
            quantity=quantity,
            avg_cost=avg_cost,
            last_updated=snapshot_date,
            action=first_action
        ))


def save_position_snapshot(account_id, symbol_data, snapshot_date):
    session.query(PositionSnapshot).filter_by(account_id=account_id, as_of_date=snapshot_date).delete()

    for symbol, data in symbol_data.items():
        quantity = round(data["qty"], 5)
        total_cost = data["total_cost"]
        first_action = data["first_action"] or TransactionType.BUY.value

        # ✅ Special case for CASH
        if symbol == "CASH":
            avg_cost = Decimal("1.0")
        else:
            avg_cost = round(total_cost / quantity, 5) if quantity else None

        if quantity == 0:
            continue

        session.add(PositionSnapshot(
            account_id=account_id,
            symbol=symbol,
            quantity=quantity,
            avg_cost=avg_cost,
            as_of_date=snapshot_date,
            action=first_action
        ))
