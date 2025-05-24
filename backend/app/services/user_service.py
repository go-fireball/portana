import uuid
from datetime import datetime, UTC

from app.db import SessionLocal
from app.models.user import User

session = SessionLocal()


def create_user(email: str, name: str):
    # Check if user already exists
    existing = session.query(User).filter_by(email=email).first()
    if existing:
        print(f"User already exists: {existing.user_id} ({email})")
        return existing.user_id

    # Create new user if not found
    user = User(user_id=uuid.uuid4(), email=email, name=name, created_at=datetime.now(UTC))
    session.add(user)
    session.commit()
    print(f"Created user: {user.user_id} ({email})")
    return user.user_id
