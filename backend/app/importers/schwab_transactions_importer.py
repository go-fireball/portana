from datetime import datetime
from typing import List

import pandas as pd
from sqlalchemy.orm import Session

from app.db import SessionLocal
from app.models.account import Account
from app.models.transaction import Transaction
from app.models.transaction_type import TransactionType
from app.models.user import User

session: Session = SessionLocal()


def import_schwab_transactions(file_path: str, email: str, account_number: str) -> List[Transaction]:
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
            # Parse date
            date = datetime.strptime(row["Date"], "%m/%d/%Y").date()

            # Detect transaction type
            action_raw = row["Action"].strip().lower().replace(" ", "_")
            if action_raw not in TransactionType.__members__.values():
                print(f"⚠️ Skipping unknown action: {row['Action']}")
                continue
            action = TransactionType(action_raw)

            # Clean symbol
            raw_symbol = str(row["Symbol"]).strip()
            if raw_symbol in ("", "nan"):
                print(f"⚠️ Skipping transaction with missing symbol on {row['Date']}")
                continue
            parts = raw_symbol.split()
            option_meta = None
            if len(parts) >= 4:
                try:
                    expiry = datetime.strptime(parts[1], "%m/%d/%Y")
                    strike = float(parts[2])
                    opt_type = "call" if parts[3].upper() == "C" else "put"
                    option_meta = {
                        "base_symbol": parts[0],
                        "expiry": expiry.strftime("%Y-%m-%d"),
                        "strike": strike,
                        "type": opt_type
                    }
                    raw_symbol = f"{option_meta['base_symbol']}_{option_meta['expiry']}_{option_meta['strike']}_{option_meta['type'].upper()}"
                except Exception:
                    option_meta = None
            symbol = raw_symbol

            # Quantity
            qty_str = str(row["Quantity"]).replace(",", "").strip()
            quantity = float(qty_str) if qty_str else 0

            # Price
            price_str = str(row["Price"]).replace("$", "").replace(",", "").strip()
            price = float(price_str) if price_str not in ("", "--", "nan") else None

            # Determine instrument type
            instrument_type = "option" if "call" in symbol.lower() or "put" in symbol.lower() else "stock"

            txn = Transaction(
                account_id=account.account_id,
                symbol=symbol,
                action=action,
                instrument_type=instrument_type,
                quantity=abs(quantity),
                price=price,
                date=date,
                option_details=option_meta,
                source="imported_transaction"
            )

            session.add(txn)
            transactions.append(txn)

        except Exception as e:
            print(f"⚠️ Skipping row due to error: {e}")
            continue

    session.commit()
    print(f"✅ Imported {len(transactions)} transactions from {file_path}")
    return transactions
