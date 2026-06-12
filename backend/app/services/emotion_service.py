KEYWORD_EMOTIONS = (
    ("anger", ("angry", "frustrated", "annoyed", "irritated", "mad", "rage")),
    ("sadness", ("sad", "lonely", "low", "down", "depressed", "heartbroken", "tired")),
    ("fear", ("anxious", "afraid", "scared", "worried", "nervous", "panic")),
    ("joy", ("happy", "excited", "great", "good", "energetic", "joy")),
    ("love", ("love", "romantic", "grateful", "warm", "close")),
    ("surprise", ("surprised", "shocked", "amazed", "curious")),
)


def detect_emotion(text: str) -> dict:
    try:
        from src.models.nlp.inference import predict_emotion

        result = predict_emotion(text)
        return {
            "emotion": result["emotion"].lower(),
            "confidence": result["confidence"],
            "source": "transformer",
        }
    except Exception:
        normalized = text.lower()
        for emotion, keywords in KEYWORD_EMOTIONS:
            if any(keyword in normalized for keyword in keywords):
                return {"emotion": emotion, "confidence": 0.86, "source": "keyword"}

    return {"emotion": "neutral", "confidence": 0.62, "source": "keyword"}
