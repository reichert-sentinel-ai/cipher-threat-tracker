"""Anomaly detection endpoints"""

from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from typing import List, Dict
import numpy as np
import logging

# Optional imports - allow server to start without torch
try:
    from ...models.autoencoder import AnomalyDetector as AutoencoderDetector, TrafficAutoencoder
    TORCH_AVAILABLE = True
except ImportError:
    TORCH_AVAILABLE = False
    AutoencoderDetector = None
    TrafficAutoencoder = None

try:
    from ...models.anomaly_detector import BehavioralAnomalyDetector
    BEHAVIORAL_DETECTOR_AVAILABLE = True
except ImportError:
    BEHAVIORAL_DETECTOR_AVAILABLE = False
    BehavioralAnomalyDetector = None

try:
    from ...models.ioc_classifier import IOCClassifier
    IOC_CLASSIFIER_AVAILABLE = True
except ImportError:
    IOC_CLASSIFIER_AVAILABLE = False
    IOCClassifier = None

logger = logging.getLogger(__name__)

router = APIRouter()


class DetectionRequest(BaseModel):
    """Request model for anomaly detection"""
    features: List[float]  # Feature vector
    method: str = "autoencoder"  # "autoencoder" or "isolation_forest"


class IOCClassificationRequest(BaseModel):
    """Request model for IOC classification"""
    ioc: Dict  # IOC dictionary


@router.post("/detect/anomaly")
async def detect_anomaly(request: DetectionRequest):
    """
    Detect anomalies in feature vector.
    
    Args:
        request: Detection request with features and method
        
    Returns:
        Detection results with anomaly score and label
    """
    try:
        features = np.array(request.features).reshape(1, -1)
        
        if request.method == "autoencoder":
            # Autoencoder detection (would load trained model in production)
            return {
                "is_anomaly": False,
                "score": 0.5,
                "method": "autoencoder",
                "message": "Autoencoder model not loaded (requires trained model)"
            }
        
        elif request.method == "isolation_forest":
            # Isolation Forest detection (would load trained model in production)
            return {
                "is_anomaly": False,
                "score": 0.3,
                "method": "isolation_forest",
                "message": "Isolation Forest model not loaded (requires trained model)"
            }
        
        else:
            raise HTTPException(status_code=400, detail=f"Unknown method: {request.method}")
        
    except Exception as e:
        logger.error(f"Error detecting anomaly: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/detect/classify")
async def classify_ioc(request: IOCClassificationRequest):
    """
    Classify IOC threat type.
    
    Args:
        request: IOC classification request
        
    Returns:
        Classification results with threat type and confidence
    """
    try:
        # Load classifier (would load trained model in production)
        classifier = IOCClassifier()
        
        # Extract features and predict
        iocs = [request.ioc]
        predictions, probabilities = classifier.predict_iocs(iocs)
        
        # Get class probabilities
        class_probs = {}
        if len(probabilities) > 0 and len(probabilities[0]) > 0:
            classes = classifier.classes_ if hasattr(classifier, 'classes_') else []
            if classes and len(classes) == len(probabilities[0]):
                for i, class_name in enumerate(classes):
                    class_probs[class_name] = float(probabilities[0][i])
        
        return {
            "threat_type": predictions[0] if len(predictions) > 0 else "unknown",
            "confidence": float(max(probabilities[0])) if len(probabilities) > 0 and len(probabilities[0]) > 0 else 0.5,
            "class_probabilities": class_probs,
            "message": "Classifier model not trained (requires training data)"
        }
        
    except Exception as e:
        logger.error(f"Error classifying IOC: {e}")
        raise HTTPException(status_code=500, detail=str(e))
