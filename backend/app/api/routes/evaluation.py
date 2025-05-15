from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.models.evaluation import Evaluation
from app.schemas.evaluation import EvaluationResponse
from app.database import get_db

router = APIRouter(prefix="/api/v1", tags=["evaluations"])


@router.get("/evaluations/{application_id}", response_model=list[EvaluationResponse])
def get_evaluations(application_id: int, db: Session = Depends(get_db)):
    evaluations = db.query(Evaluation).filter(
        Evaluation.application_id == application_id).all()
    return evaluations
