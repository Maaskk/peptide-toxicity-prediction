"""
Model interpretability and explainability module
Provides insights into model decisions and feature importance
"""
import numpy as np
import shap
import lime
import lime.lime_tabular
from sklearn.inspection import permutation_importance
import matplotlib.pyplot as plt


class ModelInterpreter:
    """
    Comprehensive model interpretation class
    """
    
    def __init__(self, model, feature_names, X_train, y_train):
        """
        Initialize interpreter
        
        Args:
            model: Trained model
            feature_names: List of feature names
            X_train: Training features
            y_train: Training labels
        """
        self.model = model
        self.feature_names = feature_names
        self.X_train = X_train
        self.y_train = y_train
        
    def get_feature_importance(self, X_test, y_test, method='permutation'):
        """
        Calculate feature importance
        
        Args:
            X_test: Test features
            y_test: Test labels
            method: 'permutation', 'shap', or 'native'
        
        Returns:
            Dictionary of feature importances
        """
        if method == 'permutation':
            result = permutation_importance(
                self.model, X_test, y_test,
                n_repeats=10,
                random_state=42,
                n_jobs=-1
            )
            importances = result.importances_mean
            
        elif method == 'native' and hasattr(self.model, 'feature_importances_'):
            importances = self.model.feature_importances_
            
        elif method == 'native' and hasattr(self.model, 'coef_'):
            importances = np.abs(self.model.coef_[0])
            
        else:
            raise ValueError(f"Method {method} not supported for this model")
        
        # Create importance dictionary
        feature_importance = dict(zip(self.feature_names, importances))
        
        # Sort by importance
        feature_importance = dict(
            sorted(feature_importance.items(), key=lambda x: x[1], reverse=True)
        )
        
        return feature_importance
    
    def explain_prediction_lime(self, instance, num_features=10):
        """
        Explain single prediction using LIME
        
        Args:
            instance: Single instance to explain
            num_features: Number of top features to show
        
        Returns:
            LIME explanation object
        """
        explainer = lime.lime_tabular.LimeTabularExplainer(
            self.X_train,
            feature_names=self.feature_names,
            class_names=['Non-Toxic', 'Toxic'],
            mode='classification'
        )
        
        explanation = explainer.explain_instance(
            instance,
            self.model.predict_proba,
            num_features=num_features
        )
        
        return explanation
    
    def explain_prediction_shap(self, instances, plot=True, save_path=None):
        """
        Explain predictions using SHAP
        
        Args:
            instances: Instances to explain
            plot: Whether to create SHAP plots
            save_path: Path to save plots
        
        Returns:
            SHAP values
        """
        # Create SHAP explainer
        explainer = shap.TreeExplainer(self.model) if hasattr(self.model, 'tree_') else shap.KernelExplainer(
            self.model.predict_proba,
            shap.sample(self.X_train, 100)
        )
        
        # Calculate SHAP values
        shap_values = explainer.shap_values(instances)
        
        if plot:
            # Summary plot
            plt.figure(figsize=(10, 8))
            shap.summary_plot(
                shap_values,
                instances,
                feature_names=self.feature_names,
                show=False
            )
            if save_path:
                plt.savefig(f'{save_path}/shap_summary.png', dpi=300, bbox_inches='tight')
            plt.close()
            
            # Force plot for first instance
            if len(instances) > 0:
                shap.force_plot(
                    explainer.expected_value[1],
                    shap_values[1][0],
                    instances[0],
                    feature_names=self.feature_names,
                    matplotlib=True,
                    show=False
                )
                if save_path:
                    plt.savefig(f'{save_path}/shap_force.png', dpi=300, bbox_inches='tight')
                plt.close()
        
        return shap_values
    
    def get_decision_boundary_analysis(self, feature_idx1, feature_idx2, resolution=100):
        """
        Analyze decision boundary for two features
        
        Args:
            feature_idx1: Index of first feature
            feature_idx2: Index of second feature
            resolution: Grid resolution
        
        Returns:
            Grid coordinates and predictions
        """
        # Get feature ranges
        x1_min, x1_max = self.X_train[:, feature_idx1].min(), self.X_train[:, feature_idx1].max()
        x2_min, x2_max = self.X_train[:, feature_idx2].min(), self.X_train[:, feature_idx2].max()
        
        # Create grid
        xx1, xx2 = np.meshgrid(
            np.linspace(x1_min, x1_max, resolution),
            np.linspace(x2_min, x2_max, resolution)
        )
        
        # Create feature matrix with mean values for other features
        grid_features = np.tile(self.X_train.mean(axis=0), (resolution * resolution, 1))
        grid_features[:, feature_idx1] = xx1.ravel()
        grid_features[:, feature_idx2] = xx2.ravel()
        
        # Predict
        predictions = self.model.predict_proba(grid_features)[:, 1].reshape(xx1.shape)
        
        return xx1, xx2, predictions
    
    def get_top_discriminative_features(self, n=10):
        """
        Get top features that discriminate between classes
        
        Args:
            n: Number of top features
        
        Returns:
            List of feature names and scores
        """
        feature_importance = self.get_feature_importance(
            self.X_train,
            self.y_train,
            method='permutation'
        )
        
        top_features = list(feature_importance.items())[:n]
        
        return top_features
    
    def generate_interpretation_report(self, X_test, y_test, output_dir='results/interpretability'):
        """
        Generate comprehensive interpretation report
        
        Args:
            X_test: Test features
            y_test: Test labels
            output_dir: Output directory
        """
        from pathlib import Path
        Path(output_dir).mkdir(parents=True, exist_ok=True)
        
        print("Generating model interpretation report...")
        
        # Feature importance
        feature_importance = self.get_feature_importance(X_test, y_test)
        
        # Plot feature importance
        plt.figure(figsize=(12, 8))
        features = list(feature_importance.keys())[:20]
        importances = list(feature_importance.values())[:20]
        
        plt.barh(features, importances, color='skyblue', edgecolor='black')
        plt.xlabel('Importance')
        plt.title('Top 20 Feature Importance')
        plt.tight_layout()
        plt.savefig(f'{output_dir}/feature_importance.png', dpi=300, bbox_inches='tight')
        plt.close()
        
        # LIME explanation for sample predictions
        sample_indices = np.random.choice(len(X_test), min(5, len(X_test)), replace=False)
        
        for idx, sample_idx in enumerate(sample_indices):
            explanation = self.explain_prediction_lime(X_test[sample_idx])
            explanation.save_to_file(f'{output_dir}/lime_explanation_{idx}.html')
        
        # Save report
        with open(f'{output_dir}/interpretation_report.txt', 'w') as f:
            f.write("=== Model Interpretation Report ===\n\n")
            f.write("Top 20 Most Important Features:\n")
            for i, (feature, importance) in enumerate(list(feature_importance.items())[:20], 1):
                f.write(f"{i}. {feature}: {importance:.6f}\n")
            f.write(f"\nDetailed explanations saved to {output_dir}/\n")
        
        print(f"Interpretation report saved to {output_dir}/")
        
        return feature_importance
