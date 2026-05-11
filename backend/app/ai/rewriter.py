import random
import re

def make_more_viral(text: str) -> str:
    """Enhances text with viral triggers and urgency."""
    viral_phrases = [
        "This changes everything. 🤯",
        "Stop scrolling and read this! 🔥",
        "The secret nobody tells you:",
        "I can't believe I'm sharing this for free 🚀",
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
