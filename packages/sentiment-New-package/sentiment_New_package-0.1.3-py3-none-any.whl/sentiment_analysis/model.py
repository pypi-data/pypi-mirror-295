import pickle
import joblib
from sklearn.feature_extraction.text import TfidfVectorizer

class SentimentModel:
    def __init__(self, model_path: str, vectorizer_path: str):
        self.model_path = model_path
        self.vectorizer_path = vectorizer_path
        self.model = self.load_model()
        self.vectorizer = self.load_vectorizer()
        self.label_mapping = {
            0: "negative",
            1: "positive"
        }

    def load_model(self):
        with open(self.model_path, 'rb') as file:
            return pickle.load(file)

    def load_vectorizer(self):
        return joblib.load(self.vectorizer_path)  # Ensure this loads the vectorizer, not a matrix

    def predict(self, text: str):
        text_transformed = self.vectorizer.transform([text])
        prediction = self.model.predict(text_transformed)[0]
        return f"Your review is {self.label_mapping.get(prediction, 'unknown')}"
