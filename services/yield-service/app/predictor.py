import os
import joblib
import numpy as np
from app.schemas import YieldRequest

STATE_YIELDS: dict[str, float] = {
    "Punjab": 4.5, "Haryana": 4.2, "Uttar Pradesh": 3.8, "West Bengal": 3.5,
    "Andhra Pradesh": 3.2, "Tamil Nadu": 3.0, "Maharashtra": 2.8, "Karnataka": 2.9,
    "Madhya Pradesh": 2.5, "Bihar": 2.3, "Rajasthan": 1.8, "Gujarat": 3.1,
}

CROP_BASE_YIELDS: dict[str, float] = {
    "rice": 3.0, "wheat": 3.5, "maize": 2.8, "cotton": 1.5, "sugarcane": 65.0,
    "soybean": 1.2, "tomato": 25.0, "potato": 20.0, "onion": 18.0,
    "groundnut": 1.5, "bajra": 1.2, "jowar": 1.0,
}

SEASON_MAP = {
    "kharif": "Kharif     ", "rabi": "Rabi       ",
    "whole year": "Whole Year ", "summer": "Summer     ",
    "winter": "Winter     ", "autumn": "Autumn     ",
}


class YieldPredictor:
    def __init__(self, model_path: str):
        self.model_path = model_path
        self._artifact = None

    def _get_artifact(self):
        if self._artifact is None and os.path.exists(self.model_path):
            self._artifact = joblib.load(self.model_path)
        return self._artifact

    def predict(self, req: YieldRequest) -> dict:
        artifact = self._get_artifact()

        if artifact:
            model = artifact["model"]
            le_crop = artifact["le_crop"]
            le_state = artifact["le_state"]
            le_season = artifact["le_season"]

            crop_lower = req.crop.lower().strip()
            state_str = req.state.strip()
            season_str = SEASON_MAP.get(req.season.lower(), "Whole Year ")

            crop_enc = le_crop.transform([crop_lower])[0] if crop_lower in le_crop.classes_ else 0
            state_enc = le_state.transform([state_str])[0] if state_str in le_state.classes_ else 0
            season_enc = le_season.transform([season_str])[0] if season_str in le_season.classes_ else 0

            features = np.array([[crop_enc, state_enc, season_enc,
                                   req.area, req.rainfall, req.fertilizer_usage, 0.0]])
            raw = float(model.predict(features)[0])
            realistic_max = {"sugarcane": 100.0, "potato": 45.0, "tomato": 55.0,
                             "onion": 35.0, "banana": 40.0}.get(req.crop.lower(), 8.0)
            # ML model trained on state-level totals — use only when in realistic range
            if 0.5 <= raw <= realistic_max:
                yield_per_ha = raw
            else:
                yield_per_ha = self._rule_based(req)
        else:
            yield_per_ha = self._rule_based(req)

        total = yield_per_ha * req.area
        return {
            "predicted_yield": f"{yield_per_ha:.2f} tons/hectare",
            "unit": "tons/hectare",
            "total_production": f"{total:.2f} tons",
        }

    def _rule_based(self, req: YieldRequest) -> float:
        base = CROP_BASE_YIELDS.get(req.crop.lower(), 2.5)
        state_factor = STATE_YIELDS.get(req.state, 2.5) / 3.0
        rain_factor = 0.7 if req.rainfall < 400 else (0.9 if req.rainfall > 1500 else 1.0)
        fert_factor = min(1.0 + (req.fertilizer_usage / 500), 1.3)
        return round(base * state_factor * rain_factor * fert_factor, 2)
