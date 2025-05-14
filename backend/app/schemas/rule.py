from pydantic import BaseModel


class RuleBase(BaseModel):
    name: str
    condition: str
    action: str


class RuleCreate(RuleBase):
    pass


class RuleResponse(RuleBase):
    id: int

    class Config:
        orm_mode = True
