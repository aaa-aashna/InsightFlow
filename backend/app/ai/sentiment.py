import random
import re
from transformers import pipeline

# We keep the pipeline loaded to use as a baseline sentiment signal
classifier = pipeline(
    "sentiment-analysis",
    model="distilbert-base-uncased-finetuned-sst-2-english"
)

def analyze_caption(text: str):
    if not text.strip():
        text = "This is a default test caption."

    result = classifier(text)[0]
    label = result["label"]
    confidence = round(result["score"], 4)

    # Basic extractions
    words = text.split()
    word_count = len(words)
    sentences = re.split(r'[.!?]+', text)
    sentences = [s.strip() for s in sentences if s.strip()]
    sentence_count = len(sentences) if sentences else 1
    hashtags = [w for w in words if w.startswith("#")]
    emojis = len(re.findall(r'[^\w\s,\.\!\?\#\:\-\_\"\'\(\)]', text))

    # Heuristic 1: Readability (pacing, sentence length)
    avg_words_per_sentence = word_count / sentence_count
    if 5 <= avg_words_per_sentence <= 15:
        readability_score = 90
    elif avg_words_per_sentence < 5:
        readability_score = 70 # Too choppy
    else:
        readability_score = max(30, 100 - (avg_words_per_sentence * 2))

    # Heuristic 2: Emotional Intensity
    emotional_words = ["love", "hate", "crazy", "unbelievable", "secret", "fail", "win", "best", "worst", "amazing", "stop", "never", "always"]
    emotion_count = sum(1 for w in words if w.lower().strip(',.!') in emotional_words)
    emotion_score = min(100, 40 + (emotion_count * 15) + (emojis * 5))
    if label == "POSITIVE":
        emotion_score = min(100, emotion_score + 10)

    # Heuristic 3: Hook Strength (First sentence analysis)
    first_sentence = sentences[0] if sentences else ""
    first_sentence_words = len(first_sentence.split())
    hook_score = 50
    if 3 <= first_sentence_words <= 10:
        hook_score += 20 # Punchy hook
    if "?" in first_sentence or "!" in first_sentence:
        hook_score += 15
    if any(w in first_sentence.lower() for w in ["stop", "you", "secret", "how", "why"]):
        hook_score += 15

    # Heuristic 4: CTA Presence (Last sentence analysis)
    last_sentence = sentences[-1] if len(sentences) > 1 else text
    cta_score = 30
    if "?" in last_sentence:
        cta_score += 30
    if any(w in text.lower() for w in ["comment", "link", "bio", "save", "share", "tag", "drop", "below"]):
        cta_score += 40

    # Heuristic 5: Discoverability (Hashtags)
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

    # Category & Tone Classification
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

    # Aggregate Scores
    virality_score = int((hook_score * 0.3) + (emotion_score * 0.2) + (cta_score * 0.2) + (discoverability_score * 0.15) + (readability_score * 0.15))
    engagement_score = int((cta_score * 0.4) + (emotion_score * 0.4) + (readability_score * 0.2))
    retention_score = int((hook_score * 0.6) + (readability_score * 0.4))

    # Explanations
    explanations = []
    if hook_score >= 80:
        explanations.append("High retention expected due to a punchy, curiosity-driven hook.")
    else:
        explanations.append("Weak opening may cause viewers to scroll past. Consider adding a bold claim or question.")

    if emotion_score >= 80:
        explanations.append("Strong emotional resonance detected. This increases likelihood of shares and saves.")
        
    if cta_score < 50:
        explanations.append("Missing a clear Call-To-Action. Tell your audience exactly what to do next.")
    else:
        explanations.append("Excellent CTA structure encourages direct audience interaction.")

    explanation_text = " ".join(explanations)

    # Formatting Radar Data
    radar_data = [
        {"metric": "Hook", "A": hook_score, "fullMark": 100},
        {"metric": "Emotion", "A": emotion_score, "fullMark": 100},
        {"metric": "Readability", "A": readability_score, "fullMark": 100},
        {"metric": "CTA", "A": cta_score, "fullMark": 100},
        {"metric": "Discovery", "A": discoverability_score, "fullMark": 100},
    ]

    # Generate trend data based on virality_score
    base_reach = virality_score * 150
    base_eng = engagement_score * 80
    days = ["Mon", "Tue", "Wed", "Thu", "Fri", "Sat", "Sun"]
    trend_data = []
    for day in days:
        trend_data.append({
            "day": day,
            "reach": int(base_reach * random.uniform(0.8, 1.2)),
            "engagement": int(base_eng * random.uniform(0.8, 1.2))
        })

    # Recommended hashtags
    recommended_hashtags = [
        {"name": "#viral", "score": 98, "color": "#a855f7"},
        {"name": "#fyp", "score": 85, "color": "#3b82f6"},
        {"name": "#trending", "score": 75, "color": "#22c55e"}
    ]

    return {
        "sentiment": label,
        "confidence": confidence,
        "content_category": category,
        "creator_tone": tone,
        "engagement_prediction": "High" if engagement_score > 75 else "Moderate",
        "engagement_score": engagement_score,
        "hook_strength": "Strong" if hook_score > 75 else "Weak",
        "hook_score": hook_score,
        "retention_score": retention_score,
        "hashtag_quality": hashtag_quality,
        "virality_score": virality_score,
        "creator_suggestion": explanations[0] if explanations else "Content structure looks decent.",
        "detailed_explanation": explanation_text,
        "radar_data": radar_data,
        "trend_data": trend_data,
        "recommended_hashtags": recommended_hashtags
    }