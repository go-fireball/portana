from datetime import datetime
from typing import List, Dict

import pandas as pd
from sqlalchemy.orm import Session

from app.db import SessionLocal
from app.models.account import Account
from app.models.transaction import Transaction
from app.models.user import User

session: Session = SessionLocal()


def import_schwab_lot_details(file_path: str, email: str, account_number: str) -> List[Dict]:
    df = pd.read_csv(file_path, header=None)
    transactions = []
    current_symbol = None
    option_meta = None

    # Look up user by email
    user = session.query(User).filter_by(email=email).first()
    if not user:
        raise ValueError(f"No user found with email: {email}")

    # Look up account by account number and user_id
    account = session.query(Account).filter_by(account_number=account_number, user_id=user.user_id).first()
    if not account:
        raise ValueError(f"No account found for user {email} with account number {account_number}")

    for i in range(len(df)):
        row = df.iloc[i]
        first_cell = str(row.iloc[0])

        # Detect start of a new section
        if "Lot Details" in first_cell:
            current_symbol = first_cell.replace(" Lot Details", "").split(" for")[0].strip()
            option_meta = None

            parts = current_symbol.split()
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
                    current_symbol = parts[0]
                except Exception:
                    pass

            continue

        try:
            open_date = datetime.strptime(str(row.iloc[0]).strip(), "%m/%d/%Y").date()
            quantity = float(str(row.iloc[1]).strip())
            cost_share_str = str(row.iloc[3]).replace("$", "").replace(",", "").strip()
            cost_per_share = float(cost_share_str) if cost_share_str not in ("--", "") else None

            action = "sell_to_open" if quantity < 0 and option_meta else "buy"

            txn = Transaction(
                account_id=account.account_id,
                symbol=current_symbol,
                action=action,
                quantity=abs(quantity),
                price=cost_per_share,
                date=open_date,
                source="imported_lot",
                option_details=option_meta
            )
            session.add(txn)
            transactions.append(txn)

        except Exception:
            continue

    session.commit()
    print(f"✅ Imported {len(transactions)} transactions from {file_path}")
    return transactions
