from src.recommender.emotion_mapping import EMOTION_TO_GENRE

emotion = "fear"

print(
    f"Emotion: {emotion}"
)

print(
    f"Genre: {EMOTION_TO_GENRE.get(emotion)}"
)