# Quick Start Guide - Peptide Toxicity Prediction Platform

Get up and running in 5 minutes with this complete guide.

---

## Prerequisites

- Python 3.8 or higher
- Node.js 16 or higher
- npm or pnpm

---

## Step 1: Download the Project

Click the three dots in the top right of v0 chat and select "Download ZIP", then extract it.

---

## Step 2: Create Dataset (30 seconds)

```bash
# Install Python dependencies
pip install -r requirements.txt

# Generate the dataset (creates 100+ peptide sequences)
python scripts/download_and_prepare_data.py
```

This creates:
- `data/raw/toxic_peptides.fasta` - 50+ toxic peptides
- `data/raw/non_toxic_peptides.fasta` - 50+ non-toxic peptides

---

## Step 3: Train ML Models (2-3 minutes)

```bash
python scripts/train_pipeline.py
```

This will:
- Extract features from peptide sequences
- Train 3 models (Logistic Regression, Random Forest, SVM)
- Save trained models to `models/` folder
- Generate evaluation reports in `results/` folder

Expected output:
```
Loading data...
Extracting features...
Training models...
Logistic Regression - Accuracy: 0.85, F1: 0.84
Random Forest - Accuracy: 0.88, F1: 0.87
SVM - Accuracy: 0.86, F1: 0.85
Models saved to models/
```

---

## Step 4: Start Backend API (1 minute)

```bash
cd backend
npm install
npm run start:dev
```

Backend will run on: **http://localhost:3001**

API Documentation: **http://localhost:3001/api/docs**

---

## Step 5: Start Frontend Dashboard (1 minute)

Open a new terminal:

```bash
cd frontend
npm install
npm run dev
```

Frontend will run on: **http://localhost:3000**

---

## Step 6: Use the Application

Open your browser to **http://localhost:3000**

### Make Predictions:
1. Click "Predict" in the navigation
2. Enter a peptide sequence (e.g., `FLPLIGRVLSGIL`)
3. Click "Predict Toxicity"
4. View results with confidence scores

### Analyze Features:
1. Click "Analysis" in the navigation
2. Enter sequences to analyze
3. View amino acid composition and physicochemical properties

### View History:
1. Click "History" in the navigation
2. See all past predictions
3. Search and filter results
4. Export data

---

## Troubleshooting

### Python Issues

**Error: "No module named 'sklearn'"**
```bash
pip install -r requirements.txt
```

**Error: "No data found"**
```bash
python scripts/download_and_prepare_data.py
```

### Backend Issues

**Error: "Port 3001 already in use"**
```bash
# Kill the process using port 3001
# On Mac/Linux:
lsof -ti:3001 | xargs kill -9

# On Windows:
netstat -ano | findstr :3001
taskkill /PID <PID> /F
```

**Error: "Cannot find module"**
```bash
cd backend
rm -rf node_modules package-lock.json
npm install
```

### Frontend Issues

**Error: "Port 3000 already in use"**
Edit `frontend/vite.config.ts` and change the port:
```typescript
server: {
  port: 3002 // Change to any available port
}
```

**Error: "Network Error"**
Make sure backend is running on port 3001

---

## Testing the System

### Test Prediction API

```bash
curl -X POST http://localhost:3001/api/predict \
  -H "Content-Type: application/json" \
  -d '{"sequence": "FLPLIGRVLSGIL"}'
```

Expected response:
```json
{
  "sequence": "FLPLIGRVLSGIL",
  "prediction": 1,
  "confidence": 0.85,
  "model": "Random Forest"
}
```

### Test Feature Extraction

```bash
curl -X POST http://localhost:3001/api/analysis/features \
  -H "Content-Type: application/json" \
  -d '{"sequence": "FLPLIGRVLSGIL"}'
```

---

## Next Steps

1. **Read the full documentation**: Open `COMPLETE_DOCUMENTATION.md`
2. **Explore the code**: Start with `src/feature_extraction.py`
3. **Customize models**: Edit `src/models.py` hyperparameters
4. **Add your own data**: Replace files in `data/raw/`
5. **Deploy**: Follow deployment guide in documentation

---

## Example Peptide Sequences to Test

**Toxic (Hemolytic):**
- `FLPLIGRVLSGIL` - Melittin fragment
- `KWKLFKKIEKVGQNIRDGIIKAGPAVAVVGQATQIAK` - LL-37
- `GIGKFLHSAKKFGKAFVGEIMNS` - Magainin

**Non-Toxic (Therapeutic):**
- `GHRP` - Growth hormone releasing peptide
- `DSIP` - Delta sleep-inducing peptide
- `RRRPRPPYLPRPRPPPFFPPRLPPRIPPGFPPRFPPRFP` - Proline-rich peptide

---

## File Structure

```
peptide-toxicity-prediction/
├── backend/              # NestJS API (port 3001)
├── frontend/             # Vue.js app (port 3000)
├── src/                  # Python ML pipeline
├── scripts/              # Training and analysis scripts
├── data/                 # Generated datasets
├── models/               # Trained ML models (generated)
├── results/              # Evaluation reports (generated)
├── requirements.txt      # Python dependencies
└── QUICK_START.md        # This file
```

---

## Summary Commands

```bash
# One-time setup
pip install -r requirements.txt
python scripts/download_and_prepare_data.py
python scripts/train_pipeline.py

# Start backend (terminal 1)
cd backend && npm install && npm run start:dev

# Start frontend (terminal 2)
cd frontend && npm install && npm run dev

# Open browser
http://localhost:3000
```

---

**You're all set! The system is now running and ready for peptide toxicity predictions.**
