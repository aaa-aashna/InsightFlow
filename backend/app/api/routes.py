from fastapi import APIRouter
from pydantic import BaseModel

from app.ai.sentiment import analyze_caption
from app.ai.rewriter import (
    make_more_viral, improve_hook, generate_cta,
    add_emotional_impact, make_more_relatable, increase_engagement, generate_better_hashtags
)

router = APIRouter()

class TextRequest(BaseModel):
    text: str

@router.get("/")
def home():
    return {"message": "API working"}

@router.post("/analyze")
def analyze(data: TextRequest):
    return analyze_caption(data.text)

@router.post("/rewrite/viral")
def rewrite_viral(data: TextRequest):
    return {"caption": make_more_viral(data.text)}

@router.post("/rewrite/hook")
def rewrite_hook(data: TextRequest):
    return {"caption": improve_hook(data.text)}

@router.post("/rewrite/cta")
def rewrite_cta(data: TextRequest):
    return {"caption": generate_cta(data.text)}

@router.post("/rewrite/emotion")
def rewrite_emotion(data: TextRequest):
    return {"caption": add_emotional_impact(data.text)}

@router.post("/rewrite/relatable")
def rewrite_relatable(data: TextRequest):
    return {"caption": make_more_relatable(data.text)}

@router.post("/rewrite/engage")
def rewrite_engage(data: TextRequest):
    return {"caption": increase_engagement(data.text)}

@router.post("/rewrite/hashtags")
def rewrite_hashtags(data: TextRequest):
    return {"caption": generate_better_hashtags(data.text)}