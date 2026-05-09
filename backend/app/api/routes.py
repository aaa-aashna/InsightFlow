from fastapi import APIRouter
from pydantic import BaseModel

from app.ai.sentiment import analyze_caption

router = APIRouter()

class TextRequest(BaseModel):
    text: str

@router.get("/")
def home():
    return {"message": "API working"}

@router.post("/analyze")
def analyze(data: TextRequest):
    return analyze_caption(data.text)