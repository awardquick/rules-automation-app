from pydantic import BaseModel
from typing import List, Optional
from datetime import datetime
from .condition import ConditionTypeBase


class RuleCondition(BaseModel):
    condition_type_id: int
    value: str
    year: Optional[int] = None


class RuleBase(BaseModel):
    name: str
    description: Optional[str] = None
    conditions: List[RuleCondition]
    action: str  # Document type to request
    action_description: Optional[str] = None


class RuleCreate(RuleBase):
    pass


class RuleResponse(RuleBase):
    id: int
    is_active: bool
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True
