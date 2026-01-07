# How to Run This Project

## Quick Start

### 1. Install Dependencies

```bash
# Create and activate virtual environment (recommended)
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install required packages
pip install -r requirements.txt
```

### 2. Prepare Your Data

⚠️ **IMPORTANT**: Replace the placeholder data loader with your actual data.

Edit `src/data_loader.py` to load your peptide sequences from FASTA files or CSV files. The loader should return three dictionaries (train, validation, test) with:

- `sequences`: List of amino acid sequences
- `labels`: Binary labels (0=non-toxic, 1=toxic)
- `source`: Data source name

### 3. Run Training Pipeline

```bash
python scripts/train_pipeline.py
```

This will:
- Load datasets
- Extract features (amino acid composition, physicochemical properties)
- Train three models (Logistic Regression, Random Forest, SVM)
- Tune hyperparameters using grid search + cross-validation
- Evaluate on test set
- Generate visualizations and biological interpretation
- Save results to `results/` directory

### 4. View Results

Check the `results/` directory for:
- `*.png` - Confusion matrices, ROC curves, feature importance plots
- `evaluation_results.json` - Detailed metrics
- `trained_models.pkl` - Saved models
- `pipeline.log` - Execution log

### 5. Predict New Sequences

```bash
python scripts/predict_new.py
```

Or modify the script to predict your own sequences.

## Expected Runtime

- Feature extraction: 1-5 minutes (depends on dataset size)
- Model training: 5-30 minutes (depends on hyperparameter grid)
- Evaluation: 1-2 minutes
- Total: ~10-40 minutes for complete pipeline

## Requirements

- Python 3.8+
- ~500MB disk space
- 4GB+ RAM recommended
- No GPU required

## Troubleshooting

**Error: "No module named 'Bio'"**
- Install BioPython: `pip install biopython`

**Error: "Cannot load datasets"**
- Replace placeholder in `src/data_loader.py` with your actual data loading code

**Warning: "Could not analyze sequence"**
- Some sequences contain non-standard amino acids. These are skipped with zeros.

**Models taking too long**
- Reduce hyperparameter grid in `src/models.py`
- Reduce cross-validation folds (default: 5)

## Output Files

```
results/
├── Logistic_Regression_confusion_matrix.png
├── Random_Forest_confusion_matrix.png
├── SVM_confusion_matrix.png
├── Logistic_Regression_roc_curve.png
├── Random_Forest_roc_curve.png
├── SVM_roc_curve.png
├── Random_Forest_feature_importance.png
├── Logistic_Regression_feature_importance.png
├── model_comparison_f1_score.png
├── model_comparison_roc_auc.png
├── aa_composition_comparison.png
├── physicochemical_distributions.png
├── length_distribution.png
├── evaluation_results.json
├── trained_models.pkl
└── pipeline.log
```

## Next Steps

1. **Analyze Results**: Review metrics, visualizations, and biological interpretations
2. **Tune Further**: Modify hyperparameters or feature configurations
3. **Deploy Model**: Use `predict_new.py` for production predictions
4. **Extend**: Add deep learning models, additional features, or external validation

---

**For questions, check `pipeline.log` or review the comprehensive documentation in `README.md`.**
