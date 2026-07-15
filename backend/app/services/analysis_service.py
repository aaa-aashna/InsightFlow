from __future__ import annotations

from typing import Any, Dict, Optional

from app.ai.sentiment import analyze_caption
from app.repositories.analysis_repository import AnalysisRepository


class AnalysisService:
    def __init__(self, repository: AnalysisRepository):
        self.repository = repository

    def analyze_caption(self, *, text: str, user_id: Optional[int] = None) -> Dict[str, Any]:
        result = analyze_caption(text)
        analysis = self.repository.create(
            caption=text,
            sentiment=result.get("sentiment", "neutral"),
            content_quality_score=int(result.get("content_quality_score", 0)),
            virality_prediction=result.get("virality_prediction", "medium"),
            readability_score=int(result.get("readability_score", 0)),
            user_id=user_id,
        )
        payload = dict(result)
        payload["analysis_id"] = analysis.id
        return payload

    def list_history(self, user_id: int) -> list[dict[str, Any]]:
        analyses = self.repository.list_for_user(user_id)
        return [
            {
                "id": analysis.id,
                "caption": analysis.caption,
                "sentiment": analysis.sentiment,
                "content_quality_score": analysis.content_quality_score,
                "virality_prediction": analysis.virality_prediction,
                "readability_score": analysis.readability_score,
                "created_at": analysis.created_at.isoformat(),
            }
            for analysis in analyses
        ]
