from datetime import datetime
from typing import List
import re
import pandas as pd
from sqlalchemy.orm import Session

from app.db import SessionLocal
from app.models.transaction import Transaction
from app.models.transaction_type import TransactionType
from app.models.account import Account
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


def import_fidelity_transactions(file_path: str, email: str, account_number: str) -> List[Transaction]:
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
            date_str = row["Run Date"]
            if pd.isna(date_str):
                continue  # skip empty rows

            date = datetime.strptime(date_str.strip(), "%m/%d/%Y").date()
            action_str = str(row["Action"]).strip()
            symbol = str(row["Symbol"]).strip() if pd.notna(row["Symbol"]) else ""
            amount = float(row["Amount ($)"]) if pd.notna(row["Amount ($)"]) else 0.0
            quantity = float(row["Quantity"]) if pd.notna(row["Quantity"]) else 0.0
            price = float(row["Price ($)"]) if pd.notna(row["Price ($)"]) else None

            # Determine action
            if symbol == "" and amount != 0:
                symbol = "CASH"
                action = TransactionType.BUY if amount > 0 else TransactionType.SELL
                quantity = abs(amount)
                price = 1.0
            elif action_str.upper().startswith("YOU BOUGHT"):
                action = TransactionType.BUY
            elif action_str.upper().startswith("YOU SOLD OPENING"):
                action = TransactionType.SELL_TO_OPEN
            elif action_str.upper().startswith("YOU SOLD CLOSING"):
                action = TransactionType.SELL_TO_CLOSE
            else:
                print(f"⚠️ Unknown or unhandled action: {action_str}")
                continue

            instrument_type = "cash" if symbol == "CASH" else "stock"

            raw_symbol = symbol
            if raw_symbol.startswith("-") or raw_symbol.startswith("+"):
                parsed = parse_option_symbol(raw_symbol)
                option_details = {
                    "base_symbol": parsed["base_symbol"],
                    "expiry": parsed["expiry"].isoformat(),
                    "strike": parsed["strike"],
                    "type": parsed["type"]
                }
                # action = TransactionType.SELL_TO_OPEN if raw_symbol.startswith("-") else TransactionType.BUY_TO_OPEN
                instrument_type = "option"
                current_symbol = f"{option_details['base_symbol']}_{option_details['expiry']}_{option_details['strike']}_{option_details['type'].upper()}"
            else:
                current_symbol = raw_symbol
            if instrument_type == "option" and action == TransactionType.SELL_TO_CLOSE:
                action = TransactionType.SELL_TO_CLOSE
            elif instrument_type == "option":
                # if action_str.upper().startswith("YOU SOLD OPENING"):
                #     action = TransactionType.SELL_TO_OPEN
                action = (
                    TransactionType.BUY_TO_OPEN if quantity > 0 else TransactionType.SELL_TO_OPEN
                )
            else:
                action = TransactionType.BUY if quantity > 0 else TransactionType.SELL

            txn = Transaction(
                account_id=account.account_id,
                symbol=current_symbol,
                action=action,
                instrument_type=instrument_type,
                quantity=quantity,
                price=price,
                date=date,
                source="imported_transaction"
            )

            session.add(txn)
            transactions.append(txn)

        except Exception as e:
            print(f"⚠️ Skipping row due to error: {e}")
            continue

    session.commit()
    print(f"✅ Imported {len(transactions)} Fidelity transactions from {file_path}")
    return transactions
