from sqlalchemy import Column, ForeignKey, Integer, String, DateTime
from datetime import datetime
from .base import Base


class Evaluation(Base):
    __tablename__ = "evaluations"

    id = Column(Integer, primary_key=True, index=True)
    application_id = Column(Integer, ForeignKey("applications.id"))
    rule_id = Column(Integer, ForeignKey("rules.id"))
    action_taken = Column(String)
    evaluated_at = Column(DateTime, default=datetime.now)
    created_at = Column(DateTime, default=datetime.now)
    updated_at = Column(DateTime, default=datetime.now, onupdate=datetime.now)
