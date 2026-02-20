# ai_engine.py - multi-tone with intensity ranking

from textblob import TextBlob
from collections import Counter

# Basic emotion mapping
emotion_dict = {
    "happy": ["happy", "joy", "glad", "delighted", "excited", "amazing", "awesome"],
    "sad": ["sad", "unhappy", "depressed", "disappointed", "down"],
    "angry": ["angry", "mad", "furious", "hate", "unacceptable"],
    "fear": ["fear", "scared", "nervous", "worried", "anxious"],
    "surprise": ["surprise", "shocked", "amazed", "wow"],
    "disgust": ["disgust", "gross", "nasty", "hate"],
}

# Tone dictionary for contextual tone
tone_dict = {
    "angry": ["angry", "hate", "unacceptable", "furious", "mad"],
    "excited": ["excited", "thrilled", "amazing", "awesome", "!"],
    "frustrated": ["frustrated", "annoyed", "upset", "disappointed"],
    "polite": ["please", "thank you", "kindly", "appreciate"],
    "sarcastic": ["yeah right", "sure", "great..."],
    "neutral": []
}


def analyze_text(text: str):
    """
    Analyze text and return multiple detected emotions and tones with intensity ranking.
    """
    blob = TextBlob(text)
    polarity = blob.sentiment.polarity
    subjectivity = blob.sentiment.subjectivity

    words = text.lower().split()

    # 1️⃣ Emotion detection with counts for intensity
    emotion_counts = Counter()
    for emotion, keywords in emotion_dict.items():
        for kw in keywords:
            if kw in words:
                emotion_counts[emotion] += 1

    # Add polarity influence
    if polarity > 0.3:
        emotion_counts["happy"] += int(polarity * 2)
    elif polarity < -0.3:
        emotion_counts["sad"] += int(-polarity * 2)

    # Sort emotions by intensity
    ranked_emotions = [e for e, _ in emotion_counts.most_common()]
    if not ranked_emotions:
        ranked_emotions = ["neutral"]

    # 2️⃣ Tone detection with counts
    tone_counts = Counter()
    for tone, keywords in tone_dict.items():
        for kw in keywords:
            if kw in text.lower():
                tone_counts[tone] += 1

    # Sort tones by intensity
    ranked_tones = [t for t, _ in tone_counts.most_common()]
    if not ranked_tones:
        ranked_tones = ["neutral"]

    # Primary sentiment is the top-ranked emotion
    primary_sentiment = ranked_emotions[0] if ranked_emotions else "neutral"

    return {
        "summary": text,
        "sentiment": primary_sentiment,
        "emotions": ranked_emotions,
        "tones": ranked_tones,
        "polarity": polarity,
        "subjectivity": subjectivity,
        "intent": "general"
    }


# Quick test
if __name__ == "__main__":
    test_texts = [
        "I am extremely angry but yeah right, that’s just great...",
        "Wow! I am so excited and thrilled!",
        "I feel sad and disappointed about this service.",
        "Thank you so much, I really appreciate it!",
        "I hate this! This is unacceptable and frustrating."
    ]
    for txt in test_texts:
        print(analyze_text(txt))