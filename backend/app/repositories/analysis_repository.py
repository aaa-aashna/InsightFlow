from typing import List, Optional

from sqlalchemy.orm import Session

from app.models import AnalysisResult


class AnalysisRepository:
    def __init__(self, session: Session):
        self.session = session

    def create(self, *, caption: str, sentiment: str, content_quality_score: int, virality_prediction: str, readability_score: int, user_id: Optional[int] = None) -> AnalysisResult:
        analysis = AnalysisResult(
            caption=caption,
            sentiment=sentiment,
            content_quality_score=content_quality_score,
            virality_prediction=virality_prediction,
            readability_score=readability_score,
            user_id=user_id,
        )
        self.session.add(analysis)
        self.session.commit()
        self.session.refresh(analysis)
        return analysis

    def list_for_user(self, user_id: int) -> List[AnalysisResult]:
        return self.session.query(AnalysisResult).filter(AnalysisResult.user_id == user_id).order_by(AnalysisResult.created_at.desc()).all()
