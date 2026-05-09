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

    # Sentiment scoring
    if label == "POSITIVE":
        virality_score += 20
        engagement = "High engagement potential"
    else:
        engagement = "Moderate engagement potential"

    # Hook analysis
    if len(text.split()) > 8:
        hook_strength = "Strong"
        virality_score += 10
    else:
        hook_strength = "Weak"

    # Hashtag analysis
    if len(hashtags) >= 3:
        hashtag_quality = "Good hashtag strategy"
        virality_score += 10
    elif len(hashtags) > 0:
        hashtag_quality = "Relevant niche hashtags detected"
        virality_score += 5
    else:
        hashtag_quality = "No hashtags detected"

    virality_score = min(100, max(0, virality_score))

    # Creator suggestions
    if virality_score >= 80:
        suggestion = "Strong content structure. Ready for posting."
    elif virality_score >= 60:
        suggestion = "Improve the opening hook for better retention."
    else:
        suggestion = "Add more emotional storytelling."

    return {
        "sentiment": label,
        "confidence": score,
        "engagement_prediction": engagement,
        "hook_strength": hook_strength,
        "hashtag_quality": hashtag_quality,
        "virality_score": virality_score,
        "creator_suggestion": suggestion
    }