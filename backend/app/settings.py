import os

# Database settings
DATABASE_URL = os.getenv(
    "DATABASE_URL",
    "postgresql://user:password@db:5432/rules_db"
)

# Other settings can be added here
