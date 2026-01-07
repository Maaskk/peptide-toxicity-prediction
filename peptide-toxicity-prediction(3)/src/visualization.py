"""
Visualization module for peptide analysis
Creates professional charts and plots for results interpretation
"""
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np
from pathlib import Path


def create_prediction_distribution(predictions, labels, save_path='results/prediction_distribution.png'):
    """
    Create distribution plot of predictions
    
    Args:
        predictions: Array of prediction probabilities
        labels: True labels
        save_path: Path to save the plot
    """
    fig, axes = plt.subplots(1, 2, figsize=(12, 5))
    
    # Prediction probability distribution
    toxic_probs = predictions[labels == 1]
    non_toxic_probs = predictions[labels == 0]
    
    axes[0].hist(toxic_probs, bins=30, alpha=0.6, label='Toxic', color='red', edgecolor='black')
    axes[0].hist(non_toxic_probs, bins=30, alpha=0.6, label='Non-Toxic', color='green', edgecolor='black')
    axes[0].set_xlabel('Prediction Probability')
    axes[0].set_ylabel('Frequency')
    axes[0].set_title('Prediction Probability Distribution')
    axes[0].legend()
    axes[0].grid(alpha=0.3)
    
    # Class distribution
    class_counts = [np.sum(labels == 0), np.sum(labels == 1)]
    axes[1].bar(['Non-Toxic', 'Toxic'], class_counts, color=['green', 'red'], alpha=0.7, edgecolor='black')
    axes[1].set_ylabel('Count')
    axes[1].set_title('Class Distribution')
    axes[1].grid(alpha=0.3, axis='y')
    
    plt.tight_layout()
    plt.savefig(save_path, dpi=300, bbox_inches='tight')
    plt.close()


def create_feature_correlation_heatmap(features, feature_names, save_path='results/feature_correlation.png'):
    """
    Create correlation heatmap of features
    
    Args:
        features: Feature matrix
        feature_names: List of feature names
        save_path: Path to save the plot
    """
    # Calculate correlation matrix
    correlation_matrix = np.corrcoef(features.T)
    
    fig, ax = plt.subplots(figsize=(12, 10))
    
    # Create heatmap
    sns.heatmap(
        correlation_matrix,
        xticklabels=feature_names,
        yticklabels=feature_names,
        cmap='coolwarm',
        center=0,
        vmin=-1,
        vmax=1,
        square=True,
        linewidths=0.5,
        cbar_kws={'label': 'Correlation Coefficient'},
        ax=ax
    )
    
    plt.title('Feature Correlation Matrix', fontsize=14, pad=20)
    plt.xticks(rotation=45, ha='right', fontsize=8)
    plt.yticks(fontsize=8)
    plt.tight_layout()
    plt.savefig(save_path, dpi=300, bbox_inches='tight')
    plt.close()


def create_amino_acid_importance_plot(aac_importance, save_path='results/aa_importance.png'):
    """
    Create bar plot showing amino acid importance
    
    Args:
        aac_importance: Dictionary of amino acid importance scores
        save_path: Path to save the plot
    """
    amino_acids = list(aac_importance.keys())
    importance = list(aac_importance.values())
    
    # Sort by importance
    sorted_pairs = sorted(zip(amino_acids, importance), key=lambda x: x[1], reverse=True)
    amino_acids, importance = zip(*sorted_pairs)
    
    fig, ax = plt.subplots(figsize=(12, 6))
    
    colors = ['red' if imp > 0 else 'blue' for imp in importance]
    bars = ax.barh(amino_acids, importance, color=colors, alpha=0.7, edgecolor='black')
    
    ax.set_xlabel('Feature Importance', fontsize=12)
    ax.set_ylabel('Amino Acid', fontsize=12)
    ax.set_title('Amino Acid Contribution to Toxicity Prediction', fontsize=14, pad=20)
    ax.axvline(x=0, color='black', linestyle='-', linewidth=0.8)
    ax.grid(alpha=0.3, axis='x')
    
    # Add value labels
    for i, (aa, imp) in enumerate(zip(amino_acids, importance)):
        ax.text(imp + 0.001, i, f'{imp:.4f}', va='center', fontsize=9)
    
    plt.tight_layout()
    plt.savefig(save_path, dpi=300, bbox_inches='tight')
    plt.close()


