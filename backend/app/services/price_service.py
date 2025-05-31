from datetime import date, datetime
from decimal import Decimal, ROUND_HALF_UP

import yfinance as yf
from sqlalchemy.orm import Session
from sqlalchemy.sql.operators import and_

from app.db import SessionLocal
from app.models import PositionSnapshot
from app.models.position import Position
from app.models.price import Price  # optional, if you store prices

# Define precision to 5 decimal places
PRECISION = Decimal("0.00001")


def parse_option_symbol(option_symbol: str):
    try:
        parts = option_symbol.split("_")
        underlying = parts[0]
        expiry = parts[1]
        strike = float(parts[2])
        option_type = parts[3].lower()
        return underlying, expiry, strike, option_type
    except Exception as e:
        raise ValueError(f"Invalid option symbol format: {option_symbol}") from e


def get_option_price(symbol: str) -> Decimal:
    underlying, expiry, strike, option_type = parse_option_symbol(symbol)
    ticker = yf.Ticker(underlying)
    chain = ticker.option_chain(expiry)
    df = chain.puts if option_type == 'put' else chain.calls
    row = df[df['strike'] == strike]
    if row.empty:
        raise ValueError(f"No matching strike {strike} for {symbol}")
    return Decimal(row.iloc[0]['lastPrice'])


def get_equity_price(symbol: str) -> Decimal:
    ticker = yf.Ticker(symbol)
    hist = ticker.history(period="1d")
    if hist.empty:
        raise ValueError(f"No price history for {symbol}")
    return Decimal(hist["Close"].iloc[-1])


def fetch_and_store_prices():
    session: Session = SessionLocal()
    today = date.today()

    symbols = session.query(Position.symbol).distinct().all()
    symbols = [row.symbol for row in symbols]

    for symbol in symbols:
        try:
            # Skip if price already exists
            exists = session.query(Price).filter_by(symbol=symbol, price_date=today).first()
            if exists:
                print(f"[{symbol}] Price already stored for {today}, skipping.")
                continue

            if "_" in symbol:
                underlying, expiry_str, _, _ = parse_option_symbol(symbol)
                expiry_date = datetime.strptime(expiry_str, "%Y-%m-%d").date()
                if expiry_date < today:
                    print(f"[{symbol}] Option expired on {expiry_date}, skipping.")
                    continue
                price = get_option_price(symbol)
            else:
                price = get_equity_price(symbol)

            price = round(price, 4)
            print(f"[{symbol}] Price on {today}: ${price}")

            session.add(Price(symbol=symbol, price_date=today, price=price))

        except Exception as e:
            print(f"[{symbol}] Error fetching price: {e}")

    session.commit()
    session.close()
    hydrate_missing_prices()


def hydrate_missing_prices():
    # Fetch all position snapshots with missing price
    session: Session = SessionLocal()
    snapshots_to_update = (
        session.query(PositionSnapshot)
        .filter(PositionSnapshot.price.is_(None))
        .all()
    )

    print(f"Found {len(snapshots_to_update)} snapshots to update.")
    updated_count = 0

    for snapshot in snapshots_to_update:
        matching_price = (
            session.query(Price)
            .filter(
                and_(
                    Price.symbol == snapshot.symbol,
                    Price.price_date <= snapshot.as_of_date
                )
            )
            .order_by(Price.price_date.desc())
            .first()
        )

        if matching_price and snapshot.quantity is not None:
            price_val = Decimal(str(matching_price.price)).quantize(PRECISION, rounding=ROUND_HALF_UP)
            qty_val = Decimal(str(snapshot.quantity))
            total_val = qty_val * price_val

            # Check if it's an option symbol (e.g., "TSLA_2025-06-20_210.0_PUT")
            if "_" in snapshot.symbol:
                total_val *= 100

            snapshot.price = price_val
            snapshot.total_value = total_val.quantize(PRECISION, rounding=ROUND_HALF_UP)
            updated_count += 1

    session.commit()
    print(f"Updated {updated_count} position snapshot(s) with price and total_value.")
