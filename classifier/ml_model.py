import joblib
import os

MODEL_PATH = os.path.join(os.path.dirname(__file__), "..", "model.pkl")
VECTORIZER_PATH = os.path.join(os.path.dirname(__file__), "..", "vectorizer.pkl")

model = joblib.load(MODEL_PATH)
vectorizer = joblib.load(VECTORIZER_PATH)


def predict(text:str) -> str:
    text_vector=vectorizer.transform([text])
    prediction = model.predict(text_vector)[0]
    return prediction