from typing import Any

from sqlalchemy.orm import Session

from app.models import Project, SavedReport, User


class WorkspaceService:
    def __init__(self, session: Session):
        self.session = session

    def create_project(self, *, user: User, name: str, description: str | None = None) -> dict[str, Any]:
        project = Project(user_id=user.id, name=name, description=description)
        self.session.add(project)
        self.session.commit()
        self.session.refresh(project)
        return {"id": project.id, "name": project.name, "description": project.description}

    def list_projects(self, user: User) -> list[dict[str, Any]]:
        return [
            {"id": project.id, "name": project.name, "description": project.description, "created_at": project.created_at.isoformat()}
            for project in self.session.query(Project).filter(Project.user_id == user.id).order_by(Project.created_at.desc()).all()
        ]

    def save_report(self, *, user: User, title: str, analysis_id: int, summary: str) -> dict[str, Any]:
        report = SavedReport(user_id=user.id, title=title, analysis_id=analysis_id, summary=summary)
        self.session.add(report)
        self.session.commit()
        self.session.refresh(report)
        return {"id": report.id, "title": report.title, "analysis_id": report.analysis_id, "summary": report.summary}

    def list_saved_reports(self, user: User) -> list[dict[str, Any]]:
        return [
            {"id": report.id, "title": report.title, "analysis_id": report.analysis_id, "summary": report.summary, "created_at": report.created_at.isoformat()}
            for report in self.session.query(SavedReport).filter(SavedReport.user_id == user.id).order_by(SavedReport.created_at.desc()).all()
        ]
