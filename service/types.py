from typing import List
from pydantic import BaseModel

class Classification(BaseModel):
    classes: List[str]
    scores: List[float]

class Detection(BaseModel):
    category: str
    label: str
    conf: float
    bbox: List[float]

class Prediction(BaseModel):
    filepath: str
    classifications: Classification
    detections: List[Detection]
    prediction: str
    prediction_score: float
    prediction_source: str
    model_version: str

class PredictionsResponse(BaseModel):
    predictions: List[Prediction]
