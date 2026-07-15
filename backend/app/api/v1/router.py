from fastapi import APIRouter

from app.api.v1.analysis import router as analysis_router
from app.api.v1.auth import router as auth_router
from app.api.v1.workspace import router as workspace_router

router = APIRouter(prefix="/api/v1")
router.include_router(auth_router)
router.include_router(analysis_router)
router.include_router(workspace_router)
