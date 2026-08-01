# Peptide Toxicity Prediction

Machine-learning project for classifying peptide sequences as toxic or non-toxic. The pipeline extracts sequence and physicochemical features, trains several classical models and records evaluation and interpretation artifacts.

The repository also contains a Vue interface and a NestJS API for submitting sequences and browsing prediction history.

## Pipeline

1. Load and clean peptide datasets.
2. Remove duplicate or highly similar sequences.
3. Extract amino-acid composition and physicochemical features.
4. Train logistic regression, random forest and SVM models.
5. Evaluate on held-out data.
6. Export metrics, plots and trained models.

Available features include sequence length, molecular weight, charge, hydrophobicity, isoelectric point, amino-acid composition and optional dipeptide composition.

## Repository map

| Path | Contents |
| --- | --- |
| `src/` | data loading, features, models, evaluation and interpretation |
| `scripts/` | dataset preparation, training, prediction and export tools |
| `backend/` | NestJS API with SQLite storage |
| `frontend/` | Vue 3 interface |
| `docker/` | Dockerfiles and Compose configuration |
| `docs/` | installation and dataset notes |

## Run with Docker

```bash
cd docker
docker compose up --build
```

## Run the ML pipeline

```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
python scripts/download_and_prepare_data.py
python scripts/train_pipeline.py
```

Use `python scripts/predict_new.py` for predictions from the command line.

## Run the web application

API:

```bash
cd backend
npm install
npm run start:dev
```

Interface:

```bash
cd frontend
npm install
npm run dev
```

The frontend runs at <http://localhost:5173>. API documentation is available through the NestJS Swagger route when the backend is running.

## Data

Training data is not treated as source code. See [`docs/HOW_TO_ADD_YOUR_OWN_DATA.md`](docs/HOW_TO_ADD_YOUR_OWN_DATA.md) and [`scripts/DATA_DOWNLOAD_README.md`](scripts/DATA_DOWNLOAD_README.md) for the expected formats and preparation steps.

Keep the test split isolated from model selection. Dataset origin, class balance and sequence-similarity filtering should be recorded with every reported result.