def create_physicochemical_comparison(toxic_properties, non_toxic_properties, save_path='results/physicochemical_comparison.png'):
    """
    Create comparison plots for physicochemical properties
    
    Args:
        toxic_properties: Dict of properties for toxic peptides
        non_toxic_properties: Dict of properties for non-toxic peptides
        save_path: Path to save the plot
    """
    properties = list(toxic_properties.keys())
    
    fig, axes = plt.subplots(2, 2, figsize=(14, 10))
    axes = axes.flatten()
    
    for idx, prop in enumerate(properties[:4]):
        ax = axes[idx]
        
        toxic_vals = toxic_properties[prop]
        non_toxic_vals = non_toxic_properties[prop]
        
        # Create violin plot
        data = [toxic_vals, non_toxic_vals]
        positions = [1, 2]
        
        parts = ax.violinplot(data, positions=positions, showmeans=True, showmedians=True)
        
        # Color the violins
        for pc in parts['bodies']:
            pc.set_facecolor('red')
            pc.set_alpha(0.3)
        
        parts['bodies'][1].set_facecolor('green')
        
        ax.set_xticks(positions)
        ax.set_xticklabels(['Toxic', 'Non-Toxic'])
        ax.set_ylabel('Value')
        ax.set_title(prop.replace('_', ' ').title())
        ax.grid(alpha=0.3, axis='y')
    
    plt.suptitle('Physicochemical Property Comparison', fontsize=16, y=1.00)
    plt.tight_layout()
    plt.savefig(save_path, dpi=300, bbox_inches='tight')
    plt.close()


def create_model_comparison_chart(model_metrics, save_path='results/model_comparison.png'):
    """
    Create comparison chart for different models
    
    Args:
        model_metrics: Dictionary of model names and their metrics
        save_path: Path to save the plot
    """
    models = list(model_metrics.keys())
    metrics = ['Accuracy', 'Precision', 'Recall', 'F1-Score']
    
    fig, ax = plt.subplots(figsize=(12, 6))
    
    x = np.arange(len(models))
    width = 0.2
    
    for idx, metric in enumerate(metrics):
        values = [model_metrics[model][metric] for model in models]
        ax.bar(x + idx * width, values, width, label=metric, alpha=0.8, edgecolor='black')
    
    ax.set_xlabel('Model', fontsize=12)
    ax.set_ylabel('Score', fontsize=12)
    ax.set_title('Model Performance Comparison', fontsize=14, pad=20)
    ax.set_xticks(x + width * 1.5)
    ax.set_xticklabels(models, rotation=15, ha='right')
    ax.legend(loc='lower right')
    ax.set_ylim([0, 1.1])
    ax.grid(alpha=0.3, axis='y')
    
    plt.tight_layout()
    plt.savefig(save_path, dpi=300, bbox_inches='tight')
    plt.close()


def create_confidence_calibration_plot(y_true, y_pred_proba, save_path='results/calibration_plot.png'):
    """
    Create calibration plot to assess prediction confidence
    
    Args:
        y_true: True labels
        y_pred_proba: Predicted probabilities
        save_path: Path to save the plot
    """
    from sklearn.calibration import calibration_curve
    
    fig, axes = plt.subplots(1, 2, figsize=(14, 6))
    
    # Calibration curve
    fraction_of_positives, mean_predicted_value = calibration_curve(
        y_true, y_pred_proba, n_bins=10, strategy='uniform'
    )
    
    axes[0].plot([0, 1], [0, 1], 'k--', label='Perfectly calibrated', linewidth=2)
    axes[0].plot(mean_predicted_value, fraction_of_positives, 'o-', label='Model', linewidth=2, markersize=8)
    axes[0].set_xlabel('Mean Predicted Probability')
    axes[0].set_ylabel('Fraction of Positives')
    axes[0].set_title('Calibration Curve')
    axes[0].legend()
    axes[0].grid(alpha=0.3)
    
    # Confidence distribution
    axes[1].hist(y_pred_proba, bins=30, alpha=0.7, color='blue', edgecolor='black')
    axes[1].set_xlabel('Predicted Probability')
    axes[1].set_ylabel('Frequency')
    axes[1].set_title('Confidence Distribution')
    axes[1].grid(alpha=0.3, axis='y')
    
    plt.tight_layout()
    plt.savefig(save_path, dpi=300, bbox_inches='tight')
    plt.close()


