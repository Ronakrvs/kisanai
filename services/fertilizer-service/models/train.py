"""
Training script for fertilizer recommendation model.
Dataset: Fertilizer Prediction.csv (Kaggle: gdabhishek/fertilizer-prediction)
Columns: Temparature, Humidity, Moisture, Soil Type, Crop Type,
         Nitrogen, Potassium, Phosphorous, Fertilizer Name
"""

import pandas as pd
import joblib
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score
from sklearn.preprocessing import LabelEncoder
import os


def train(data_path: str = "data/Fertilizer Prediction.csv"):
    df = pd.read_csv(data_path)
    df.columns = df.columns.str.strip()

    le_soil = LabelEncoder()
    le_crop = LabelEncoder()
    le_fert = LabelEncoder()

    df["Soil_enc"] = le_soil.fit_transform(df["Soil Type"])
    df["Crop_enc"] = le_crop.fit_transform(df["Crop Type"])
    y = le_fert.fit_transform(df["Fertilizer Name"])

    X = df[["Temparature", "Humidity", "Moisture", "Nitrogen", "Potassium", "Phosphorous", "Soil_enc", "Crop_enc"]]

    X_train, X_val, y_train, y_val = train_test_split(X, y, test_size=0.2, random_state=42)

    model = RandomForestClassifier(n_estimators=200, max_depth=10, random_state=42, n_jobs=-1)
    model.fit(X_train, y_train)

    acc = accuracy_score(y_val, model.predict(X_val))
    print(f"Validation Accuracy: {acc:.4f}")
    print("Classes:", list(le_fert.classes_))

    os.makedirs("models", exist_ok=True)
    artifact = {
        "model": model,
        "label_encoder": le_fert,
        "le_soil": le_soil,
        "le_crop": le_crop,
        "feature_cols": ["Temparature", "Humidity", "Moisture", "Nitrogen", "Potassium", "Phosphorous", "Soil_enc", "Crop_enc"],
    }
    joblib.dump(artifact, "models/fertilizer_model.joblib")
    print("Saved to models/fertilizer_model.joblib")


if __name__ == "__main__":
    train()
