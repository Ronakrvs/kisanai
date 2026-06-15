from fastapi import FastAPI, UploadFile, File, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from app.detector import DiseaseDetector
from app.schemas import DetectionResponse
import os

app = FastAPI(title="Disease Detection Service", version="1.0.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["POST"],
    allow_headers=["*"],
)

detector = DiseaseDetector(model_path=os.getenv("MODEL_PATH", "models/disease_model.onnx"))


@app.get("/health")
def health():
    return {"status": "ok"}


@app.post("/detect", response_model=DetectionResponse)
async def detect(image: UploadFile = File(...)):
    if not image.content_type.startswith("image/"):
        raise HTTPException(status_code=400, detail="File must be an image")

    contents = await image.read()
    if len(contents) > 10 * 1024 * 1024:
        raise HTTPException(status_code=400, detail="Image too large (max 10MB)")

    return detector.predict(contents)
