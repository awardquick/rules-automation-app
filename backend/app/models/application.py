from sqlalchemy import Column, Integer, String, DateTime, Boolean
from datetime import datetime
from .base import Base


class Application(Base):
    __tablename__ = "applications"

    id = Column(Integer, primary_key=True, index=True)
    family_status = Column(String)
    business_owner = Column(Boolean)
    filed_us_taxes = Column(Boolean)
    tax_year = Column(Integer)
    submitted_at = Column(DateTime)
    created_at = Column(DateTime, default=datetime.now)
    updated_at = Column(DateTime, default=datetime.now, onupdate=datetime.now)
