import json
import sys
import os

# Ensure the parent directory is in sys.path so 'services' can be imported
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from services.nlp_utils import detect_script_heuristic, get_language_name
from langdetect import detect
from textblob import TextBlob
import speech_recognition as sr
from deep_translator import GoogleTranslator

# -----------------------------
# 1️⃣ Intent Configuration
# -----------------------------
INTENTS = {
    "fraud": ["unauthorized", "fraud", "scam"],
    "refund": ["refund", "money back"],
    "complaint": ["problem", "issue", "not working"],
    "support": ["help", "assist"],
}

# 2️⃣ Core Detection Support
def detect_language(text):
    """
    Hybrid detection for readable language names.
    """
    heuristic = detect_script_heuristic(text)
    if heuristic:
        return get_language_name(heuristic)
    try:
        code = detect(text)
        return get_language_name(code)
    except Exception:
        return "Unknown"

# -----------------------------
# 3️⃣ Emotion Detection
# -----------------------------
def detect_emotion(text):
    text = text.lower()
    if any(word in text for word in ["angry", "frustrated", "upset", "mad"]):
        return "angry"
    elif any(word in text for word in ["happy", "great", "excellent", "satisfied"]):
        return "happy"
    else:
        return "calm"

# -----------------------------
# 4️⃣ Sentiment Detection
# -----------------------------
def detect_sentiment(text):
    polarity = TextBlob(text).sentiment.polarity
    if polarity > 0.2:
        return "positive"
    elif polarity < -0.2:
        return "negative"
    else:
        return "neutral"

# -----------------------------
# 5️⃣ Intent Detection
# -----------------------------
def detect_intent(text):
    text = text.lower()
    for intent, keywords in INTENTS.items():
        for word in keywords:
            if word in text:
                return intent
    return "general inquiry"

# -----------------------------
# 6️⃣ Dual-Language Voice Recognition (ML & EN)
# -----------------------------
def speech_to_text_dual():
    """
    Captures voice input once and detects whether the speaker 
    used English or Malayalam.
    """
    recognizer = sr.Recognizer()

    with sr.Microphone() as source:
        print("🎤 Listening (Speak in English or Malayalam)...")
        recognizer.adjust_for_ambient_noise(source)
        audio = recognizer.listen(source)

    # Path A: Try Malayalam
    try:
        text_ml = recognizer.recognize_google(audio, language="ml-IN")
        # Check if the result actually contains Malayalam script
        if detect_script_heuristic(text_ml) == "mal_Mlym":
            print(f"✅ Detected Malayalam: {text_ml}")
            return text_ml, "Malayalam"
    except:
        text_ml = ""

    # Path B: Try English
    try:
        text_en = recognizer.recognize_google(audio, language="en-IN")
        if text_en.strip():
            print(f"✅ Detected English: {text_en}")
            return text_en, "English"
    except:
        text_en = ""

    print("❌ Could not identify the language or speech")
    return "", "Unknown"

# -----------------------------
# 7️⃣ Translate to English (Only if needed)
# -----------------------------
def translate_to_english(text, source_lang="auto"):
    if not text.strip():
        return ""
        
    try:
        # If we know it's Malayalam, force source to 'ml'
        src = "ml" if source_lang == "Malayalam" else "auto"
        
        translated = GoogleTranslator(source=src, target="en").translate(text)
        print("🌍 English Translation:", translated)
        return translated
    except Exception as e:
        print("❌ Translation error:", e)
        return text

# -----------------------------
# 8️⃣ Main Dual-Language Analyzer
# -----------------------------
def analyze_dual_voice_conversation():
    text, lang = speech_to_text_dual()

    if not text.strip():
        return {"error": "No speech detected"}

    # Translate if Malayalam was detected
    if lang == "Malayalam":
        eng_text = translate_to_english(text, source_lang="Malayalam")
    else:
        eng_text = text # Already English

    sentiment = detect_sentiment(eng_text)
    intent = detect_intent(eng_text)
    emotion = detect_emotion(eng_text)

    return {
        "detected_language": lang,
        "original_text": text,
        "translated_text": eng_text,
        "sentiment": sentiment,
        "intent": intent,
        "emotion": emotion
    }

def analyze_conversation(text):
    """
    General text analysis based on the new logic.
    """
    sentiment = detect_sentiment(text)
    intent = detect_intent(text)
    emotion = detect_emotion(text)
    language = detect_language(text)
    
    return {
        "text": text,
        "language": language,
        "sentiment": sentiment,
        "intent": intent,
        "emotion": emotion
    }

# -----------------------------
# RUN
# -----------------------------
if __name__ == "__main__":
    print("--- Testing Dual Language Voice Engine ---")
    print("Speak in either English or Malayalam...")
    result = analyze_dual_voice_conversation()
    print("\n✅ Final Analysis Result:")
    print(json.dumps(result, indent=4))
