from fastapi import APIRouter, Depends, Body
from sqlalchemy.orm import Session
from app.models.application import Application
from app.schemas.application import ApplicationCreate, ApplicationResponse
from app.database import get_db
from app.models.application import Application
from app.schemas.application import ApplicationCreate, ApplicationResponse
from app.services.rule_engine import RuleEngine
from typing import List, Union
from pydantic import BaseModel


class ConditionMatch(BaseModel):
    field: str
    value: str
    year: Union[int, None] = None


class MatchCountRequest(BaseModel):
    conditions: List[ConditionMatch]


router = APIRouter()


@router.post("/applications", response_model=ApplicationResponse)
def submit_application(app_data: ApplicationCreate, db: Session = Depends(get_db)):
    application = Application(**app_data.model_dump())
    db.add(application)
    db.commit()
    db.refresh(application)

    # trigger rule engine
    engine = RuleEngine(db)
    actions = engine.evaluate_application(
        application_record=application, application_data=app_data)

    # Trigger document requests based on actions
    for action in actions:
        print(f"Triggered document request for action: {action}")
        # In production, you would enqueue a task or call an external service here.

    return application


@router.post("/applicants/match-count")
def count_matching_applicants(request: MatchCountRequest, db: Session = Depends(get_db)):
    """
    Count the number of applicants that match the given conditions.
    Each condition should have: field, value, and optionally year
    """
    query = db.query(Application)

    for condition in request.conditions:
        if condition.field == "family_status":
            query = query.filter(Application.family_status == condition.value)
        elif condition.field == "business_owner":
            query = query.filter(Application.business_owner == (
                condition.value.lower() == "true"))
        elif condition.field == "filed_us_taxes":
            if condition.year is not None:
                query = query.filter(
                    Application.filed_us_taxes == (
                        condition.value.lower() == "true"),
                    Application.tax_year == condition.year
                )
            else:
                query = query.filter(Application.filed_us_taxes == (
                    condition.value.lower() == "true"))

    count = query.count()
    return {"count": count}
