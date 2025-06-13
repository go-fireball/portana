import os

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base, Session

# Load from environment or default
DATABASE_URL = os.getenv("DATABASE_URL", "postgresql://portana:secret@localhost:5432/portana")

# Create engine
engine = create_engine(DATABASE_URL, echo=True)

# Session factory
SessionLocal: sessionmaker[Session] = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Base class for models
Base = declarative_base()


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
