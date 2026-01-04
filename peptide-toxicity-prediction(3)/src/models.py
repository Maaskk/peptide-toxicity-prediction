"""
Machine learning models for peptide toxicity prediction.

Implements and trains multiple classification algorithms with hyperparameter tuning.
"""

import numpy as np
from typing import Dict, Tuple, Optional, Any
from sklearn.linear_model import LogisticRegression
from sklearn.ensemble import RandomForestClassifier
from sklearn.svm import SVC
from sklearn.preprocessing import StandardScaler
from sklearn.model_selection import GridSearchCV, cross_val_score
import joblib


class ToxicityPredictor:
    """
    Ensemble of ML models for peptide toxicity prediction.
    
    Implements three complementary algorithms:
    - Logistic Regression: Linear baseline with probabilistic interpretation
    - Random Forest: Non-linear ensemble with feature importance
    - SVM: Maximum margin classifier with kernel trick
    """
    
    def __init__(self):
        """Initialize model collection and preprocessing."""
        self.scaler = StandardScaler()
        self.models = {}
        self.best_params = {}
        self.trained = False
        
    def _get_logistic_regression(self) -> Tuple[LogisticRegression, Dict]:
        """
        Configure Logistic Regression with hyperparameter grid.
        
        LR is a linear model suitable for interpretable feature weights.
        Regularization (C parameter) controls model complexity.
        """
        model = LogisticRegression(random_state=42, max_iter=1000, class_weight='balanced')
        
        param_grid = {
            'C': [0.01, 0.1, 1.0, 10.0, 100.0],  # Regularization strength
            'penalty': ['l2'],
            'solver': ['lbfgs']
        }
        
        return model, param_grid
    
    def _get_random_forest(self) -> Tuple[RandomForestClassifier, Dict]:
        """
        Configure Random Forest with hyperparameter grid.
        
        RF builds ensemble of decision trees with bootstrap sampling.
        Provides feature importance and handles non-linear relationships.
        """
        model = RandomForestClassifier(random_state=42, class_weight='balanced')
        
        param_grid = {
            'n_estimators': [100, 200, 300],  # Number of trees
            'max_depth': [10, 20, 30, None],  # Tree depth
            'min_samples_split': [2, 5, 10],  # Minimum samples to split node
            'min_samples_leaf': [1, 2, 4]     # Minimum samples in leaf
        }
        
        return model, param_grid
    
    def _get_svm(self) -> Tuple[SVC, Dict]:
        """
        Configure Support Vector Machine with hyperparameter grid.
        
        SVM finds maximum margin hyperplane separating classes.
        RBF kernel allows non-linear decision boundaries.
        """
        model = SVC(random_state=42, probability=True, class_weight='balanced')
        
        param_grid = {
            'C': [0.1, 1.0, 10.0, 100.0],      # Regularization
            'gamma': ['scale', 'auto', 0.001, 0.01, 0.1],  # Kernel coefficient
            'kernel': ['rbf']                   # Radial basis function kernel
        }
        
        return model, param_grid
    
    def train(self, X_train: np.ndarray, y_train: np.ndarray, 
              X_val: np.ndarray, y_val: np.ndarray,
              cv_folds: int = 5) -> Dict[str, Any]:
        """
        Train all models with hyperparameter tuning.
        
        Uses grid search with cross-validation to find optimal hyperparameters.
        Each model is tuned independently on the validation set.
        
        Args:
            X_train: Training features
            y_train: Training labels
            X_val: Validation features
            y_val: Validation labels
            cv_folds: Number of cross-validation folds
            
        Returns:
            Dictionary of training results and metrics
        """
        print("\n" + "="*70)
        print("TRAINING MACHINE LEARNING MODELS")
        print("="*70)
        
        # Standardize features (critical for SVM and LR)
        # Scaling ensures all features have zero mean and unit variance
        print("\nStandardizing features...")
        X_train_scaled = self.scaler.fit_transform(X_train)
        X_val_scaled = self.scaler.transform(X_val)
        
        print(f"Training set: {X_train_scaled.shape[0]} samples")
        print(f"Validation set: {X_val_scaled.shape[0]} samples")
        print(f"Feature dimensionality: {X_train_scaled.shape[1]}")
        
        results = {}
        
        # Define models to train
        model_configs = {
            'Logistic Regression': self._get_logistic_regression(),
            'Random Forest': self._get_random_forest(),
            'SVM': self._get_svm()
        }
        
        for model_name, (base_model, param_grid) in model_configs.items():
            print(f"\n{'='*70}")
            print(f"Training: {model_name}")
            print(f"{'='*70}")
            
            # Grid search with cross-validation
            print(f"Hyperparameter search space: {len(list(self._param_combinations(param_grid)))} combinations")
            
            grid_search = GridSearchCV(
                estimator=base_model,
                param_grid=param_grid,
                cv=cv_folds,
                scoring='f1',  # F1 is balanced metric for imbalanced datasets
                n_jobs=-1,      # Use all CPU cores
                verbose=1
            )
            
            # Fit on training data
            grid_search.fit(X_train_scaled, y_train)
            
            # Store best model
            best_model = grid_search.best_estimator_
            self.models[model_name] = best_model
            self.best_params[model_name] = grid_search.best_params_
            
            # Cross-validation score
            cv_scores = cross_val_score(best_model, X_train_scaled, y_train, 
                                       cv=cv_folds, scoring='f1')
            
            # Validation performance
            val_score = best_model.score(X_val_scaled, y_val)
            
            results[model_name] = {
                'best_params': grid_search.best_params_,
                'cv_mean_f1': cv_scores.mean(),
                'cv_std_f1': cv_scores.std(),
                'val_accuracy': val_score,
                'best_cv_f1': grid_search.best_score_
            }
            
            print(f"\n✓ Best parameters: {grid_search.best_params_}")
            print(f"✓ Cross-validation F1: {cv_scores.mean():.4f} (+/- {cv_scores.std():.4f})")
            print(f"✓ Validation accuracy: {val_score:.4f}")
        
        self.trained = True
        
        print("\n" + "="*70)
        print("TRAINING COMPLETE")
        print("="*70 + "\n")
        
        return results
    
    def predict(self, X: np.ndarray, model_name: str = 'Random Forest') -> np.ndarray:
        """
        Make predictions using specified model.
        
        Args:
            X: Feature matrix
            model_name: Name of model to use for prediction
            
        Returns:
            Binary predictions (0=non-toxic, 1=toxic)
        """
        if not self.trained:
            raise ValueError("Models must be trained before making predictions")
        
        if model_name not in self.models:
            raise ValueError(f"Model '{model_name}' not found. Available: {list(self.models.keys())}")
        
        X_scaled = self.scaler.transform(X)
        return self.models[model_name].predict(X_scaled)
    
    def predict_proba(self, X: np.ndarray, model_name: str = 'Random Forest') -> np.ndarray:
        """
        Predict class probabilities.
        
        Args:
            X: Feature matrix
            model_name: Name of model to use
            
        Returns:
            Probability matrix of shape (n_samples, 2)
        """
        if not self.trained:
            raise ValueError("Models must be trained before making predictions")
        
        if model_name not in self.models:
            raise ValueError(f"Model '{model_name}' not found")
        
        X_scaled = self.scaler.transform(X)
        return self.models[model_name].predict_proba(X_scaled)
    
    def get_feature_importance(self, model_name: str = 'Random Forest', 
                              feature_names: Optional[list] = None) -> np.ndarray:
        """
        Extract feature importance from trained model.
        
        Only works for Random Forest (inherent feature importance) and 
        Logistic Regression (coefficient magnitudes).
        
        Args:
            model_name: Name of model
            feature_names: Optional list of feature names
            
        Returns:
            Array of feature importance scores
        """
        if not self.trained:
            raise ValueError("Models must be trained first")
        
        model = self.models[model_name]
        
        if model_name == 'Random Forest':
            return model.feature_importances_
        elif model_name == 'Logistic Regression':
            # Use absolute coefficient values as importance
            return np.abs(model.coef_[0])
        else:
            print(f"Feature importance not available for {model_name}")
            return None
    
    def save_models(self, filepath: str):
        """Save trained models and scaler to disk."""
        if not self.trained:
            raise ValueError("No trained models to save")
        
        joblib.dump({
            'models': self.models,
            'scaler': self.scaler,
            'best_params': self.best_params
        }, filepath)
        print(f"Models saved to {filepath}")
    
    def load_models(self, filepath: str):
        """Load trained models from disk."""
        data = joblib.load(filepath)
        self.models = data['models']
        self.scaler = data['scaler']
        self.best_params = data['best_params']
        self.trained = True
        print(f"Models loaded from {filepath}")
    
    def _param_combinations(self, param_grid: Dict) -> int:
        """Calculate total number of parameter combinations."""
        import itertools
        return itertools.product(*param_grid.values())
