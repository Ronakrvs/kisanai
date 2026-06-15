"""
Training script for crop yield prediction.
Dataset: crop_yield.csv (Kaggle: akshatgupta7/crop-yield-in-indian-states-dataset)
Columns: Crop, Crop_Year, Season, State, Area, Production, Annual_Rainfall,
         Fertilizer, Pesticide, Yield
"""

import pandas as pd
import numpy as np
import joblib
import os
from xgboost import XGBRegressor
from sklearn.model_selection import train_test_split
from sklearn.metrics import mean_absolute_error, r2_score
from sklearn.preprocessing import LabelEncoder


def train(data_path: str = "data/crop_yield.csv"):
    df = pd.read_csv(data_path)
    df = df.dropna(subset=["Yield"])

    le_crop = LabelEncoder()
    le_state = LabelEncoder()
    le_season = LabelEncoder()

    df["Crop_enc"] = le_crop.fit_transform(df["Crop"].str.lower().str.strip())
    df["State_enc"] = le_state.fit_transform(df["State"].str.strip())
    df["Season_enc"] = le_season.fit_transform(df["Season"].str.strip())

    features = ["Crop_enc", "State_enc", "Season_enc", "Area", "Annual_Rainfall", "Fertilizer", "Pesticide"]
    X = df[features].fillna(0)
    y = df["Yield"]

    X_train, X_val, y_train, y_val = train_test_split(X, y, test_size=0.2, random_state=42)

    model = XGBRegressor(
        n_estimators=300, max_depth=6, learning_rate=0.05,
        subsample=0.8, colsample_bytree=0.8, random_state=42,
        verbosity=0,
    )
    model.fit(X_train, y_train, eval_set=[(X_val, y_val)], verbose=50)

    preds = model.predict(X_val)
    print(f"MAE:  {mean_absolute_error(y_val, preds):.4f}")
    print(f"R2:   {r2_score(y_val, preds):.4f}")

    os.makedirs("models", exist_ok=True)
    artifact = {
        "model": model,
        "le_crop": le_crop,
        "le_state": le_state,
        "le_season": le_season,
        "feature_cols": features,
    }
    joblib.dump(artifact, "models/yield_model.joblib")
    print("Saved to models/yield_model.joblib")


if __name__ == "__main__":
    train()
