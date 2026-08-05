from collections.abc import Generator

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from app.core.config import settings

# pool_pre_ping avoids "server closed the connection" errors after idle periods,
# which matter once this runs long-term on a real server instead of localhost.
engine = create_engine(settings.DATABASE_URL, pool_pre_ping=True)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


def get_db() -> Generator:
    """FastAPI dependency that yields a DB session and always closes it."""
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
