# Generalized parser for Schwab Lot Details files
from datetime import datetime
from typing import List, Dict

import pandas as pd


def import_schwab_lot_details(file_path: str, account_number: str) -> List[Dict]:
    df = pd.read_csv(file_path, header=None)
    transactions = []
    current_symbol = None
    option_meta = None

    for i in range(len(df)):
        row = df.iloc[i]
        first_cell = str(row.iloc[0])

        # Detect start of a new section
        if "Lot Details" in first_cell:
            # Extract symbol (stock or option)
            current_symbol = first_cell.replace(" Lot Details", "").split(" for")[0].strip()
            option_meta = None

            # Try to parse as option
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
                    current_symbol = parts[0]  # overwrite with just base symbol
                except Exception:
                    pass  # treat as stock if parsing fails

            continue

        # Detect a valid data row (starts with date)
        try:
            open_date = datetime.strptime(str(row.iloc[0]).strip(), "%m/%d/%Y").date()
            quantity = float(str(row.iloc[1]).strip())
            cost_share_str = str(row.iloc[3]).replace("$", "").replace(",", "").strip()
            cost_per_share = float(cost_share_str) if cost_share_str not in ("--", "") else None

            action = "sell_to_open" if quantity < 0 and option_meta else "buy"

            transactions.append({
                "account_id": account_number,
                "symbol": current_symbol,
                "action": action,
                "quantity": abs(quantity),
                "price": cost_per_share,
                "date": open_date.isoformat(),
                "source": "imported_lot",
                "option_details": option_meta
            })
        except Exception:
            continue  # skip non-parsable rows

    return transactions
