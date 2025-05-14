
import re
from typing import List
from sqlalchemy.orm import Session
from models.rule import Rule
from schemas.application import ApplicationCreate
from models.application import Application
from models.evaluation import Evaluation
from datetime import datetime


class RuleEngine:
    def __init__(self, db: Session):
        self.db = db

    def evaluate_application(self, application_record: Application, application_data: ApplicationCreate) -> List[Evaluation]:
        applicable_evaluations = []
        rules = self.db.query(Rule).filter(Rule.is_active == True).all()

        for rule in rules:
            print(f"Evaluating Rule Condition: {rule.condition}")
            if self.evaluate_condition(application_data, rule.condition):
                applicable_evaluations.append(rule.action)

                evaluation = Evaluation(
                    application_id=application_record.id,
                    rule_id=rule.id,
                    action_taken=rule.action,
                    evaluated_at=datetime.utcnow()
                )
                self.db.add(evaluation)
        self.db.commit()
        return applicable_evaluations

    def evaluate_condition(self, application: ApplicationCreate, condition: str) -> bool:
        try:
            condition = condition.lower().strip()

            if condition == "family_status == new":
                return application.family_status.lower() == "new"
            elif condition == "family_status == returning":
                return application.family_status.lower() == "returning"
            elif condition == "business_owner == true":
                return application.business_owner is True
            elif "did not file us taxes in" in condition:
                match = re.search(
                    r"did not file us taxes in (\d{4})", condition)
                if match:
                    year = int(match.group(1))
                    return application.filed_us_taxes is False and application.tax_year == year
                return False
            else:
                return False

        except Exception as e:
            print(f"Error evaluating condition: {e}")
            return False
