from sqlalchemy import Column, Integer, String, Text, DateTime, Boolean, ForeignKey, Table
from sqlalchemy.orm import relationship
from datetime import datetime
from .base import Base

# Association table for Rule-ConditionType relationship
rule_conditions = Table(
    'rule_conditions',
    Base.metadata,
    Column('rule_id', Integer, ForeignKey('rules.id')),
    Column('condition_type_id', Integer, ForeignKey('condition_types.id')),
    Column('value', String),  # Store the selected value for the condition
    Column('year', Integer, nullable=True)  # For year-based conditions
)


class Rule(Base):
    __tablename__ = "rules"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, unique=True, index=True)
    description = Column(Text, nullable=True)
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime, default=datetime.now)
    updated_at = Column(DateTime, default=datetime.now, onupdate=datetime.now)

    # Relationships
    conditions = relationship("ConditionType", secondary=rule_conditions)
    action = Column(String)  # Document type to request
    # Description of the document request
    action_description = Column(Text, nullable=True)
