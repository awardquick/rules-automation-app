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
        print("\nQuerying for active rules...")
        rules = self.db.query(Rule).filter(Rule.is_active == True).all()
        print(f"Found {len(rules)} active rules")
        print(f"Rules: {rules}")

        for rule in rules:
            print(f"\nEvaluating rule: {rule.name}")
            if self.evaluate_rule_conditions(application_data, rule):
                print(f"Rule {rule.name} matched")
                # Create document request
                evaluation = Evaluation(
                    application_id=application_record.id,
                    rule_id=rule.id,
                    action_taken=f"Request document: {rule.action}",
                    evaluated_at=datetime.utcnow()
                )
                self.db.add(evaluation)
                applicable_evaluations.append(evaluation)
            else:
                print(f"Rule {rule.name} did not match")

        self.db.commit()
        return applicable_evaluations

    def evaluate_rule_conditions(self, application: ApplicationCreate, rule: Rule) -> bool:
        # Get all conditions for this rule with their values
        rule_condition_values = self.db.query(rule_conditions).filter(
            rule_conditions.c.rule_id == rule.id
        ).all()
        print(
            f"Found {len(rule_condition_values)} conditions for rule {rule.name}")

        for condition_value in rule_condition_values:
            print(
                f"\nEvaluating condition: rule_id={condition_value.rule_id}, type_id={condition_value.condition_type_id}, value={condition_value.value}, year={condition_value.year}")
            condition_type = self.db.query(ConditionType).get(
                condition_value.condition_type_id)
            print(
                f"Condition type: {condition_type.name} ({condition_type.data_type})")
            if self.evaluate_condition(application, condition_type, condition_value.value, condition_value.year):
                print(f"Condition did not match")
                return True
            print(f"Condition matched")
        return False

    def evaluate_condition(self, application: ApplicationCreate, condition_type: ConditionType, value: str, year: int = None) -> bool:
        try:
            if condition_type.data_type == "boolean":
                result = getattr(application, condition_type.field) == (
                    value.lower() == "true")
                print(
                    f"Boolean evaluation: {getattr(application, condition_type.field)} == {value.lower() == 'true'} = {result}")
                return result
            elif condition_type.data_type == "enum":
                result = getattr(
                    application, condition_type.field).lower() == value.lower()
                print(
                    f"Enum evaluation: {getattr(application, condition_type.field).lower()} == {value.lower()} = {result}")
                return result
            elif condition_type.data_type == "year_boolean":
                if year is None:
                    print("Year boolean evaluation failed: year is None")
                    return False
                result = (not getattr(application, condition_type.field)) and getattr(
                    application, condition_type.year_field) == year
                print(
                    f"Year boolean evaluation: not {getattr(application, condition_type.field)} and {getattr(application, condition_type.year_field)} == {year} = {result}")
                return result
            print(f"Unknown data type: {condition_type.data_type}")
            return False
        except Exception as e:
            print(f"Error evaluating condition: {e}")
            return False
