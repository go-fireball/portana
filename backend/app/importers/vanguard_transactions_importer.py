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


def import_vanguard_transactions(file_path: str, email: str, account_number: str) -> List[Transaction]:
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
            action_str = row["Transaction Type"].strip().lower().replace(" ", "_")
            if action_str not in ("buy", "sell"):
                continue
            action = TransactionType(action_str)

            symbol = str(row["Symbol"]).strip()
            if symbol in ("", "nan", "VMFXX"):
                continue

            investment_name = str(row["Investment Name"]).lower()
            if "money market" in investment_name:
                continue

            date = datetime.strptime(row["Trade Date"], "%m/%d/%Y").date()

            quantity = float(str(row["Shares"]).replace(",", "").strip())
            price_str = str(row["Share Price"]).replace("$", "").replace(",", "").strip()
            price = float(price_str) if price_str not in ("", "--", "nan") else None
            price = round(price,5)

            instrument_type = "stock"

            txn = Transaction(
                account_id=account.account_id,
                symbol=symbol,
                action=action,
                instrument_type=instrument_type,
                quantity=abs(quantity),
                price=price,
                date=date,
                option_details=None,
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
