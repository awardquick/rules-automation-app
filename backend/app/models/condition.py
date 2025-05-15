from sqlalchemy import Column, Integer, String, Text, JSON
from .base import Base


class ConditionType(Base):
    __tablename__ = "condition_types"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, unique=True, index=True)  # e.g., "Is Business Owner"
    field = Column(String, unique=True, index=True)  # e.g., "business_owner"
    description = Column(Text, nullable=True)
    # e.g., "boolean", "string", "enum", "year_boolean"
    data_type = Column(String, nullable=True)
    # For enum types, e.g., ["New", "Returning"]
    options = Column(JSON, nullable=True)
    # For year-based conditions, e.g., "tax_year"
    year_field = Column(String, nullable=True)
