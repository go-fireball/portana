from datetime import datetime
from typing import List, Dict

import pandas as pd
from sqlalchemy.orm import Session

from app.db import SessionLocal
from app.models import TransactionType
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
        first_cell = str(row.iloc[0]).strip()

        # Skip blank rows
        if first_cell == "" or all(str(cell).strip() == "" for cell in row):
            continue

        # Detect start of a new section
        if "Lot Details" in first_cell:
            current_symbol = first_cell.replace(" Lot Details", "").split(" for")[0].strip()
            option_meta = None

            # Try parsing as option
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
                    current_symbol = f"{option_meta['base_symbol']}_{option_meta['expiry']}_{option_meta['strike']}_{option_meta['type'].upper()}"
                except Exception:
                    pass
            continue

        # Skip subtotal rows
        if first_cell.lower() == "total":
            continue

        # Try parsing a valid row
        try:
            open_date = datetime.strptime(first_cell, "%m/%d/%Y").date()
            quantity_str = str(row.iloc[1]).replace(",", "").strip()
            quantity = float(quantity_str) if quantity_str else 0.0
            quantity = round(quantity, 5)

            cost_share_str = str(row.iloc[3]).replace("$", "").replace(",", "").strip()
            cost_per_share = float(cost_share_str) if cost_share_str not in ("--", "") else None
            cost_per_share = round(cost_per_share, 5)

            # Set action depending on the transaction type
            if quantity < 0 and option_meta:  # SELL TO OPEN for options
                action = TransactionType.SELL_TO_OPEN.value
            elif quantity > 0 and option_meta:  # BUY TO OPEN for options
                action = TransactionType.BUY_TO_OPEN.value
            elif quantity < 0:  # SELL for stocks
                action = TransactionType.SELL.value
            else:  # BUY for stocks
                action = TransactionType.BUY.value

            instrument_type = "option" if option_meta else "stock"

            txn = Transaction(
                account_id=account.account_id,
                symbol=current_symbol,
                action=action,
                quantity=abs(quantity) if action != TransactionType.SELL_TO_OPEN.value else -abs(quantity), # wouldn't quantity=quantity would solve this??
                price=cost_per_share,
                date=open_date,
                source="imported_lot",
                instrument_type=instrument_type,
                option_details=option_meta
            )
            session.add(txn)
            transactions.append(txn)
        except Exception:
            continue  # Skip unparsable rows

    session.commit()
    print(f"Imported {len(transactions)} transactions from {file_path}")
    return transactions
