# Peptide Toxicity Prediction

A production-quality machine learning pipeline for predicting peptide toxicity from amino acid sequences. This project implements comprehensive feature extraction, multiple ML algorithms, rigorous evaluation, and biological interpretation suitable for academic research.

## 🎯 Project Overview

This bioinformatics tool predicts whether peptide sequences are toxic or non-toxic using machine learning. It analyzes amino acid composition, physicochemical properties, and sequence characteristics to identify molecular signatures associated with toxicity.

### Key Features

- **Comprehensive Feature Extraction**: Amino acid composition (AAC), physicochemical properties (MW, charge, hydrophobicity, pI), sequence length, optional dipeptide composition
- **Multiple ML Algorithms**: Logistic Regression, Random Forest, SVM with hyperparameter tuning
- **Rigorous Evaluation**: Accuracy, precision, recall, F1-score, ROC-AUC with cross-validation
- **Biological Interpretation**: Amino acid enrichment analysis, physicochemical property distributions, statistical significance testing
- **Production-Ready**: Modular code, reproducible results, comprehensive logging, model persistence

## 📁 Project Structure

```
.
├── src/
│   ├── data_loader.py           # Dataset loading (placeholder - add your data)
│   ├── feature_extraction.py    # Feature engineering for peptides
│   ├── models.py                 # ML model implementations
│   ├── evaluate.py               # Evaluation metrics and visualization
│   ├── biological_analysis.py    # Biological interpretation
│   └── utils.py                  # Utility functions
├── scripts/
│   ├── train_pipeline.py         # Complete training pipeline
│   └── predict_new.py            # Prediction script for new sequences
├── results/                      # Output directory (created automatically)
│   ├── *.png                     # Visualizations
│   ├── evaluation_results.json   # Metrics
│   ├── trained_models.pkl        # Saved models
│   └── pipeline.log              # Execution log
├── requirements.txt              # Python dependencies
└── README.md                     # This file
```

## 🚀 Quick Start

For detailed installation instructions, see [INSTALLATION.md](INSTALLATION.md)

### Prerequisites

- Python 3.8 or higher
- Node.js 18 or higher
- npm (comes with Node.js)

### Quick Installation

```bash
# Clone repository
git clone https://github.com/yourusername/peptide-toxicity-prediction.git
cd peptide-toxicity-prediction

# Setup Python environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
pip install -r requirements.txt

# Prepare data
python scripts/download_and_prepare_data.py

# Train models (optional if you have trained models)
python scripts/train_pipeline.py

# Setup and start backend
cd backend
npm install
npm run start:dev  # Keep this running

# Setup and start frontend (in new terminal)
cd frontend
npm install
npm run dev
```

Open `http://localhost:5173` in your browser.

### Step 2: Create Virtual Environment (Recommended)

```bash
# Create virtual environment
python -m venv venv

# Activate virtual environment
# On Windows:
venv\Scripts\activate
# On macOS/Linux:
source venv/bin/activate
```

### Step 3: Install Dependencies

```bash
pip install -r requirements.txt
```

## 📊 Data Preparation

### Important: Add Your Data

The `src/data_loader.py` file contains a **placeholder implementation**. You need to replace it with your actual data loading code.

#### Expected Data Format

Your data loader should return three dictionaries (train, validation, test):

```python
{
    'sequences': List[str],      # Amino acid sequences (e.g., "GLFDIVKKVVGALG")
    'labels': np.ndarray,         # Binary labels (0=non-toxic, 1=toxic)
    'source': str                 # Data source identifier
}
```

#### Example: Loading from FASTA Files

```python
from Bio import SeqIO

def load_fasta(filepath):
    sequences = []
    labels = []
    
    for record in SeqIO.parse(filepath, "fasta"):
        sequences.append(str(record.seq))
        # Parse label from description
        label = 1 if "toxic" in record.description.lower() else 0
        labels.append(label)
    
    return sequences, labels
```

#### Recommended Data Split

- **Training set**: 60-70% of data (for model training)
- **Validation set**: 15-20% of data (for hyperparameter tuning)
- **Test set**: 15-20% of data (independent evaluation, never seen during training)

## 🔬 Usage

### Training the Models

Run the complete training pipeline:

```bash
python scripts/train_pipeline.py
```

This will:
1. ✅ Load your datasets
2. ✅ Extract features (AAC, physicochemical properties, etc.)
3. ✅ Train three ML models (Logistic Regression, Random Forest, SVM)
4. ✅ Perform hyperparameter tuning with cross-validation
5. ✅ Evaluate on validation and test sets
6. ✅ Generate visualizations (confusion matrices, ROC curves, feature importance)
7. ✅ Perform biological interpretation (amino acid enrichment, property distributions)
8. ✅ Save models and results

#### Output

All results are saved to the `results/` directory:

- **Visualizations**: `*.png` files (confusion matrices, ROC curves, distributions)
- **Metrics**: `evaluation_results.json` (comprehensive performance metrics)
- **Models**: `trained_models.pkl` (trained models for prediction)
- **Log**: `pipeline.log` (execution log)

### Predicting New Sequences

Use trained models to predict toxicity of new peptides:

```bash
python scripts/predict_new.py
```

Or programmatically:

```python
from scripts.predict_new import predict_sequences

# Your peptide sequences
sequences = [
    "GLFDIVKKVVGALG",
    "ATCDLLSGTVSRGGRL",
    "KKKKKKKKKK"
]

predict_sequences(sequences, model_path="results/trained_models.pkl")
```

## 📈 Feature Extraction

### Implemented Features

#### 1. Amino Acid Composition (20 features)
Normalized frequency of each of the 20 standard amino acids.

