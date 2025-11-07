"""Isolation Forest and other anomaly detection models"""

import numpy as np
from typing import Tuple, Optional, List
from sklearn.ensemble import IsolationForest
from sklearn.preprocessing import StandardScaler
import logging

logger = logging.getLogger(__name__)


class IsolationForestDetector:
    """Isolation Forest for behavioral anomaly detection"""
    
    def __init__(self,
                 contamination: float = 0.05,
                 n_estimators: int = 100,
                 max_samples: float = 1.0,
                 random_state: int = 42):
        """
        Initialize Isolation Forest detector.
        
        Args:
            contamination: Expected proportion of anomalies (default: 0.05 = 5%)
            n_estimators: Number of trees in the forest
            max_samples: Proportion of samples to use for each tree
            random_state: Random seed
        """
        self.model = IsolationForest(
            contamination=contamination,
            n_estimators=n_estimators,
            max_samples=max_samples,
            random_state=random_state,
            n_jobs=-1
        )
        self.scaler = StandardScaler()
        self.is_fitted = False
    
    def fit(self, X: np.ndarray):
        """
        Fit Isolation Forest on normal data.
        
        Args:
            X: Feature matrix [N, features]
        """
        # Scale features
        X_scaled = self.scaler.fit_transform(X)
        
        # Fit model
        self.model.fit(X_scaled)
        self.is_fitted = True
        
        logger.info(f"Fitted Isolation Forest on {X.shape[0]} samples with {X.shape[1]} features")
    
    def predict(self, X: np.ndarray) -> Tuple[np.ndarray, np.ndarray]:
        """
        Predict anomalies.
        
        Args:
            X: Feature matrix [N, features]
            
        Returns:
            Tuple of (is_anomaly array, anomaly_scores array)
                - is_anomaly: Boolean array (-1 for anomaly, 1 for normal)
                - scores: Anomaly scores (more negative = more anomalous)
        """
        if not self.is_fitted:
            raise ValueError("Model not fitted. Call fit() first.")
        
        # Scale features
        X_scaled = self.scaler.transform(X)
        
        # Predict
        predictions = self.model.predict(X_scaled)
        scores = self.model.score_samples(X_scaled)
        
        # Convert to boolean (1 = normal, -1 = anomaly)
        is_anomaly = predictions == -1
        
        return is_anomaly, scores
    
    def fit_predict(self, X: np.ndarray) -> Tuple[np.ndarray, np.ndarray]:
        """
        Fit and predict in one step.
        
        Args:
            X: Feature matrix [N, features]
            
        Returns:
            Tuple of (is_anomaly array, anomaly_scores array)
        """
        self.fit(X)
        return self.predict(X)
    
    def get_feature_importance(self) -> np.ndarray:
        """
        Get feature importances (not directly available in Isolation Forest).
        Returns dummy array for compatibility.
        
        Returns:
            Array of feature importances (all zeros, as Isolation Forest doesn't provide this)
        """
        # Isolation Forest doesn't directly provide feature importance
        # Return zeros as placeholder
        n_features = self.model.n_features_in_ if hasattr(self.model, 'n_features_in_') else 0
        return np.zeros(n_features)


class BehavioralAnomalyDetector:
    """Composite anomaly detector using multiple methods"""
    
    def __init__(self,
                 iso_forest_contamination: float = 0.05,
                 use_iso_forest: bool = True):
        """
        Initialize behavioral anomaly detector.
        
        Args:
            iso_forest_contamination: Contamination rate for Isolation Forest
            use_iso_forest: Whether to use Isolation Forest
        """
        self.use_iso_forest = use_iso_forest
        if use_iso_forest:
            self.iso_forest = IsolationForestDetector(
                contamination=iso_forest_contamination
            )
        else:
            self.iso_forest = None
    
    def fit(self, X: np.ndarray):
        """
        Fit anomaly detectors.
        
        Args:
            X: Feature matrix [N, features]
        """
        if self.use_iso_forest and self.iso_forest:
            self.iso_forest.fit(X)
    
    def predict(self, X: np.ndarray) -> Tuple[np.ndarray, np.ndarray]:
        """
        Predict anomalies using ensemble of methods.
        
        Args:
            X: Feature matrix [N, features]
            
        Returns:
            Tuple of (is_anomaly array, anomaly_scores array)
        """
        if not self.iso_forest:
            raise ValueError("No detectors initialized")
        
        is_anomaly, scores = self.iso_forest.predict(X)
        
        # Combine results from multiple detectors if available
        # For now, just use Isolation Forest
        
        return is_anomaly, scores
    
    def fit_predict(self, X: np.ndarray) -> Tuple[np.ndarray, np.ndarray]:
        """
        Fit and predict in one step.
        
        Args:
            X: Feature matrix [N, features]
            
        Returns:
            Tuple of (is_anomaly array, anomaly_scores array)
        """
        self.fit(X)
        return self.predict(X)

