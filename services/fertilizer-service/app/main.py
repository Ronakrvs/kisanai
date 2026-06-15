from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.recommender import FertilizerRecommender
from app.schemas import FertilizerRequest, FertilizerResponse
import os

app = FastAPI(title="Fertilizer Recommendation Service", version="1.0.0")

app.add_middleware(CORSMiddleware, allow_origins=["*"], allow_methods=["POST"], allow_headers=["*"])

recommender = FertilizerRecommender(model_path=os.getenv("MODEL_PATH", "models/fertilizer_model.joblib"))


@app.get("/health")
def health():
    return {"status": "ok"}


@app.post("/recommend", response_model=FertilizerResponse)
def recommend(req: FertilizerRequest):
    return recommender.predict(req)
