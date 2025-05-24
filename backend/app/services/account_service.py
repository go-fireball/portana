import uuid
from datetime import datetime, UTC

from app.db import SessionLocal
from app.models.account import Account

session = SessionLocal()


def create_account(user_id: str, brokerage: str, account_number: str, nickname: str):
    account = Account(
        account_id=uuid.uuid4(),
        user_id=user_id,
        brokerage=brokerage,
        account_number=account_number,
        nickname=nickname,
        created_at=datetime.now(UTC)
    )
    session.add(account)
    session.commit()
    print(f"Created account: {account.account_id} ({brokerage} - {account_number})")
    return account.account_id
