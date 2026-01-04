# Installation Guide

**👉 This is the main installation file. Follow these steps in order to get the project running.**

Complete step-by-step guide for running this project on your local machine.

## Prerequisites

Before you begin, ensure you have the following installed:

- **Python 3.8+** ([Download](https://www.python.org/downloads/))
- **Node.js 18+** ([Download](https://nodejs.org/))
- **npm** (comes with Node.js)

## Step 1: Clone the Repository

```bash
git clone https://github.com/yourusername/peptide-toxicity-prediction.git
cd peptide-toxicity-prediction
```

## Step 2: Set Up Python Environment

### Create Virtual Environment

```bash
# Create virtual environment
python -m venv venv

# Activate virtual environment
# On Windows:
venv\Scripts\activate
# On macOS/Linux:
source venv/bin/activate
```

### Install Python Dependencies

```bash
pip install -r requirements.txt
```

## Step 3: Prepare Data

### Download and Prepare Dataset

```bash
python scripts/download_and_prepare_data.py
```

This will download and prepare the peptide datasets needed for training.

## Step 4: Train the Models

Train the machine learning models (this may take several minutes):

```bash
python scripts/train_pipeline.py
```

This will:
- Load and process the datasets
- Extract features from peptide sequences
- Train three ML models (Logistic Regression, Random Forest, SVM)
- Save trained models to `results/trained_models.pkl`

**Note:** You can skip this step if you already have trained models. The app will use existing models if available.

## Step 5: Set Up Backend

### Install Backend Dependencies

```bash
cd backend
npm install
cd ..
```

### Start Backend Server

```bash
cd backend
npm run start:dev
```

The backend will run on `http://localhost:3000`

**Keep this terminal open** - the backend needs to keep running.

## Step 6: Set Up Frontend

Open a **new terminal window** and navigate to the project directory.

### Install Frontend Dependencies

```bash
cd frontend
npm install
```

### Start Frontend Development Server

```bash
npm run dev
```

The frontend will run on `http://localhost:5173` (or another port if 5173 is busy)

## Step 7: Access the Application

Open your browser and navigate to:

```
http://localhost:5173
```

You should see the Peptide Toxicity Prediction application!

## Usage

1. **Predict**: Enter a peptide sequence and click "Predict Toxicity"
2. **Analysis**: Analyze features of a peptide sequence
3. **History**: View your prediction history

## Troubleshooting

### Backend won't start

- Make sure Python 3 is installed and in your PATH
- Ensure all Python dependencies are installed: `pip install -r requirements.txt`
- Check that trained models exist in `results/trained_models.pkl` (or train them first)

### Frontend won't start

- Make sure Node.js 18+ is installed: `node --version`
- Clear node_modules and reinstall: `rm -rf node_modules && npm install`
- Check that the backend is running on port 3000

### Python script errors

- Activate your virtual environment: `source venv/bin/activate` (macOS/Linux) or `venv\Scripts\activate` (Windows)
- Make sure all dependencies are installed: `pip install -r requirements.txt`

### Port already in use

- Backend: Change port in `backend/src/main.ts` (default: 3000)
- Frontend: Vite will automatically use the next available port

## Development Notes

- **Backend**: NestJS framework, runs on port 3000
- **Frontend**: Vue.js 3 with Vite, runs on port 5173
- **Models**: Saved in `results/trained_models.pkl`
- **Database**: SQLite database at `backend/data/predictions.db`

## Stopping the Application

1. Press `Ctrl+C` in both terminal windows (backend and frontend)
2. Deactivate Python virtual environment: `deactivate`

## Need Help?

- Check the **Troubleshooting** section above
- Read `README.md` for project overview
- Make sure you followed all steps in order
- Verify all prerequisites are installed correctly

## What's Next?

After installation:
- ✅ Backend running on `http://localhost:3000`
- ✅ Frontend running on `http://localhost:5173`
- ✅ Open browser and start using the app!

**Tip:** Keep both terminals open (backend and frontend). Press `Ctrl+C` to stop each server.

