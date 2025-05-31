from enum import Enum


class TransactionType(str, Enum):
    BUY = "buy"
    SELL = "sell"
    BUY_TO_OPEN = "buy_to_open"
    SELL_TO_OPEN = "sell_to_open"
    BUY_TO_CLOSE = "buy_to_close"
    SELL_TO_CLOSE = "sell_to_close"
    SELL_SHORT = 'short_sell'
    DIVIDEND = "dividend"
    JOURNAL = "journal"
    QUALIFIED_DIVIDEND = "qualified_dividend"
    CASH_DIVIDEND = "cash_dividend"
    CREDIT_INTEREST = "credit_interest"
    MARGIN_INTEREST = "margin_interest"
    MONEYLINK_TRANSFER = "moneylink_transfer"
    JOURNALED_SHARES = "journaled_shares"
