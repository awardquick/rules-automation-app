import os

# Database settings
DATABASE_URL = os.getenv(
    "DATABASE_URL",
    "postgresql://postgres:postgres@db:5432/rules_db"
)

# Other settings can be added here
