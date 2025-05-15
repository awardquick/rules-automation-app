from datetime import datetime
from pydantic import BaseModel, ConfigDict


class EvaluationBase(BaseModel):
    application_id: int
    rule_id: int
    action_taken: str


class EvaluationCreate(EvaluationBase):
    pass


class EvaluationResponse(EvaluationBase):
    id: int
    application_id: int
    rule_id: int
    action_taken: str
    evaluated_at: datetime

    model_config = ConfigDict(from_attributes=True,
                              arbitrary_types_allowed=True)
