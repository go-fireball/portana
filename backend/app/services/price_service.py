from datetime import date
from decimal import Decimal

import yfinance as yf
from sqlalchemy.orm import Session

from app.db import SessionLocal
from app.models.position import Position
from app.models.price import Price  # optional, if you store prices


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

            # Fetch from Yahoo
            price = (
                get_option_price(symbol)
                if "_" in symbol else
                get_equity_price(symbol)
            )
            price = round(price, 4)
            print(f"[{symbol}] Price on {today}: ${price}")

            session.add(Price(symbol=symbol, price_date=today, price=price))

        except Exception as e:
            print(f"[{symbol}] Error fetching price: {e}")

    session.commit()
    session.close()
