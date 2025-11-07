"""Autoencoder model for anomaly detection in network traffic"""

import torch
import torch.nn as nn
import torch.optim as optim
import numpy as np
from typing import Tuple, Optional, List
import logging

logger = logging.getLogger(__name__)


class TrafficAutoencoder(nn.Module):
    """Autoencoder for network traffic anomaly detection"""
    
    def __init__(self, input_dim: int = 512, encoding_dim: int = 128):
        """
        Initialize autoencoder.
        
        Args:
            input_dim: Input feature dimension (default: 512)
            encoding_dim: Encoder bottleneck dimension (default: 128)
        """
        super(TrafficAutoencoder, self).__init__()
        
        # Encoder: 512 -> 256 -> 128
        self.encoder = nn.Sequential(
            nn.Linear(input_dim, 256),
            nn.ReLU(),
            nn.Dropout(0.2),
            nn.Linear(256, encoding_dim),
            nn.ReLU()
        )
        
        # Decoder: 128 -> 256 -> 512
        self.decoder = nn.Sequential(
            nn.Linear(encoding_dim, 256),
            nn.ReLU(),
            nn.Dropout(0.2),
            nn.Linear(256, input_dim),
            nn.Sigmoid()  # Normalize output to [0, 1]
        )
    
    def forward(self, x: torch.Tensor) -> torch.Tensor:
        """
        Forward pass.
        
        Args:
            x: Input tensor [batch_size, input_dim]
            
        Returns:
            Reconstructed tensor [batch_size, input_dim]
        """
        encoded = self.encoder(x)
        decoded = self.decoder(encoded)
        return decoded
    
    def encode(self, x: torch.Tensor) -> torch.Tensor:
        """
        Encode input to latent representation.
        
        Args:
            x: Input tensor [batch_size, input_dim]
            
        Returns:
            Encoded tensor [batch_size, encoding_dim]
        """
        return self.encoder(x)


class AutoencoderTrainer:
    """Trainer for autoencoder model"""
    
    def __init__(self, 
                 input_dim: int = 512,
                 encoding_dim: int = 128,
                 learning_rate: float = 0.001,
                 device: Optional[str] = None):
        """
        Initialize trainer.
        
        Args:
            input_dim: Input feature dimension
            encoding_dim: Encoder bottleneck dimension
            learning_rate: Learning rate for optimizer
            device: Device to use (cuda/cpu)
        """
        self.device = device or ('cuda' if torch.cuda.is_available() else 'cpu')
        self.model = TrafficAutoencoder(input_dim=input_dim, encoding_dim=encoding_dim)
        self.model.to(self.device)
        
        self.criterion = nn.MSELoss()
        self.optimizer = optim.Adam(self.model.parameters(), lr=learning_rate)
        self.scheduler = optim.lr_scheduler.ReduceLROnPlateau(
            self.optimizer, mode='min', factor=0.5, patience=5, verbose=True
        )
    
    def train(self,
              train_loader: torch.utils.data.DataLoader,
              epochs: int = 50,
              val_loader: Optional[torch.utils.data.DataLoader] = None) -> List[float]:
        """
        Train autoencoder.
        
        Args:
            train_loader: Training data loader
            epochs: Number of training epochs
            val_loader: Optional validation data loader
            
        Returns:
            List of training losses per epoch
        """
        train_losses = []
        
        for epoch in range(epochs):
            # Training
            self.model.train()
            epoch_loss = 0.0
            num_batches = 0
            
            for batch in train_loader:
                if isinstance(batch, (list, tuple)):
                    batch = batch[0]
                
                batch = batch.to(self.device)
                
                # Forward pass
                self.optimizer.zero_grad()
                reconstructed = self.model(batch)
                loss = self.criterion(reconstructed, batch)
                
                # Backward pass
                loss.backward()
                self.optimizer.step()
                
                epoch_loss += loss.item()
                num_batches += 1
            
            avg_loss = epoch_loss / num_batches if num_batches > 0 else 0.0
            train_losses.append(avg_loss)
            
            # Validation
            val_loss = None
            if val_loader:
                val_loss = self.validate(val_loader)
                self.scheduler.step(val_loss)
            
            if (epoch + 1) % 10 == 0:
                logger.info(f"Epoch {epoch+1}/{epochs}, Train Loss: {avg_loss:.6f}, Val Loss: {val_loss:.6f if val_loss else 'N/A'}")
        
        return train_losses
    
    def validate(self, val_loader: torch.utils.data.DataLoader) -> float:
        """
        Validate model on validation set.
        
        Args:
            val_loader: Validation data loader
            
        Returns:
            Average validation loss
        """
        self.model.eval()
        val_loss = 0.0
        num_batches = 0
        
        with torch.no_grad():
            for batch in val_loader:
                if isinstance(batch, (list, tuple)):
                    batch = batch[0]
                
                batch = batch.to(self.device)
                reconstructed = self.model(batch)
                loss = self.criterion(reconstructed, batch)
                
                val_loss += loss.item()
                num_batches += 1
        
        avg_loss = val_loss / num_batches if num_batches > 0 else 0.0
        return avg_loss
    
    def save_model(self, filepath: str):
        """Save model to file."""
        torch.save({
            'model_state_dict': self.model.state_dict(),
            'optimizer_state_dict': self.optimizer.state_dict(),
        }, filepath)
        logger.info(f"Model saved to {filepath}")
    
    def load_model(self, filepath: str):
        """Load model from file."""
        checkpoint = torch.load(filepath, map_location=self.device)
        self.model.load_state_dict(checkpoint['model_state_dict'])
        self.optimizer.load_state_dict(checkpoint['optimizer_state_dict'])
        logger.info(f"Model loaded from {filepath}")


