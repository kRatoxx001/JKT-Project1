from src.models.nlp.inference import predict_emotion

texts = [
    "I am feeling very happy today",
    "I am stressed about my exams",
    "I feel lonely and sad",
    "I am excited for the trip"
]

for text in texts:

    result = predict_emotion(text)

    print("\nInput:", text)
    print("Output:", result)