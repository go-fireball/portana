import uuid
from datetime import datetime, UTC

from app.db import SessionLocal
from app.models.account import Account
from app.models.user import User

session = SessionLocal()


def create_account(email: str, brokerage: str, account_number: str, nickname: str):
    # Look up the user by email
    user = session.query(User).filter_by(email=email).first()
    if not user:
        print(f"No user found with email: {email}")
        return None

    account = Account(
        account_id=uuid.uuid4(),
        user_id=user.user_id,
        brokerage=brokerage,
        account_number=account_number,
        nickname=nickname,
        created_at=datetime.now(UTC)
    )
    session.add(account)
    session.commit()
    print(f"Created account: {account.account_id} ({brokerage} - {account_number})")
    return account.account_id