class AnomalyDetector:
    """Anomaly detector using trained autoencoder"""
    
    def __init__(self, model: TrafficAutoencoder, threshold_percentile: float = 95.0):
        """
        Initialize anomaly detector.
        
        Args:
            model: Trained autoencoder model
            threshold_percentile: Percentile for anomaly threshold (default: 95th)
        """
        self.model = model
        self.threshold_percentile = threshold_percentile
        self.threshold: Optional[float] = None
        self.device = next(model.parameters()).device
    
    def fit_threshold(self, normal_data: torch.Tensor):
        """
        Fit threshold on normal data.
        
        Args:
            normal_data: Tensor of normal samples [N, input_dim]
        """
        self.model.eval()
        reconstruction_errors = []
        
        with torch.no_grad():
            normal_data = normal_data.to(self.device)
            reconstructed = self.model(normal_data)
            errors = torch.mean((reconstructed - normal_data) ** 2, dim=1)
            reconstruction_errors.extend(errors.cpu().numpy())
        
        self.threshold = np.percentile(reconstruction_errors, self.threshold_percentile)
        logger.info(f"Anomaly threshold set to {self.threshold:.6f} (percentile: {self.threshold_percentile})")
    
    def detect(self, data: torch.Tensor) -> Tuple[np.ndarray, np.ndarray]:
        """
        Detect anomalies in data.
        
        Args:
            data: Input tensor [N, input_dim]
            
        Returns:
            Tuple of (is_anomaly array, anomaly_scores array)
        """
        if self.threshold is None:
            raise ValueError("Threshold not fitted. Call fit_threshold() first.")
        
        self.model.eval()
        
        with torch.no_grad():
            data = data.to(self.device)
            reconstructed = self.model(data)
            errors = torch.mean((reconstructed - data) ** 2, dim=1)
            scores = errors.cpu().numpy()
        
        is_anomaly = scores > self.threshold
        return is_anomaly, scores
    
    def predict(self, data: np.ndarray) -> Tuple[np.ndarray, np.ndarray]:
        """
        Predict anomalies for numpy array.
        
        Args:
            data: Input array [N, input_dim]
            
        Returns:
            Tuple of (is_anomaly array, anomaly_scores array)
        """
        data_tensor = torch.FloatTensor(data).to(self.device)
        return self.detect(data_tensor)

