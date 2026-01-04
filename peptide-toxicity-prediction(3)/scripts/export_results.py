"""
Export results in various formats for reporting and publication
"""
import json
import csv
from pathlib import Path
import joblib
import numpy as np
import pandas as pd


def export_predictions_csv(predictions, sequences, labels, output_path='results/predictions.csv'):
    """
    Export predictions to CSV format
    
    Args:
        predictions: Model predictions
        sequences: Peptide sequences
        labels: True labels
        output_path: Output file path
    """
    df = pd.DataFrame({
        'Sequence': sequences,
        'True_Label': ['Toxic' if l == 1 else 'Non-Toxic' for l in labels],
        'Predicted_Label': ['Toxic' if p > 0.5 else 'Non-Toxic' for p in predictions],
        'Toxic_Probability': predictions,
        'Non_Toxic_Probability': 1 - predictions,
        'Correct': [int(l == (1 if p > 0.5 else 0)) for l, p in zip(labels, predictions)]
    })
    
    df.to_csv(output_path, index=False)
    print(f"Predictions exported to {output_path}")


def export_model_summary_json(model_metrics, feature_importance, output_path='results/model_summary.json'):
    """
    Export model summary to JSON
    
    Args:
        model_metrics: Dictionary of model performance metrics
        feature_importance: Dictionary of feature importances
        output_path: Output file path
    """
    summary = {
        'model_performance': model_metrics,
        'feature_importance': {
            'top_10': dict(list(feature_importance.items())[:10]),
            'all_features': feature_importance
        },
        'metadata': {
            'created_at': pd.Timestamp.now().isoformat(),
            'framework': 'scikit-learn',
            'features': list(feature_importance.keys())
        }
    }
    
    with open(output_path, 'w') as f:
        json.dump(summary, f, indent=2)
    
    print(f"Model summary exported to {output_path}")


def export_feature_matrix(features, feature_names, sequences, output_path='results/feature_matrix.csv'):
    """
    Export feature matrix to CSV
    
    Args:
        features: Feature matrix
        feature_names: List of feature names
        sequences: Peptide sequences
        output_path: Output file path
    """
    df = pd.DataFrame(features, columns=feature_names)
    df.insert(0, 'Sequence', sequences)
    
    df.to_csv(output_path, index=False)
    print(f"Feature matrix exported to {output_path}")


def create_publication_table(model_metrics, output_path='results/publication_table.txt'):
    """
    Create publication-ready table
    
    Args:
        model_metrics: Model performance metrics
        output_path: Output file path
    """
    with open(output_path, 'w') as f:
        f.write("=" * 80 + "\n")
        f.write("Table 1: Model Performance Comparison\n")
        f.write("=" * 80 + "\n\n")
        
        f.write(f"{'Model':<25} {'Accuracy':<12} {'Precision':<12} {'Recall':<12} {'F1-Score':<12}\n")
        f.write("-" * 80 + "\n")
        
        for model_name, metrics in model_metrics.items():
            f.write(f"{model_name:<25} ")
            f.write(f"{metrics['Accuracy']:.4f}       ")
            f.write(f"{metrics['Precision']:.4f}       ")
            f.write(f"{metrics['Recall']:.4f}       ")
            f.write(f"{metrics['F1-Score']:.4f}\n")
        
        f.write("=" * 80 + "\n")
    
    print(f"Publication table exported to {output_path}")


if __name__ == '__main__':
    print("Export utilities loaded. Use functions to export results.")
