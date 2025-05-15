import re
from typing import List
from sqlalchemy.orm import Session
from app.models.rule import Rule, rule_conditions
from app.schemas.application import ApplicationCreate
from app.models.application import Application
from app.models.evaluation import Evaluation
from app.models.condition import ConditionType
from datetime import datetime


class RuleEngine:
    def __init__(self, db: Session):
        self.db = db

    def evaluate_application(self, application_record: Application, application_data: ApplicationCreate) -> List[Evaluation]:
        applicable_evaluations = []
        rules = self.db.query(Rule).filter(Rule.is_active == True).all()

        for rule in rules:
            if self.evaluate_rule_conditions(application_data, rule):
                # Create document request
                evaluation = Evaluation(
                    application_id=application_record.id,
                    rule_id=rule.id,
                    action_taken=f"Request document: {rule.action}",
                    evaluated_at=datetime.utcnow()
                )
                self.db.add(evaluation)
                applicable_evaluations.append(evaluation)

        self.db.commit()
        return applicable_evaluations

    def evaluate_rule_conditions(self, application: ApplicationCreate, rule: Rule) -> bool:
        # Get all conditions for this rule with their values
        rule_condition_values = self.db.query(rule_conditions).filter(
            rule_conditions.c.rule_id == rule.id
        ).all()

        for condition_value in rule_condition_values:
            condition_type = self.db.query(ConditionType).get(
                condition_value.condition_type_id)
            if not self.evaluate_condition(application, condition_type, condition_value.value, condition_value.year):
                return False
        return True

    def evaluate_condition(self, application: ApplicationCreate, condition_type: ConditionType, value: str, year: int = None) -> bool:
        try:
            if condition_type.data_type == "boolean":
                return getattr(application, condition_type.field) == (value.lower() == "true")
            elif condition_type.data_type == "enum":
                return getattr(application, condition_type.field).lower() == value.lower()
            elif condition_type.data_type == "year_boolean":
                if year is None:
                    return False
                return (not getattr(application, condition_type.field)) and getattr(application, condition_type.year_field) == year
            return False
        except Exception as e:
            print(f"Error evaluating condition: {e}")
            return False
