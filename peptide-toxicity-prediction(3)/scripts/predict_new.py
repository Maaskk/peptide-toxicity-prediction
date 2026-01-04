"""
Prediction script for new peptide sequences.

Load trained models and predict toxicity for new sequences.
"""

import sys
from pathlib import Path
import numpy as np

sys.path.append(str(Path(__file__).parent.parent))

from src.feature_extraction import PeptideFeatureExtractor
from src.models import ToxicityPredictor


def predict_sequences(sequences: list, model_path: str = "results/trained_models.pkl"):
    """
    Predict toxicity for new sequences.
    
    Args:
        sequences: List of amino acid sequences
        model_path: Path to trained models
    """
    print("="*70)
    print("PEPTIDE TOXICITY PREDICTION")
    print("="*70 + "\n")
    
    # Load models
    print(f"Loading trained models from {model_path}...")
    predictor = ToxicityPredictor()
    predictor.load_models(model_path)
    print("✓ Models loaded\n")
    
    # Initialize feature extractor (must match training configuration)
    extractor = PeptideFeatureExtractor(use_dipeptide=False)
    
    # Extract features
    print("Extracting features...")
    X, _ = extractor.extract_batch(sequences)
    print(f"✓ Features extracted: {X.shape}\n")
    
    # Make predictions with all models
    print("Making predictions...\n")
    
    for i, sequence in enumerate(sequences):
        print(f"Sequence {i+1}: {sequence}")
        print(f"  Length: {len(sequence)} AA\n")
        
        for model_name in ['Logistic Regression', 'Random Forest', 'SVM']:
            prediction = predictor.predict(X[i:i+1], model_name)[0]
            proba = predictor.predict_proba(X[i:i+1], model_name)[0]
            
            label = "TOXIC" if prediction == 1 else "NON-TOXIC"
            confidence = proba[1] if prediction == 1 else proba[0]
            
            print(f"  {model_name}:")
            print(f"    Prediction: {label}")
            print(f"    Confidence: {confidence*100:.2f}%")
            print(f"    P(toxic): {proba[1]*100:.2f}%")
        
        print()


if __name__ == "__main__":
    # Example usage
    example_sequences = [
        "GLFDIVKKVVGALG",  # Example toxic peptide
        "ATCDLLSGTVSRGGRL",  # Example non-toxic peptide
        "MKFLVFSLLLLFSSAYSRGVFRRDTHKSEIAHRFKDLGEEHFKGLVLIAFSQYLQQCPFDEHVKLVNELTEFAKT"
    ]
    
    predict_sequences(example_sequences)
