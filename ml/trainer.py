import pandas as pd
import numpy as np
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression
from sklearn.pipeline import Pipeline
from sklearn.model_selection import train_test_split
from sklearn.metrics import classification_report, confusion_matrix
import joblib
import os
from datetime import datetime

# Download dataset automatically
URL = "https://raw.githubusercontent.com/mohitgupta-omg/Kaggle-SMS-Spam-Collection-Dataset-/master/spam.csv"
DATA_PATH = "ml/spam.csv"
MODEL_PATH = "ml/pipeline.pkl"


def download_data():
    if not os.path.exists(DATA_PATH):
        print("Downloading dataset...")
        df = pd.read_csv(URL, encoding='latin-1')
        df = df[['v1', 'v2']]  # keep only label and text
        df.columns = ['label', 'text']
        os.makedirs("ml", exist_ok=True)
        df.to_csv(DATA_PATH, index=False)
        print("Dataset saved to ml/spam.csv")


def train_and_save_model():
    if os.path.exists(MODEL_PATH):
        print("Model already exists – loading")
        return joblib.load(MODEL_PATH)

    print(f"[{datetime.now()}] Training spam detector...")

    df = pd.read_csv(DATA_PATH)
    print("Dataset shape:", df.shape)
    print("\nClass distribution:\n", df.label.value_counts())

    # Convert labels to binary
    y = df.label.map({'ham': 0, 'spam': 1})
    X = df.text

    # Split
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42, stratify=y)

    # Create pipeline
    pipeline = Pipeline([
        ('tfidf', TfidfVectorizer(stop_words='english', max_features=3000)),
        ('clf', LogisticRegression(random_state=42))
    ])

    pipeline.fit(X_train, y_train)

    # Evaluation
    y_pred = pipeline.predict(X_test)
    print("\nClassification Report:\n")
    print(classification_report(y_test, y_pred, target_names=['ham', 'spam']))

    # Confusion Matrix
    tn, fp, fn, tp = confusion_matrix(y_test, y_pred).ravel()
    print(f"True Ham: {tn}, False Spam: {fp}")
    print(f"Missed Spam: {fn}, True Spam: {tp}")

    # Save model
    os.makedirs("ml", exist_ok=True)
    joblib.dump(pipeline, MODEL_PATH)
    print(f"Model saved to {MODEL_PATH}")

    return pipeline


# Run training when imported (only once thanks to cache)
pipeline = train_and_save_model()