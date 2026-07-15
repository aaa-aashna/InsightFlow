import random
import re

def make_more_viral(text: str) -> str:
    """Enhances text with viral triggers and urgency."""
    viral_phrases = [
        "This changes everything. ",
        "Stop scrolling and read this! ",
        "The secret nobody tells you:",
        "I can't believe I'm sharing this for free ",
    ]
    prefix = random.choice(viral_phrases)
    
    # Capitalize the first letter of the original text if it's not
    if text:
        text = text[0].upper() + text[1:]
    
    return f"{prefix}\n\n{text}"

def improve_hook(text: str) -> str:
    """Replaces the first sentence with an attention-grabbing hook."""
    sentences = re.split(r'(?<=[.!?]) +', text.strip())
    
    hooks = [
        "Want to 10x your growth this year?",
        "If you're still doing this, you're losing out.",
        "Here is the ultimate cheat code:",
        "Don't make this simple mistake..."
    ]
    new_hook = random.choice(hooks)
    
    if len(sentences) > 1:
        rest_of_text = " ".join(sentences[1:])
        return f"{new_hook} {rest_of_text}"
    else:
        return f"{new_hook}\n\n{text}"

def generate_cta(text: str) -> str:
    """Appends a high-converting call to action."""
    ctas = [
        "👇 Drop a 🔥 in the comments if you agree!",
        "Save this post for later so you don't lose it! 📌",
        "Tag a friend who needs to see this! 🗣️",
        "Click the link in my bio to learn more! 🔗"
    ]
    cta = random.choice(ctas)
    
    return f"{text}\n\n{cta}"

def add_emotional_impact(text: str) -> str:
    """Injects emotional adjectives to increase intensity."""
    emotional_words = ["incredible", "heartbreaking", "mind-blowing", "unreal", "powerful"]
    word = random.choice(emotional_words)
    return f"This is absolutely {word}. {text}"

def make_more_relatable(text: str) -> str:
    """Makes the tone more casual and relatable."""
    phrases = [
        "We've all been there...",
        "Am I the only one who does this?",
        "Real talk:",
        "Let's be honest for a second."
    ]
    phrase = random.choice(phrases)
    return f"{phrase}\n{text}"

def increase_engagement(text: str) -> str:
    """Adds an engaging question or poll to the text."""
    questions = [
        "\n\nWhat do you guys think? Let me know ",
        "\n\nHave you ever experienced this?",
        "\n\nAgree or disagree? Drop a comment! "
    ]
    return f"{text}{random.choice(questions)}"

def generate_better_hashtags(text: str) -> str:
    """Appends trending niche hashtags based on content length."""
    tags = "\n\n#viral #fyp #creator #tips #growth #mindset"
    return f"{text}{tags}"
