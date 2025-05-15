from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from app.database import get_db
from app.crud import rule as rule_crud
from app.schemas.rule import RuleCreate, RuleResponse

router = APIRouter()


@router.post("/rules", response_model=RuleResponse)
def create_rule_route(rule_data: RuleCreate, db: Session = Depends(get_db)):
    return rule_crud.create_rule(db, rule_data)


@router.get("/rules", response_model=List[RuleResponse])
def get_rules(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    return rule_crud.get_rules(db, skip=skip, limit=limit)


@router.get("/rules/{rule_id}", response_model=RuleResponse)
def get_rule(rule_id: int, db: Session = Depends(get_db)):
    rule = rule_crud.get_rule(db, rule_id)
    if rule is None:
        raise HTTPException(status_code=404, detail="Rule not found")
    return rule
