from datetime import datetime, date
from decimal import Decimal
from typing import List
import pandas as pd
import re

from sqlalchemy.orm import Session
from app.db import SessionLocal
from app.models.account import Account
from app.models.transaction import Transaction
from app.models.transaction_type import TransactionType
from app.models.user import User

session: Session = SessionLocal()


def parse_option_symbol(raw: str):
    """Parse Fidelity-style option symbol like -NVDA250919C70"""
    clean = raw.lstrip("+-")
    match = re.match(r"^([A-Z]+)(\d{6})([CP])(\d+(\.\d+)?)$", clean)
    if not match:
        raise ValueError(f"Unrecognized option symbol format: {raw}")

    base, expiry_str, opt_type, strike, _ = match.groups()
    expiry = datetime.strptime(expiry_str, "%y%m%d").date()
    return {
        "formatted_symbol": f"{base}_{expiry.isoformat()}_{strike}_{opt_type.upper()}",
        "base_symbol": base,
        "expiry": expiry,
        "strike": float(strike),
        "type": "call" if opt_type.upper() == "C" else "put"
    }


def import_fidelity_positions(file_path: str, email: str, account_number: str) -> List[Transaction]:
    df = pd.read_csv(file_path)
    transactions = []

    # Validate user and account
    user = session.query(User).filter_by(email=email).first()
    if not user:
        raise ValueError(f"No user found with email: {email}")

    account = session.query(Account).filter_by(account_number=account_number, user_id=user.user_id).first()
    if not account:
        raise ValueError(f"No account found for user {email} with account number {account_number}")

    for _, row in df.iterrows():
        try:
            raw_symbol = str(row.get("Symbol", "")).strip()
            if not raw_symbol or raw_symbol.lower() == "nan":
                continue

            # Skip rows with no quantity or known non-investment placeholders
            quantity_str = str(row.get("Quantity", "")).replace(",", "").strip()
            if not quantity_str or quantity_str.lower() in ("nan", "--"):
                continue

            quantity = float(quantity_str)
            if quantity == 0.0:
                continue

            avg_cost_str = str(row.get("Average Cost Basis", "")).replace("$", "").replace(",", "").strip()
            price = float(avg_cost_str) if avg_cost_str not in ("", "nan", "--") else None

            date_today = date.today()
            instrument_type = "stock"
            option_details = None
            # action = TransactionType.BUY

            if raw_symbol.startswith("-") or raw_symbol.startswith("+"):
                parsed = parse_option_symbol(raw_symbol)
                symbol = parsed["formatted_symbol"]
                option_details = {
                    "base_symbol": parsed["base_symbol"],
                    "expiry": parsed["expiry"].isoformat(),
                    "strike": parsed["strike"],
                    "type": parsed["type"]
                }
                # action = TransactionType.SELL_TO_OPEN if raw_symbol.startswith("-") else TransactionType.BUY_TO_OPEN
                instrument_type = "option"
            else:
                symbol = raw_symbol

            if instrument_type == "option":
                action = (
                    TransactionType.BUY_TO_OPEN if quantity > 0 else TransactionType.SELL_TO_OPEN
                )
            else:
                action = TransactionType.BUY if quantity > 0 else TransactionType.SELL

            txn = Transaction(
                account_id=account.account_id,
                symbol=symbol,
                action=action,
                instrument_type=instrument_type,
                quantity=abs(quantity),
                price=Decimal(price) if price is not None else None,
                date=date_today,
                source="imported_position",
                option_details=option_details
            )

            session.add(txn)
            transactions.append(txn)

        except Exception as e:
            print(f"⚠️ Error parsing row: {e}")
            continue

    session.commit()
    print(f"✅ Imported {len(transactions)} transactions from {file_path}")
    return transactions
