# 👋 START HERE - Installation Guide

**Welcome! This is the main file you should follow to install and run this project.**

## 📋 What to Follow (In Order)

### For First-Time Users:
1. **Read this file** (`START_HERE.md`) - You're here! ✅
2. **Follow [INSTALLATION.md](INSTALLATION.md)** - Complete step-by-step installation guide
3. **Check [README.md](README.md)** - Project overview and features

### Quick Links:
- 📦 **Installation**: [INSTALLATION.md](INSTALLATION.md) ← **START HERE**
- 📖 **Project Info**: [README.md](README.md)
- 🚀 **GitHub Setup**: [GITHUB_SETUP.md](GITHUB_SETUP.md) (only if uploading to GitHub)

---

## 🎯 Installation Steps Overview

Follow these steps in order:

### Step 1: Prerequisites
- Install Python 3.8+ from [python.org](https://www.python.org/downloads/)
- Install Node.js 18+ from [nodejs.org](https://nodejs.org/)

### Step 2: Clone & Setup
- Clone the repository
- Create Python virtual environment
- Install Python dependencies

### Step 3: Prepare Data
- Download and prepare datasets

### Step 4: Train Models (Optional)
- Train ML models (or skip if models already exist)

### Step 5: Run Backend
- Install backend dependencies
- Start backend server

### Step 6: Run Frontend
- Install frontend dependencies  
- Start frontend server

### Step 7: Use the App!
- Open browser to `http://localhost:5173`

---

## 📁 Which Files to Read?

### ✅ Must Read:
- **[INSTALLATION.md](INSTALLATION.md)** - Complete installation instructions
- **[README.md](README.md)** - Project overview

### ⚠️ Optional:
- **[GITHUB_SETUP.md](GITHUB_SETUP.md)** - Only if you want to upload to GitHub

### ❌ Don't Worry About:
- `LEARNING_GUIDE.md` - Learning resource (not needed to run)
- `COMPLETE_DOCUMENTATION.md` - Detailed docs (not needed to run)
- `COMPLETE_SETUP_GUIDE.md` - Alternative guide (use INSTALLATION.md instead)
- `DATA_SETUP.md` - Data preparation (covered in INSTALLATION.md)

---

## 🚀 Quick Start (Experienced Users)

If you're experienced with Python and Node.js:

```bash
# 1. Clone
git clone https://github.com/yourusername/peptide-toxicity-prediction.git
cd peptide-toxicity-prediction

# 2. Python setup
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate
pip install -r requirements.txt

# 3. Data
python scripts/download_and_prepare_data.py

# 4. Train (optional)
python scripts/train_pipeline.py

# 5. Backend (Terminal 1)
cd backend && npm install && npm run start:dev

# 6. Frontend (Terminal 2)
cd frontend && npm install && npm run dev

# 7. Open browser
# http://localhost:5173
```

---

## ❓ Need Help?

1. **Installation issues?** → Check [INSTALLATION.md](INSTALLATION.md) Troubleshooting section
2. **Project questions?** → Read [README.md](README.md)
3. **Still stuck?** → Check the error messages and make sure:
   - Python 3.8+ is installed
   - Node.js 18+ is installed
   - All dependencies are installed
   - Backend is running before starting frontend

---

## ✅ What's Next?

👉 **Go to [INSTALLATION.md](INSTALLATION.md) and follow it step by step!**

Good luck! 🎉

