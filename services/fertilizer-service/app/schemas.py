from pydantic import BaseModel, Field
from typing import Literal


class FertilizerRequest(BaseModel):
    crop: str
    soil_type: Literal["Black", "Clayey", "Loamy", "Red", "Sandy"] = "Loamy"
    temperature: float = Field(ge=-10, le=60)
    humidity: float = Field(ge=0, le=100)
    moisture: float = Field(ge=0, le=100, default=40)
    nitrogen: float = Field(ge=0, le=200)
    phosphorus: float = Field(ge=0, le=200)
    potassium: float = Field(ge=0, le=200)


class FertilizerResponse(BaseModel):
    fertilizer: str
    quantity: str
    reason: str
