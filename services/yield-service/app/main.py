from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.predictor import YieldPredictor
from app.schemas import YieldRequest, YieldResponse
import os

app = FastAPI(title="Crop Yield Prediction Service", version="1.0.0")
app.add_middleware(CORSMiddleware, allow_origins=["*"], allow_methods=["POST"], allow_headers=["*"])

predictor = YieldPredictor(model_path=os.getenv("MODEL_PATH", "models/yield_model.joblib"))


@app.get("/health")
def health():
    return {"status": "ok"}


@app.post("/predict", response_model=YieldResponse)
def predict(req: YieldRequest):
    return predictor.predict(req)
