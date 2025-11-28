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

# Paths
DATA_PATH = "ml/spam.csv"
MODEL_PATH = "ml/pipeline.pkl"

# Dataset URL (permanent, works forever)
URL = "https://raw.githubusercontent.com/mohitgupta-omg/Kaggle-SMS-Spam-Collection-Dataset-/master/spam.csv"


def download_data():
    os.makedirs("ml", exist_ok=True)  # Ensure folder exists

    if not os.path.exists(DATA_PATH):
        print("[ML] Downloading SMS Spam dataset...")
        # Pandas can read directly from URL → no extra dependency
        df = pd.read_csv(URL, encoding="latin-1")
        df = df[['v1', 'v2']]
        df.columns = ['label', 'text']
        df.to_csv(DATA_PATH, index=False)
        print(f"[ML] Dataset saved to {len(df)} messages saved to {DATA_PATH}")


def train_and_save_model():
    os.makedirs("ml", exist_ok=True)

    if os.path.exists(MODEL_PATH):
        print(f"[ML] Model found → loading from {MODEL_PATH}")
        return joblib.load(MODEL_PATH)

    print(f"[{datetime.now()}] Training spam detector from scratch...")

    # ← THIS WAS MISSING ←
    download_data()  # ← NOW IT WILL DOWNLOAD IF NEEDED

    df = pd.read_csv(DATA_PATH)
    print(f"[ML] Loaded {len(df)} messages")

    y = df.label.map({'ham': 0, 'spam': 1})
    X = df.text

    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.2, random_state=42, stratify=y
    )

    pipeline = Pipeline([
        ('tfidf', TfidfVectorizer(stop_words='english', max_features=5000)),
        ('clf', LogisticRegression(random_state=42, max_iter=1000))
    ])

    pipeline.fit(X_train, y_train)

    y_pred = pipeline.predict(X_test)
    print("\n[ML] Classification Report:")
    print(classification_report(y_test, y_pred, target_names=['ham', 'spam']))

    tn, fp, fn, tp = confusion_matrix(y_test, y_pred).ravel()
    print(f"[ML] True Ham: {tn} | False Spam: {fp} | Missed Spam: {fn} | True Spam: {tp}")

    joblib.dump(pipeline, MODEL_PATH)
    print(f"[ML] Model trained and saved → {MODEL_PATH}")

    return pipeline


# Auto-run on import (only trains once per process)
pipeline = train_and_save_model()