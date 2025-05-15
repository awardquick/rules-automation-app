from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from app.core.config import settings
from .seed import seed_condition_types

# Create engine with correct credentials
engine = create_engine(settings.database_url)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


def seed_database():
    db = SessionLocal()
    try:
        seed_condition_types(db)
    finally:
        db.close()


if __name__ == "__main__":
    seed_database()
