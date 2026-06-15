import os
import joblib
import numpy as np
from app.schemas import FertilizerRequest

FERTILIZER_QUANTITIES: dict[str, str] = {
    "Urea": "50-60 kg/hectare",
    "DAP": "100-125 kg/hectare",
    "MOP": "50-60 kg/hectare",
    "SSP": "150-200 kg/hectare",
    "20-20": "100 kg/hectare",
    "10-26-26": "100 kg/hectare",
    "14-35-14": "100 kg/hectare",
    "17-17-17": "100 kg/hectare",
    "28-28": "100 kg/hectare",
    "Superphosphate": "100 kg/hectare",
}

FERTILIZER_REASONS: dict[str, str] = {
    "Urea": "Soil has low nitrogen. Urea provides 46% nitrogen to boost leafy growth.",
    "DAP": "Soil needs phosphorus and nitrogen. DAP supports root development and early growth.",
    "MOP": "Potassium is deficient. MOP improves drought resistance and fruit quality.",
    "SSP": "Phosphorus is low. SSP also supplies calcium and sulfur for soil health.",
    "20-20": "Balanced NPK needed for moderate soil deficiency.",
    "10-26-26": "High P and K needed — suitable for fruiting crops at flowering stage.",
    "14-35-14": "High phosphorus crop at critical growth stage.",
    "17-17-17": "Well-balanced NPK for general crop nutrition.",
    "28-28": "High nitrogen and phosphorus for leafy crops or early growth.",
    "Superphosphate": "Phosphorus-deficient soil. Promotes root growth and early establishment.",
}

# Soil type and crop type mappings matching the training data
SOIL_TYPES = ["Black", "Clayey", "Loamy", "Red", "Sandy"]
CROP_TYPES = ["Barley", "Cotton", "Ground Nuts", "Maize", "Millets",
              "Oil seeds", "Paddy", "Pulses", "Sugarcane", "Tobacco", "Wheat"]


class FertilizerRecommender:
    def __init__(self, model_path: str):
        self.model_path = model_path
        self._artifact = None

    def _get_artifact(self):
        if self._artifact is None and os.path.exists(self.model_path):
            self._artifact = joblib.load(self.model_path)
        return self._artifact

    def predict(self, req: FertilizerRequest) -> dict:
        artifact = self._get_artifact()

        if artifact:
            model = artifact["model"]
            le_fert = artifact["label_encoder"]
            le_soil = artifact["le_soil"]
            le_crop = artifact["le_crop"]

            soil_enc = le_soil.transform([req.soil_type])[0] if req.soil_type in le_soil.classes_ else 0
            crop_enc = le_crop.transform([req.crop])[0] if req.crop in le_crop.classes_ else 0

            features = np.array([[req.temperature, req.humidity, req.moisture,
                                   req.nitrogen, req.potassium, req.phosphorus,
                                   soil_enc, crop_enc]])
            label = le_fert.inverse_transform(model.predict(features))[0]
        else:
            label = self._rule_based(req)

        quantity = FERTILIZER_QUANTITIES.get(label, "100 kg/hectare")
        reason = FERTILIZER_REASONS.get(label, "Based on your soil analysis.")
        return {"fertilizer": label, "quantity": quantity, "reason": reason}

    def _rule_based(self, req: FertilizerRequest) -> str:
        if req.nitrogen < 30:
            return "Urea"
        if req.phosphorus < 30:
            return "DAP" if req.nitrogen < 50 else "Superphosphate"
        if req.potassium < 30:
            return "MOP"
        return "17-17-17"