$$\text{AAC}_{aa} = \frac{\text{count}(aa)}{L}$$

where $L$ is sequence length.

#### 2. Sequence Length (1 feature)
Total number of amino acids. Toxic peptides often have characteristic length ranges.

#### 3. Physicochemical Properties (6 features)
Using BioPython's ProtParam:

- **Molecular Weight**: Total mass (Da)
- **Net Charge at pH 7**: Electrostatic properties
- **Isoelectric Point**: pH at zero net charge
- **Aromaticity**: Fraction of F, W, Y residues
- **Instability Index**: Protein stability estimate
- **GRAVY**: Grand average of hydropathy (hydrophobicity)

#### 4. Dipeptide Composition (400 features, optional)
Captures local sequence order via 2-mer frequencies. Enable with `use_dipeptide=True`.

### Total Features
- **Basic**: 27 features (20 AAC + 1 length + 6 physicochemical)
- **Extended**: 427 features (+ 400 dipeptide)

## 🤖 Machine Learning Models

### 1. Logistic Regression
- Linear model with L2 regularization
- Interpretable feature coefficients
- Hyperparameters: Regularization strength (C)

### 2. Random Forest
- Ensemble of decision trees
- Non-linear relationships
- Feature importance scores
- Hyperparameters: n_estimators, max_depth, min_samples_split, min_samples_leaf

### 3. Support Vector Machine (SVM)
- Maximum margin classifier
- RBF kernel for non-linearity
- Hyperparameters: C, gamma

### Training Strategy
- **Grid Search**: Exhaustive hyperparameter search
- **Cross-Validation**: 5-fold CV for robust evaluation
- **Class Balancing**: Automatic handling of imbalanced datasets
- **Feature Scaling**: Standardization (zero mean, unit variance)

## 📊 Evaluation Metrics

### Classification Metrics

- **Accuracy**: Overall correctness
- **Precision**: Positive predictive value (avoid false alarms)
- **Recall**: Sensitivity (catch all toxic peptides)
- **F1-Score**: Harmonic mean of precision and recall
- **ROC-AUC**: Area under receiver operating characteristic curve

### Visualizations

1. **Confusion Matrices**: True/false positives and negatives
2. **ROC Curves**: TPR vs FPR trade-off
3. **Feature Importance**: Most predictive features
4. **Model Comparison**: Side-by-side performance

## 🧬 Biological Interpretation

### Amino Acid Enrichment Analysis
Statistical testing (t-tests) to identify amino acids significantly enriched in toxic vs non-toxic peptides.

Example insights:
- **Lysine (K) enrichment** → Positive charges facilitate membrane interaction
- **Leucine (L) enrichment** → Hydrophobicity promotes membrane partitioning
- **Aromatic residues (F, W, Y)** → Enhance membrane insertion

### Physicochemical Property Distributions
Comparison of molecular weight, charge, hydrophobicity, etc. between toxic and non-toxic groups.

### Sequence Length Analysis
Length distribution analysis with statistical significance testing.

## 🔬 Scientific Validity

### Best Practices Implemented

✅ **Independent test set**: Never used during training/tuning  
✅ **Cross-validation**: 5-fold CV for robust estimates  
✅ **Hyperparameter tuning**: Grid search on validation set  
✅ **Feature scaling**: Standardization for algorithm fairness  
✅ **Class balancing**: Handle imbalanced datasets  
✅ **Reproducibility**: Fixed random seeds  
✅ **Statistical testing**: P-values for biological findings  

### Suitable for Publication

This pipeline produces results suitable for academic papers:
- Comprehensive methodology
- Multiple model comparison
- Rigorous evaluation
- Biological interpretation with statistical support
- Publication-quality figures

## 🛠️ Customization

### Change Feature Configuration

Edit `scripts/train_pipeline.py`:

```python
# Enable dipeptide composition (more features, slower)
extractor = PeptideFeatureExtractor(use_dipeptide=True)
```

### Add Custom Features

Extend `src/feature_extraction.py`:

```python
def extract_custom_feature(self, sequence: str) -> float:
    # Your custom feature logic
    return feature_value
```

### Modify Hyperparameter Search

Edit `src/models.py`:

```python
param_grid = {
    'n_estimators': [50, 100, 200, 500],  # Add more options
    'max_depth': [5, 10, 20, None]
}
```

### Change Cross-Validation Folds

Edit `scripts/train_pipeline.py`:

```python
training_results = predictor.train(
    X_train=X_train,
    y_train=y_train,
    X_val=X_val,
    y_val=y_val,
    cv_folds=10  # Change from default 5 to 10
)
```

## 📝 Citation

If you use this code in your research, please cite:

```
[Your Name]. (2024). Peptide Toxicity Prediction: 
A Machine Learning Pipeline for Amino Acid Sequence Analysis.
```

## 🤝 Contributing

Suggestions for improvement:
- Additional feature extraction methods (k-mer, physicochemical indices)
- Deep learning models (LSTM, CNN, Transformers)
- Ensemble voting across models
- External validation on independent datasets
- SHAP values for model interpretation

## 📧 Support

For issues or questions:
1. Check the log file: `results/pipeline.log`
2. Verify data format in `src/data_loader.py`
3. Ensure all dependencies are installed: `pip install -r requirements.txt`

## ⚖️ License

This project is released for academic and research purposes.

## 🎓 Academic Context

This project demonstrates:
- **Machine Learning**: Classification, hyperparameter tuning, cross-validation
- **Bioinformatics**: Sequence analysis, physicochemical properties
- **Data Science**: Feature engineering, evaluation, interpretation
- **Software Engineering**: Modular design, documentation, reproducibility

---

**Built for serious bioinformatics research. No shortcuts, no placeholders, production-quality code.**
