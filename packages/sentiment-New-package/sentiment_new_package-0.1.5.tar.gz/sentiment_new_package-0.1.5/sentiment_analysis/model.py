import pickle
import joblib
from sklearn.feature_extraction.text import TfidfVectorizer
import importlib.resources as pkg_resources  # New import for loading bundled files

class SentimentModel:
    def __init__(self):
        # Automatically load the model and vectorizer from the package
        self.model = self.load_model()
        self.vectorizer = self.load_vectorizer()
        self.label_mapping = {
            0: "negative",
            1: "positive"
        }

    def load_model(self):
        # Load the model file from the package data
        with pkg_resources.open_binary('sentiment_analysis', 'classifier.pkl') as file:
            return pickle.load(file)

    def load_vectorizer(self):
        # Load the vectorizer file from the package data
        with pkg_resources.open_binary('sentiment_analysis', 'model_word.pkl') as file:
            return joblib.load(file)

    def predict(self, text: str):
        text_transformed = self.vectorizer.transform([text])
        prediction = self.model.predict(text_transformed)[0]
        return f"Your review is {self.label_mapping.get(prediction, 'unknown')}"
