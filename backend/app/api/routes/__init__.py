from fastapi import APIRouter

from .application import router as application_router
from .condition import router as condition_router
# Add other routers as you split them out:
from .evaluation import router as evaluation_router
from .rule import router as rule_router

api_router = APIRouter()
api_router.include_router(application_router)
api_router.include_router(condition_router)
api_router.include_router(evaluation_router)
api_router.include_router(rule_router)
