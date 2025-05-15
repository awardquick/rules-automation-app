from sqlalchemy.orm import Session
from app.models.rule import Rule, rule_conditions
from app.schemas.rule import RuleCreate, RuleResponse
from datetime import datetime
from sqlalchemy.exc import IntegrityError


def create_rule(db: Session, rule: RuleCreate) -> RuleResponse:
    # Create the rule without conditions first
    rule_data = rule.dict(exclude={'conditions'})

    # Try to create the rule, if name exists, append timestamp
    try:
        db_rule = Rule(**rule_data)
        db.add(db_rule)
        db.flush()
    except IntegrityError:
        # If name exists, append timestamp to make it unique
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        rule_data['name'] = f"{rule_data['name']}_{timestamp}"
        db_rule = Rule(**rule_data)
        db.add(db_rule)
        db.flush()

    # Add conditions
    for condition in rule.conditions:
        stmt = rule_conditions.insert().values(
            rule_id=db_rule.id,
            condition_type_id=condition.condition_type_id,
            value=condition.value,
            year=condition.year
        )
        db.execute(stmt)

    db.commit()
    db.refresh(db_rule)
    return db_rule


def get_rules(db: Session, skip: int = 0, limit: int = 100):
    rules = db.query(Rule).offset(skip).limit(limit).all()
    result = []

    for rule in rules:
        # Get conditions for each rule
        conditions = db.query(rule_conditions).filter(
            rule_conditions.c.rule_id == rule.id).all()
        rule_dict = {
            "id": rule.id,
            "name": rule.name,
            "description": rule.description,
            "is_active": rule.is_active,
            "created_at": rule.created_at,
            "updated_at": rule.updated_at,
            "action": rule.action,
            "action_description": rule.action_description,
            "conditions": [
                {
                    "condition_type_id": c.condition_type_id,
                    "value": c.value,
                    "year": c.year
                }
                for c in conditions
            ]
        }
        result.append(rule_dict)

    return result
