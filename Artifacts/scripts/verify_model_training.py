"""
Verify that models are trained and meet performance targets.

Usage:
    python scripts/verify_model_training.py
"""
import os
from pathlib import Path

def verify_autoencoder_model():
    """Verify autoencoder model exists."""
    model_path = Path("models/autoencoder_model.pth")
    
    if not model_path.exists():
        print("❌ Autoencoder model not found")
        print(f"   Expected location: {model_path.absolute()}")
        print("   Run: python src/models/train_autoencoder.py")
        return False
    
    try:
        import torch
        model = torch.load(model_path)
        print(f"✅ Autoencoder model found")
        return True
    except Exception as e:
        print(f"❌ Error loading autoencoder: {e}")
        return False

def verify_performance_targets():
    """Verify performance targets are documented."""
    targets = {
        'detection_precision': 0.953,
        'false_positive_rate': 0.021,
    }
    
    print("\nPerformance Targets:")
    for metric, target in targets.items():
        if 'rate' in metric:
            print(f"   {metric}: ≤{target:.2%}")
        else:
            print(f"   {metric}: ≥{target:.2%}")
    
    print("\n⚠️  Model performance verification requires:")
    print("   1. Trained models")
    print("   2. Test IOCs")
    print("   3. Running evaluation script")
    
    return False

if __name__ == "__main__":
    print("=" * 60)
    print("Cipher Model Training Verification")
    print("=" * 60)
    print()
    
    repo_dir = Path(__file__).parent.parent
    os.chdir(repo_dir)
    
    print("1. Model Files:")
    print("-" * 60)
    model_ok = verify_autoencoder_model()
    
    print("\n2. Performance Targets:")
    print("-" * 60)
    verify_performance_targets()
    
    print("\n" + "=" * 60)
    print("Summary:")
    print("=" * 60)
    
    if model_ok:
        print("✅ Model found!")
    else:
        print("⚠️  Model not found. See docs/MODEL_TRAINING_VERIFICATION.md for details.")

