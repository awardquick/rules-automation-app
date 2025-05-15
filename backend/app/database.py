from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from .core.config import settings

print("Database URL:", settings.database_url)  # Debug print

engine = create_engine(settings.database_url)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


def get_database_url():
    return settings.database_url
