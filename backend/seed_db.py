import os
from app.db.seed import seed_condition_types, seed_sample_rule
from app.db.session import SessionLocal

# Set the correct database URL
os.environ["DATABASE_URL"] = "postgresql://postgres:postgres@localhost:5432/rules_db"

if __name__ == "__main__":
    db = SessionLocal()
    seed_condition_types(db)
    seed_sample_rule(db)
    print("Database seeded successfully!")
