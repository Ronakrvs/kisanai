from pydantic import BaseModel


class DetectionResponse(BaseModel):
    crop: str
    disease: str
    confidence: float
    cause: str
    treatment: str
    prevention: str
