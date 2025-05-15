from pydantic import BaseModel, ConfigDict
from typing import Optional, List


class ConditionTypeBase(BaseModel):
    name: str
    field: str
    description: Optional[str] = None
    data_type: Optional[str] = None
    options: Optional[List[str]] = None
    year_field: Optional[str] = None


class ConditionTypeCreate(ConditionTypeBase):
    pass


class ConditionTypeResponse(ConditionTypeBase):
    id: int

    model_config = ConfigDict(from_attributes=True)
