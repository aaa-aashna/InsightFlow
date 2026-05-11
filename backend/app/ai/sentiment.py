from transformers import pipeline

classifier = pipeline(
    "sentiment-analysis",
    model="distilbert-base-uncased-finetuned-sst-2-english"
)

def analyze_caption(text: str):
    result = classifier(text)[0]

    label = result["label"]
    score = round(result["score"], 4)

    hashtags = [word for word in text.split() if word.startswith("#")]

    virality_score = 50
    engagement_score = 50

    # Sentiment scoring
    if label == "POSITIVE":
        virality_score += 20
        engagement_score += 25
        engagement = "High engagement potential"
    else:
        engagement_score -= 10
        engagement = "Moderate engagement potential"

    # Hook analysis
    if len(text.split()) > 8:
        hook_strength = "Strong"
        hook_score = min(100, 70 + (len(text.split()) * 2))
        virality_score += 10
        engagement_score += 10
    else:
        hook_strength = "Weak"
        hook_score = 40
        engagement_score -= 10

    # Hashtag analysis
    if len(hashtags) >= 3:
        hashtag_quality = "Good hashtag strategy"
        virality_score += 10
        engagement_score += 15
    elif len(hashtags) > 0:
        hashtag_quality = "Relevant niche hashtags detected"
        virality_score += 5
        engagement_score += 5
    else:
        hashtag_quality = "No hashtags detected"

    virality_score = min(100, max(0, virality_score))
    engagement_score = min(100, max(0, engagement_score))
    hook_score = min(100, max(0, hook_score))

    # Creator suggestions
    if virality_score >= 80:
        suggestion = "Strong content structure. Ready for posting."
    elif virality_score >= 60:
        suggestion = "Improve the opening hook for better retention."
    else:
        suggestion = "Add more emotional storytelling."

    # Generate trend data based on virality_score
    base_reach = virality_score * 100
    base_eng = engagement_score * 50
    
    import random
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
    if label == "POSITIVE":
        recommended_hashtags[1] = {"name": "#inspiration", "score": 88, "color": "#3b82f6"}

    return {
        "sentiment": label,
        "confidence": score,
        "engagement_prediction": engagement,
        "engagement_score": engagement_score,
        "hook_strength": hook_strength,
        "hook_score": hook_score,
        "hashtag_quality": hashtag_quality,
        "virality_score": virality_score,
        "creator_suggestion": suggestion,
        "trend_data": trend_data,
        "recommended_hashtags": recommended_hashtags
    }