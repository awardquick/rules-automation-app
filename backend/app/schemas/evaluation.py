from pydantic import BaseModel


class EvaluationBase(BaseModel):
    application_id: int
    rule_id: int
    action_taken: str


class EvaluationCreate(EvaluationBase):
    pass


class EvaluationResponse(EvaluationBase):
    id: int
    evaluated_at: datetime

    class Config:
        orm_mode = True
