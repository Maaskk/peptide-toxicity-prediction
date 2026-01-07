"""
Comprehensive evaluation module for model performance assessment.

Generates metrics, confusion matrices, ROC curves, and statistical analyses.
"""

import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from typing import Dict, List, Tuple
from sklearn.metrics import (
    accuracy_score, precision_score, recall_score, f1_score,
    roc_auc_score, roc_curve, confusion_matrix, classification_report
)
from pathlib import Path


class ModelEvaluator:
    """
    Comprehensive evaluation toolkit for binary classification models.
    
    Provides metrics, visualizations, and statistical analyses suitable
    for publication-quality scientific reporting.
    """
    
    def __init__(self, output_dir: str = "results"):
        """
        Initialize evaluator.
        
        Args:
            output_dir: Directory to save evaluation results
        """
        self.output_dir = Path(output_dir)
        self.output_dir.mkdir(exist_ok=True)
        
        # Set publication-quality plotting style
        sns.set_style("whitegrid")
        plt.rcParams['figure.figsize'] = (10, 8)
        plt.rcParams['font.size'] = 11
        plt.rcParams['axes.labelsize'] = 12
        plt.rcParams['axes.titlesize'] = 14
        plt.rcParams['xtick.labelsize'] = 10
        plt.rcParams['ytick.labelsize'] = 10
        plt.rcParams['legend.fontsize'] = 10
    
    def evaluate_model(self, y_true: np.ndarray, y_pred: np.ndarray, 
                      y_proba: np.ndarray, model_name: str) -> Dict:
        """
        Compute comprehensive evaluation metrics.
        
        Args:
            y_true: True labels
            y_pred: Predicted labels
            y_proba: Predicted probabilities for positive class
            model_name: Name of the model
            
        Returns:
            Dictionary of evaluation metrics
        """
        print(f"\n{'='*70}")
        print(f"EVALUATING: {model_name}")
        print(f"{'='*70}\n")
        
        # Core classification metrics
        metrics = {
            'accuracy': accuracy_score(y_true, y_pred),
            'precision': precision_score(y_true, y_pred, zero_division=0),
            'recall': recall_score(y_true, y_pred, zero_division=0),
            'f1_score': f1_score(y_true, y_pred, zero_division=0),
            'roc_auc': roc_auc_score(y_true, y_proba)
        }
        
        # Print metrics
        print("Classification Metrics:")
        print(f"  Accuracy:  {metrics['accuracy']:.4f}")
        print(f"  Precision: {metrics['precision']:.4f}")
        print(f"  Recall:    {metrics['recall']:.4f}")
        print(f"  F1-score:  {metrics['f1_score']:.4f}")
        print(f"  ROC-AUC:   {metrics['roc_auc']:.4f}")
        
        # Detailed classification report
        print(f"\nDetailed Classification Report:")
        print(classification_report(y_true, y_pred, 
                                   target_names=['Non-toxic', 'Toxic'],
                                   digits=4))
        
        # Confusion matrix
        cm = confusion_matrix(y_true, y_pred)
        metrics['confusion_matrix'] = cm
        
        print(f"Confusion Matrix:")
        print(f"                 Predicted")
        print(f"                 Non-toxic  Toxic")
        print(f"Actual Non-toxic    {cm[0,0]:5d}   {cm[0,1]:5d}")
        print(f"       Toxic        {cm[1,0]:5d}   {cm[1,1]:5d}")
        
        return metrics
    
    def plot_confusion_matrix(self, cm: np.ndarray, model_name: str, 
                             dataset_name: str = "Test"):
        """
        Plot confusion matrix heatmap.
        
        Args:
            cm: Confusion matrix
            model_name: Name of model
            dataset_name: Name of dataset (e.g., "Test", "Validation")
        """
        plt.figure(figsize=(8, 6))
        
        # Create heatmap
        sns.heatmap(cm, annot=True, fmt='d', cmap='Blues', 
                   xticklabels=['Non-toxic', 'Toxic'],
                   yticklabels=['Non-toxic', 'Toxic'],
                   cbar_kws={'label': 'Count'})
        
        plt.title(f'Confusion Matrix: {model_name}\n({dataset_name} Set)', 
                 fontsize=14, fontweight='bold')
        plt.ylabel('True Label', fontweight='bold')
        plt.xlabel('Predicted Label', fontweight='bold')
        plt.tight_layout()
        
        # Save figure
        filename = f"{model_name.replace(' ', '_')}_confusion_matrix.png"
        filepath = self.output_dir / filename
        plt.savefig(filepath, dpi=300, bbox_inches='tight')
        print(f"✓ Confusion matrix saved to {filepath}")
        plt.close()
    
    def plot_roc_curve(self, y_true: np.ndarray, y_proba: np.ndarray, 
                       model_name: str, dataset_name: str = "Test"):
        """
        Plot ROC curve with AUC.
        
        ROC curve shows trade-off between true positive rate and false positive rate.
        AUC (Area Under Curve) summarizes model discrimination ability.
        
        Args:
            y_true: True labels
            y_proba: Predicted probabilities for positive class
            model_name: Name of model
            dataset_name: Name of dataset
        """
        # Calculate ROC curve
        fpr, tpr, thresholds = roc_curve(y_true, y_proba)
        auc = roc_auc_score(y_true, y_proba)
        
        plt.figure(figsize=(8, 8))
        
        # Plot ROC curve
        plt.plot(fpr, tpr, color='darkorange', lw=2, 
                label=f'{model_name} (AUC = {auc:.4f})')
        
        # Plot diagonal (random classifier)
        plt.plot([0, 1], [0, 1], color='navy', lw=2, linestyle='--', 
                label='Random Classifier (AUC = 0.5000)')
        
        plt.xlim([0.0, 1.0])
        plt.ylim([0.0, 1.05])
        plt.xlabel('False Positive Rate', fontweight='bold')
        plt.ylabel('True Positive Rate', fontweight='bold')
        plt.title(f'ROC Curve: {model_name}\n({dataset_name} Set)', 
                 fontsize=14, fontweight='bold')
        plt.legend(loc="lower right")
        plt.grid(True, alpha=0.3)
        plt.tight_layout()
        
        # Save figure
        filename = f"{model_name.replace(' ', '_')}_roc_curve.png"
        filepath = self.output_dir / filename
        plt.savefig(filepath, dpi=300, bbox_inches='tight')
        print(f"✓ ROC curve saved to {filepath}")
        plt.close()
    
    def compare_models(self, results: Dict[str, Dict], metric: str = 'f1_score'):
        """
        Create comparison plot of model performance.
        
        Args:
            results: Dictionary mapping model names to their metrics
            metric: Metric to compare (default: 'f1_score')
        """
        model_names = list(results.keys())
        scores = [results[name][metric] for name in model_names]
        
        plt.figure(figsize=(10, 6))
        
        # Create bar plot
        bars = plt.bar(model_names, scores, color=['#3498db', '#2ecc71', '#e74c3c'])
        
        # Add value labels on bars
        for bar in bars:
            height = bar.get_height()
            plt.text(bar.get_x() + bar.get_width()/2., height,
                    f'{height:.4f}',
                    ha='center', va='bottom', fontweight='bold')
        
        plt.ylabel(metric.replace('_', ' ').title(), fontweight='bold')
        plt.title(f'Model Comparison: {metric.replace("_", " ").title()}', 
                 fontsize=14, fontweight='bold')
        plt.ylim([0, 1.0])
        plt.grid(True, axis='y', alpha=0.3)
        plt.tight_layout()
        
        # Save figure
        filename = f"model_comparison_{metric}.png"
        filepath = self.output_dir / filename
        plt.savefig(filepath, dpi=300, bbox_inches='tight')
        print(f"✓ Model comparison saved to {filepath}")
        plt.close()
    
    def plot_feature_importance(self, importance_scores: np.ndarray, 
                               feature_names: List[str], 
                               model_name: str, top_n: int = 20):
        """
        Plot top feature importances.
        
        Feature importance indicates which molecular properties
        are most predictive of peptide toxicity.
        
        Args:
            importance_scores: Array of importance values
            feature_names: List of feature names
            model_name: Name of model
            top_n: Number of top features to display
        """
        if importance_scores is None:
            print(f"Feature importance not available for {model_name}")
            return
        
        # Sort features by importance
        indices = np.argsort(importance_scores)[::-1][:top_n]
        top_features = [feature_names[i] for i in indices]
        top_scores = importance_scores[indices]
        
        plt.figure(figsize=(10, 8))
        
        # Create horizontal bar plot
        y_pos = np.arange(len(top_features))
        plt.barh(y_pos, top_scores, color='steelblue')
        plt.yticks(y_pos, top_features)
        plt.xlabel('Importance Score', fontweight='bold')
        plt.title(f'Top {top_n} Feature Importances: {model_name}', 
                 fontsize=14, fontweight='bold')
        plt.gca().invert_yaxis()  # Highest importance at top
        plt.tight_layout()
        
        # Save figure
        filename = f"{model_name.replace(' ', '_')}_feature_importance.png"
        filepath = self.output_dir / filename
        plt.savefig(filepath, dpi=300, bbox_inches='tight')
        print(f"✓ Feature importance plot saved to {filepath}")
        plt.close()
        
        # Print top features
        print(f"\nTop {min(10, top_n)} Most Important Features:")
        for i, (feat, score) in enumerate(zip(top_features[:10], top_scores[:10]), 1):
            print(f"  {i:2d}. {feat:30s} {score:.6f}")
