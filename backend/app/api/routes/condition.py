from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.schemas.condition import ConditionTypeResponse
from app.models.condition import ConditionType
from app.database import get_db
import logging

router = APIRouter()
logger = logging.getLogger(__name__)


@router.get("/condition-types", response_model=list[ConditionTypeResponse])
def get_condition_types(db: Session = Depends(get_db)):
    try:
        logger.info("Fetching condition types from database")
        conditions = db.query(ConditionType).all()
        logger.info(f"Found {len(conditions)} condition types")
        return conditions
    except Exception as e:
        logger.error(f"Error fetching condition types: {str(e)}")
        raise HTTPException(
            status_code=500, detail=f"Database error: {str(e)}")
