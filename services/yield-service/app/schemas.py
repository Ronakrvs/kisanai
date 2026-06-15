from pydantic import BaseModel, Field


class YieldRequest(BaseModel):
    state: str
    district: str
    crop: str
    rainfall: float = Field(ge=0)
    temperature: float = Field(ge=-10, le=60)
    area: float = Field(gt=0, description="Farm area in hectares")
    fertilizer_usage: float = Field(ge=0, description="kg/hectare")
    season: str = "Whole Year"


class YieldResponse(BaseModel):
    predicted_yield: str
    unit: str = "tons/hectare"
    total_production: str
