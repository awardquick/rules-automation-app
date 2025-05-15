from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.models.application import Application
from app.schemas.application import ApplicationCreate, ApplicationResponse
from app.database import get_db
from app.models.application import Application
from app.schemas.application import ApplicationCreate, ApplicationResponse
from app.services.rule_engine import RuleEngine

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
