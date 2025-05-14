from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.database import get_db
from app.models.application import Application
from app.schemas.application import ApplicationCreate, ApplicationResponse
from app.models.evaluation import Evaluation
from app.schemas.evaluation import EvaluationResponse
from app.services.rule_engine import RuleEngine
from app.schemas.rule import RuleCreate, RuleResponse
from app.crud.rule import create_rule

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


@router.get("/evaluations/{application_id}", response_model=[EvaluationResponse])
def get_evaluations(application_id: int, db: Session = Depends(get_db)):
    evaluations = db.query(Evaluation).filter(
        Evaluation.application_id == application_id).all()
    return evaluations


@router.post("/rules", response_model=RuleResponse)
def create_rule(rule_data: RuleCreate, db: Session = Depends(get_db)):
    return create_rule(db, rule_data)
