from sqlalchemy.orm import Session
from app.models.rule import Rule
from app.schemas.rule import RuleCreate, RuleResponse


def create_rule(db: Session, rule: RuleCreate) -> RuleResponse:
    db_rule = Rule(**rule.dict())
    db.add(db_rule)
    db.commit()
    db.refresh(db_rule)
    return db_rule


def get_rules(db: Session):
    return db.query(Rule).all()
