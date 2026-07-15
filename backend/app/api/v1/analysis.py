from typing import Any

from fastapi import APIRouter, Depends, HTTPException, status
from pydantic import BaseModel
from sqlalchemy.orm import Session

from app.db.session import get_db
from app.services.analysis_service import AnalysisService
from app.repositories.analysis_repository import AnalysisRepository

router = APIRouter(prefix="/analysis", tags=["analysis"])


class AnalyzeRequest(BaseModel):
    text: str


class HistoryResponse(BaseModel):
    id: int
    caption: str
    sentiment: str | None
    content_quality_score: int
    virality_prediction: str
    readability_score: int
    created_at: str


def get_analysis_service(db: Session = Depends(get_db)) -> AnalysisService:
    repository = AnalysisRepository(db)
    return AnalysisService(repository)


@router.post("", status_code=status.HTTP_200_OK)
def analyze(payload: AnalyzeRequest, service: AnalysisService = Depends(get_analysis_service)) -> dict[str, Any]:
    if not payload.text.strip():
        raise HTTPException(status_code=400, detail="Text cannot be empty")
    return service.analyze_caption(text=payload.text)


@router.get("/history", response_model=list[HistoryResponse])
def history(service: AnalysisService = Depends(get_analysis_service)) -> list[HistoryResponse]:
    return service.list_history(user_id=1)
