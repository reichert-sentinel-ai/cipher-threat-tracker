"""IOC classifier using XGBoost"""

import numpy as np
import pandas as pd
from typing import List, Dict, Optional, Tuple
import xgboost as xgb
from sklearn.preprocessing import LabelEncoder
from sklearn.model_selection import train_test_split
from sklearn.metrics import classification_report, confusion_matrix, f1_score
import logging
import pickle

logger = logging.getLogger(__name__)


class IOCClassifier:
    """XGBoost classifier for IOC threat type classification"""
    
    def __init__(self,
                 n_estimators: int = 100,
                 max_depth: int = 6,
                 learning_rate: float = 0.1,
                 random_state: int = 42):
        """
        Initialize IOC classifier.
        
        Args:
            n_estimators: Number of boosting rounds
            max_depth: Maximum tree depth
            learning_rate: Learning rate
            random_state: Random seed
        """
        self.model = xgb.XGBClassifier(
            n_estimators=n_estimators,
            max_depth=max_depth,
            learning_rate=learning_rate,
            random_state=random_state,
            objective='multi:softprob',
            eval_metric='mlogloss',
            n_jobs=-1
        )
        self.label_encoder = LabelEncoder()
        self.feature_names: List[str] = []
        self.is_fitted = False
        self.classes_: Optional[np.ndarray] = None
    
    def extract_features(self, iocs: List[Dict]) -> Tuple[pd.DataFrame, pd.Series]:
        """
        Extract features from IOC dictionaries.
        
        Args:
            iocs: List of IOC dictionaries
            
        Returns:
            Tuple of (features DataFrame, labels Series)
        """
        features = []
        labels = []
        
        for ioc in iocs:
            feature_dict = self._extract_single_features(ioc)
            features.append(feature_dict)
            
            # Label is threat_type
            threat_type = ioc.get('threat_type', 'unknown')
            labels.append(threat_type)
        
        df = pd.DataFrame(features)
        labels_series = pd.Series(labels)
        
        return df, labels_series
    
    def _extract_single_features(self, ioc: Dict) -> Dict:
        """Extract features from a single IOC."""
        ioc_value = str(ioc.get('ioc_value', ''))
        ioc_type = ioc.get('ioc_type', 'unknown')
        
        features = {
            'ioc_type_ip': 1 if ioc_type == 'ip' else 0,
            'ioc_type_url': 1 if ioc_type == 'url' else 0,
            'ioc_type_domain': 1 if ioc_type == 'domain' else 0,
            'ioc_type_hash': 1 if ioc_type == 'hash' else 0,
            'ioc_type_email': 1 if ioc_type == 'email' else 0,
            'ioc_type_cve': 1 if ioc_type == 'cve' else 0,
            'confidence': float(ioc.get('confidence', 0.5)),
            'num_tags': len(ioc.get('tags', [])),
            'has_description': 1 if ioc.get('metadata', {}).get('description') else 0,
            'has_references': 1 if ioc.get('metadata', {}).get('references') else 0,
            'ioc_length': len(ioc_value),
            'source_otx': 1 if ioc.get('source', '').startswith('otx') else 0,
            'source_abuse': 1 if 'abuse' in ioc.get('source', '').lower() else 0,
            'source_phishtank': 1 if 'phishtank' in ioc.get('source', '').lower() else 0,
            'source_nvd': 1 if ioc.get('source', '') == 'nvd' else 0,
        }
        
        # Add hash-specific features
        if ioc_type == 'hash':
            features['hash_length'] = len(ioc_value)
            features['is_md5'] = 1 if len(ioc_value) == 32 else 0
            features['is_sha1'] = 1 if len(ioc_value) == 40 else 0
            features['is_sha256'] = 1 if len(ioc_value) == 64 else 0
        else:
            features['hash_length'] = 0
            features['is_md5'] = 0
            features['is_sha1'] = 0
            features['is_sha256'] = 0
        
        # Add IP-specific features
        if ioc_type == 'ip':
            parts = ioc_value.split('.')
            if len(parts) == 4:
                try:
                    features['ip_first_octet'] = int(parts[0])
                    features['ip_private'] = 1 if (parts[0] == '10' or 
                                                   (parts[0] == '192' and parts[1] == '168') or
                                                   parts[0] == '172') else 0
                except ValueError:
                    features['ip_first_octet'] = 0
                    features['ip_private'] = 0
            else:
                features['ip_first_octet'] = 0
                features['ip_private'] = 0
        else:
            features['ip_first_octet'] = 0
            features['ip_private'] = 0
        
        # Add URL/domain-specific features
        if ioc_type in ['url', 'domain']:
            features['has_path'] = 1 if '/' in ioc_value else 0
            features['num_subdomains'] = ioc_value.count('.')
            features['has_port'] = 1 if ':' in ioc_value else 0
        else:
            features['has_path'] = 0
            features['num_subdomains'] = 0
            features['has_port'] = 0
        
        return features
    
    def fit(self, X: pd.DataFrame, y: pd.Series, validation_split: float = 0.2):
        """
        Train IOC classifier.
        
        Args:
            X: Feature matrix [N, features]
            y: Labels [N]
            validation_split: Fraction of data to use for validation
        """
        # Encode labels
        y_encoded = self.label_encoder.fit_transform(y)
        self.classes_ = self.label_encoder.classes_
        
        # Split data
        X_train, X_val, y_train, y_val = train_test_split(
            X, y_encoded, test_size=validation_split, random_state=42, stratify=y_encoded
        )
        
        # Train model
        self.model.fit(
            X_train, y_train,
            eval_set=[(X_val, y_val)],
            early_stopping_rounds=10,
            verbose=False
        )
        
        # Store feature names
        self.feature_names = list(X.columns)
        self.is_fitted = True
        
        # Evaluate
        train_score = self.model.score(X_train, y_train)
        val_score = self.model.score(X_val, y_val)
        
        logger.info(f"Model trained - Train accuracy: {train_score:.4f}, Val accuracy: {val_score:.4f}")
        
        # Get predictions for evaluation
        y_pred = self.model.predict(X_val)
        f1 = f1_score(y_val, y_pred, average='weighted')
        
        logger.info(f"Validation F1-score: {f1:.4f}")
        logger.info(f"Classes: {list(self.classes_)}")
    
    def predict(self, X: pd.DataFrame) -> np.ndarray:
        """
        Predict threat types.
        
        Args:
            X: Feature matrix [N, features]
            
        Returns:
            Array of predicted threat types (strings)
        """
        if not self.is_fitted:
            raise ValueError("Model not fitted. Call fit() first.")
        
        predictions = self.model.predict(X)
        return self.label_encoder.inverse_transform(predictions)
    
    def predict_proba(self, X: pd.DataFrame) -> np.ndarray:
        """
        Predict threat type probabilities.
        
        Args:
            X: Feature matrix [N, features]
            
        Returns:
            Array of class probabilities [N, num_classes]
        """
        if not self.is_fitted:
            raise ValueError("Model not fitted. Call fit() first.")
        
        return self.model.predict_proba(X)
    
    def fit_from_iocs(self, iocs: List[Dict], validation_split: float = 0.2):
        """
        Fit model directly from IOC dictionaries.
        
        Args:
            iocs: List of IOC dictionaries with 'threat_type' labels
            validation_split: Fraction of data to use for validation
        """
        X, y = self.extract_features(iocs)
        self.fit(X, y, validation_split=validation_split)
    
    def predict_iocs(self, iocs: List[Dict]) -> Tuple[np.ndarray, np.ndarray]:
        """
        Predict threat types for IOC dictionaries.
        
        Args:
            iocs: List of IOC dictionaries
            
        Returns:
            Tuple of (predictions array, probabilities array)
        """
        X, _ = self.extract_features(iocs)
        predictions = self.predict(X)
        probabilities = self.predict_proba(X)
        
        return predictions, probabilities
    
    def save_model(self, filepath: str):
        """Save model to file."""
        with open(filepath, 'wb') as f:
            pickle.dump({
                'model': self.model,
                'label_encoder': self.label_encoder,
                'feature_names': self.feature_names,
                'classes': self.classes_
            }, f)
        logger.info(f"Model saved to {filepath}")
    
    def load_model(self, filepath: str):
        """Load model from file."""
        with open(filepath, 'rb') as f:
            data = pickle.load(f)
            self.model = data['model']
            self.label_encoder = data['label_encoder']
            self.feature_names = data['feature_names']
            self.classes_ = data['classes']
            self.is_fitted = True
        logger.info(f"Model loaded from {filepath}")

