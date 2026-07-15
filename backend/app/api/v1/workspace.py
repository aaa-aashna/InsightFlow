from fastapi import APIRouter, Depends
from pydantic import BaseModel
from sqlalchemy.orm import Session

from app.api.dependencies import CurrentUser
from app.db.session import get_db
from app.models import User
from app.services.workspace_service import WorkspaceService

router = APIRouter(prefix="/workspace", tags=["workspace"])


class ProjectCreateRequest(BaseModel):
    name: str
    description: str | None = None


class ReportCreateRequest(BaseModel):
    title: str
    analysis_id: int
    summary: str


def get_workspace_service(db: Session = Depends(get_db)) -> WorkspaceService:
    return WorkspaceService(db)


@router.post("/projects")
def create_project(payload: ProjectCreateRequest, user: CurrentUser, service: WorkspaceService = Depends(get_workspace_service)):
    return service.create_project(user=user, name=payload.name, description=payload.description)


@router.get("/projects")
def list_projects(user: CurrentUser, service: WorkspaceService = Depends(get_workspace_service)):
    return service.list_projects(user)


@router.post("/reports")
def save_report(payload: ReportCreateRequest, user: CurrentUser, service: WorkspaceService = Depends(get_workspace_service)):
    return service.save_report(user=user, title=payload.title, analysis_id=payload.analysis_id, summary=payload.summary)


@router.get("/reports")
def list_reports(user: CurrentUser, service: WorkspaceService = Depends(get_workspace_service)):
    return service.list_saved_reports(user)