def create_length_analysis_plot(sequences_toxic, sequences_non_toxic, save_path='results/length_analysis.png'):
    """
    Analyze peptide length distribution
    
    Args:
        sequences_toxic: List of toxic sequences
        sequences_non_toxic: List of non-toxic sequences
        save_path: Path to save the plot
    """
    lengths_toxic = [len(seq) for seq in sequences_toxic]
    lengths_non_toxic = [len(seq) for seq in sequences_non_toxic]
    
    fig, axes = plt.subplots(1, 2, figsize=(14, 6))
    
    # Histogram
    axes[0].hist(lengths_toxic, bins=20, alpha=0.6, label='Toxic', color='red', edgecolor='black')
    axes[0].hist(lengths_non_toxic, bins=20, alpha=0.6, label='Non-Toxic', color='green', edgecolor='black')
    axes[0].set_xlabel('Peptide Length (amino acids)')
    axes[0].set_ylabel('Frequency')
    axes[0].set_title('Peptide Length Distribution')
    axes[0].legend()
    axes[0].grid(alpha=0.3, axis='y')
    
    # Box plot
    data = [lengths_toxic, lengths_non_toxic]
    bp = axes[1].boxplot(data, labels=['Toxic', 'Non-Toxic'], patch_artist=True)
    bp['boxes'][0].set_facecolor('red')
    bp['boxes'][0].set_alpha(0.3)
    bp['boxes'][1].set_facecolor('green')
    bp['boxes'][1].set_alpha(0.3)
    axes[1].set_ylabel('Peptide Length (amino acids)')
    axes[1].set_title('Length Distribution by Class')
    axes[1].grid(alpha=0.3, axis='y')
    
    plt.tight_layout()
    plt.savefig(save_path, dpi=300, bbox_inches='tight')
    plt.close()


def create_comprehensive_report(
    predictions,
    labels,
    features,
    feature_names,
    model_metrics,
    sequences,
    output_dir='results/visualizations'
):
    """
    Create comprehensive visual report
    
    Args:
        predictions: Prediction probabilities
        labels: True labels
        features: Feature matrix
        feature_names: Feature names
        model_metrics: Model performance metrics
        sequences: Original sequences
        output_dir: Directory to save visualizations
    """
    Path(output_dir).mkdir(parents=True, exist_ok=True)
    
    print("Generating comprehensive visual report...")
    
    # Prediction distribution
    create_prediction_distribution(
        predictions, 
        labels, 
        f'{output_dir}/prediction_distribution.png'
    )
    
    # Model comparison
    create_model_comparison_chart(
        model_metrics,
        f'{output_dir}/model_comparison.png'
    )
    
    # Calibration plot
    create_confidence_calibration_plot(
        labels,
        predictions,
        f'{output_dir}/calibration_plot.png'
    )
    
    # Length analysis
    toxic_sequences = [seq for seq, label in zip(sequences, labels) if label == 1]
    non_toxic_sequences = [seq for seq, label in zip(sequences, labels) if label == 0]
    
    create_length_analysis_plot(
        toxic_sequences,
        non_toxic_sequences,
        f'{output_dir}/length_analysis.png'
    )
    
    print(f"Visual report saved to {output_dir}/")
