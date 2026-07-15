import random
import re

from transformers import pipeline

# Load once and reuse the model across requests.
classifier = pipeline(
    "sentiment-analysis",
    model="distilbert-base-uncased-finetuned-sst-2-english",
)


def analyze_caption(text: str) -> dict[str, object]:
    if not text or not text.strip():
        text = "This is a default test caption."

    result = classifier(text)[0]
    label = result["label"]
    confidence = round(result["score"], 4)

    words = text.split()
    word_count = len(words)
    sentences = re.split(r"[.!?]+", text)
    sentences = [s.strip() for s in sentences if s.strip()]
    sentence_count = len(sentences) if sentences else 1
    hashtags = [w for w in words if w.startswith("#")]
    emojis = len(re.findall(r"[^\w\s,\.\!\?\#\:\-\_\"\'\(\)]", text))

    avg_words_per_sentence = word_count / sentence_count
    if 5 <= avg_words_per_sentence <= 15:
        readability_score = 90
    elif avg_words_per_sentence < 5:
        readability_score = 70
    else:
        readability_score = max(30, 100 - (avg_words_per_sentence * 2))

    emotional_words = ["love", "hate", "crazy", "unbelievable", "secret", "fail", "win", "best", "worst", "amazing", "stop", "never", "always"]
    emotion_count = sum(1 for w in words if w.lower().strip(",.!") in emotional_words)
    emotion_score = min(100, 40 + (emotion_count * 15) + (emojis * 5))
    if label == "POSITIVE":
        emotion_score = min(100, emotion_score + 10)

    first_sentence = sentences[0] if sentences else ""
    first_sentence_words = len(first_sentence.split())
    hook_score = 50
    if 3 <= first_sentence_words <= 10:
        hook_score += 20
    if "?" in first_sentence or "!" in first_sentence:
        hook_score += 15
    if any(w in first_sentence.lower() for w in ["stop", "you", "secret", "how", "why"]):
        hook_score += 15

    last_sentence = sentences[-1] if len(sentences) > 1 else text
    cta_score = 30
    if "?" in last_sentence:
        cta_score += 30
    if any(w in text.lower() for w in ["comment", "link", "bio", "save", "share", "tag", "drop", "below"]):
        cta_score += 40

    if len(hashtags) >= 3 and len(hashtags) <= 8:
        discoverability_score = 95
        hashtag_quality = "Optimal niche targeting"
    elif len(hashtags) > 8:
        discoverability_score = 60
        hashtag_quality = "Potential hashtag stuffing"
    elif len(hashtags) > 0:
        discoverability_score = 75
        hashtag_quality = "Needs more niche tags"
    else:
        discoverability_score = 20
        hashtag_quality = "No hashtags detected"

    text_lower = text.lower()
    if any(w in text_lower for w in ["learn", "how to", "step", "tutorial", "guide"]):
        category = "Educational"
        tone = "Authoritative & Informative"
    elif any(w in text_lower for w in ["mindset", "grind", "success", "never give up", "consistent"]):
        category = "Motivational"
        tone = "Inspiring & Uplifting"
    elif any(w in text_lower for w in ["buy", "sale", "discount", "offer"]):
        category = "Promotional"
        tone = "Sales-oriented"
    elif emotion_score > 75:
        category = "Storytelling"
        tone = "Emotional & Raw"
    else:
        category = "General/Lifestyle"
        tone = "Casual & Conversational"

    virality_score = int((hook_score * 0.3) + (emotion_score * 0.2) + (cta_score * 0.2) + (discoverability_score * 0.15) + (readability_score * 0.15))
    engagement_score = int((cta_score * 0.4) + (emotion_score * 0.4) + (readability_score * 0.2))
    retention_score = int((hook_score * 0.6) + (readability_score * 0.4))

    if virality_score >= 80:
        virality_prediction = "high"
    elif virality_score >= 55:
        virality_prediction = "medium"
    else:
        virality_prediction = "low"

    content_quality_score = min(100, int((readability_score * 0.4) + (hook_score * 0.3) + (cta_score * 0.2) + (emotion_score * 0.1)))

    recommended_hashtags = [
        {"name": "#creator", "score": 90, "color": "#a855f7"},
        {"name": "#growth", "score": 82, "color": "#3b82f6"},
        {"name": "#marketing", "score": 76, "color": "#22c55e"},
    ]

    return {
        "sentiment": label,
        "confidence": confidence,
        "content_category": category,
        "creator_tone": tone,
        "content_quality_score": content_quality_score,
        "engagement_prediction": "High" if engagement_score > 75 else "Moderate",
        "engagement_score": engagement_score,
        "hook_strength": "Strong" if hook_score > 75 else "Weak",
        "hook_score": hook_score,
        "retention_score": retention_score,
        "readability_score": readability_score,
        "hashtag_quality": hashtag_quality,
        "virality_prediction": virality_prediction,
        "virality_score": virality_score,
        "recommended_hashtags": recommended_hashtags,
    }
