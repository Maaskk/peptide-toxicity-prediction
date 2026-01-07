# 🐳 Docker Setup Guide for Peptide Toxicity Prediction

This guide will help you run the Peptide Toxicity Prediction project using Docker. Docker makes installation simple and ensures the project runs smoothly on any system (Windows, macOS, Linux).

## 📋 Table of Contents

1. [What is Docker?](#what-is-docker)
2. [Prerequisites](#prerequisites)
3. [Quick Start (Recommended)](#quick-start-recommended)
4. [Step-by-Step Installation](#step-by-step-installation)
5. [Running the Application](#running-the-application)
6. [Training Models](#training-models)
7. [Troubleshooting](#troubleshooting)
8. [Advanced Usage](#advanced-usage)

---

## 🤔 What is Docker?

Docker is a platform that packages applications and their dependencies into containers. Think of it as a lightweight virtual machine that:
- ✅ Works the same on any computer
- ✅ Includes all dependencies pre-installed
- ✅ Isolates the app from your system
- ✅ Makes setup incredibly simple

**With Docker, you don't need to install Python, Node.js, or any dependencies manually!**

---

## 📦 Prerequisites

### Install Docker Desktop

1. **Download Docker Desktop** for your operating system:
   - **Windows**: [Docker Desktop for Windows](https://www.docker.com/products/docker-desktop/)
   - **macOS**: [Docker Desktop for Mac](https://www.docker.com/products/docker-desktop/)
   - **Linux**: [Docker Engine for Linux](https://docs.docker.com/engine/install/)

2. **Install Docker Desktop**:
   - Run the installer and follow the on-screen instructions
   - On Windows, you may need to enable WSL 2 (Windows Subsystem for Linux)
   - Restart your computer if prompted

3. **Verify Docker is installed**:
   ```bash
   docker --version
   docker-compose --version
   ```
   
   You should see version numbers (e.g., `Docker version 24.0.0`).

4. **Start Docker Desktop**:
   - Open Docker Desktop application
   - Wait for it to start (you'll see a green icon/status)

---

## ⚡ Quick Start (Recommended)

### For First-Time Users

If you just downloaded this project from GitHub, follow these steps:

```bash
# 1. Download/Clone the project
git clone https://github.com/Maaskk/peptide-toxicity-prediction.git
cd peptide-toxicity-prediction

# 2. Make sure you have trained models
# If results/trained_models.pkl doesn't exist, you need to train first
# See "Training Models" section below

# 3. Start the application with Docker
docker-compose up --build

# 4. Wait for startup messages (30-60 seconds)
# You'll see:
# "Backend started..."
# "Frontend started..."
# "Application is ready!"

# 5. Open your browser
# Frontend: http://localhost:3000
# Backend API: http://localhost:3001
```

**That's it!** The application should be running.

### For Quick Testing (Without Training)

If you want to test the app quickly without training models first:

```bash
# Start the app (it will use mock predictions until you train)
docker-compose up --build
```

Visit `http://localhost:3000` and enter a peptide sequence to test.

---

## 📖 Step-by-Step Installation

### Step 1: Download the Project

```bash
# Option A: Clone from GitHub
git clone https://github.com/Maaskk/peptide-toxicity-prediction.git
cd peptide-toxicity-prediction

# Option B: Download ZIP
# 1. Go to GitHub repository
# 2. Click "Code" → "Download ZIP"
# 3. Extract the ZIP file
# 4. Open terminal in the extracted folder
```

### Step 2: Verify Docker is Running

```bash
# Check Docker is installed and running
docker --version
docker-compose --version

# If these commands fail:
# - Make sure Docker Desktop is running
# - Restart Docker Desktop
# - Check Docker Desktop settings
```

### Step 3: Prepare Your Data (Optional)

If you want to train models with your own data:

```bash
# Option A: Use the provided data download script
docker-compose run --rm peptide-app python3 scripts/download_and_prepare_data.py

# Option B: Add your own data manually
# Place your CSV files in data/raw/:
# - train_pos.csv (toxic peptides for training)
# - train_neg.csv (non-toxic peptides for training)
# - test_pos.csv (toxic peptides for testing)
# - test_neg.csv (non-toxic peptides for testing)
```

### Step 4: Build the Docker Image

```bash
# Build the Docker image (this may take 5-10 minutes the first time)
docker-compose build

# You'll see:
# - Python packages being installed
# - Node.js dependencies being installed
# - Application being built
```

### Step 5: Start the Application

```bash
# Start all services
docker-compose up

# Or run in background (detached mode)
docker-compose up -d

# To see logs when running in background:
docker-compose logs -f
```

### Step 6: Access the Application

Open your web browser and visit:

- **Frontend (Web Interface)**: http://localhost:3000
- **Backend API**: http://localhost:3001
- **API Documentation**: http://localhost:3001/api (if Swagger is enabled)

---

## 🚀 Running the Application

### Normal Usage (After Initial Setup)

```bash
# Start the application
docker-compose up

# Or start in background
docker-compose up -d

# Stop the application
docker-compose down

# Restart the application
docker-compose restart

# View logs
docker-compose logs -f peptide-app
```

### Using the Web Interface

1. **Home Page** (`http://localhost:3000`):
   - Overview of the project
   - Model accuracy statistics
   - Quick start options

2. **Predict Page**:
   - Enter a peptide sequence (e.g., `GIGAVLKVLTTGLPALISWIKRKRQQ`)
   - Click "Predict"
   - View toxicity prediction and confidence score

3. **Analysis Page**:
   - Analyze peptide features
   - View amino acid composition
   - See physicochemical properties

4. **History Page**:
   - View past predictions
   - See statistics

---

## 🎓 Training Models

### Train Models Inside Docker

```bash
# Option 1: Train using the main container
docker-compose run --rm peptide-app python3 scripts/train_pipeline.py

# Option 2: Use the dedicated ML service (for development)
docker-compose --profile dev up ml-service
docker-compose --profile dev run --rm ml-service python3 scripts/train_pipeline.py

# Training will:
# 1. Load data from data/raw/
# 2. Extract features
# 3. Train 3 models (Logistic Regression, Random Forest, SVM)
# 4. Save results to results/
# 5. Save trained models to results/trained_models.pkl
```

### Training Time Estimates

- **Small dataset** (1,000-5,000 sequences): 2-5 minutes
- **Medium dataset** (10,000-50,000 sequences): 10-30 minutes
- **Large dataset** (100,000+ sequences): 1-3 hours

### Monitor Training Progress

```bash
# Watch training logs in real-time
docker-compose run --rm peptide-app python3 scripts/train_pipeline.py 2>&1 | tee training.log

# Or if training is already running
docker-compose logs -f peptide-app
```

### After Training

The trained models are automatically saved and the web app will use them for predictions.

---

## 🔧 Troubleshooting

### Docker Issues

#### Problem: "Cannot connect to Docker daemon"
**Solution:**
```bash
# Make sure Docker Desktop is running
# On macOS/Windows: Open Docker Desktop app
# On Linux: 
sudo systemctl start docker
```

#### Problem: "Port 3000 or 3001 already in use"
**Solution:**
```bash
# Option A: Stop other services using these ports
# Find what's using the port (macOS/Linux):
lsof -i :3000
lsof -i :3001

# Find what's using the port (Windows):
netstat -ano | findstr :3000
netstat -ano | findstr :3001

# Option B: Change ports in docker-compose.yml:
# Edit ports section:
ports:
  - "8080:3000"  # Use port 8080 instead of 3000
  - "8081:3001"  # Use port 8081 instead of 3001
```

#### Problem: "Build fails with memory error"
**Solution:**
```bash
# Increase Docker memory limit:
# 1. Open Docker Desktop
# 2. Go to Settings → Resources
# 3. Increase Memory to at least 4GB (8GB recommended)
# 4. Click "Apply & Restart"
```

### Application Issues

#### Problem: "Models not found" error
**Solution:**
```bash
# Train the models first
docker-compose run --rm peptide-app python3 scripts/train_pipeline.py
```

#### Problem: "Prediction failed" error
**Solution:**
```bash
# Check logs for details
docker-compose logs peptide-app

# Common causes:
# 1. Invalid peptide sequence (use only standard amino acids: ACDEFGHIKLMNPQRSTVWY)
# 2. Sequence too short (minimum 5 amino acids)
# 3. Sequence too long (maximum 100 amino acids)
```

#### Problem: Web page shows blank/white screen
**Solution:**
```bash
# Rebuild the frontend
docker-compose down
docker-compose build --no-cache
docker-compose up
```

### Data Issues

#### Problem: "No data found" error during training
**Solution:**
```bash
# Download and prepare data
docker-compose run --rm peptide-app python3 scripts/download_and_prepare_data.py

# Or add your own data to data/raw/
# Required files:
# - train_pos.csv
# - train_neg.csv
# - test_pos.csv
# - test_neg.csv
```

---

## 🔬 Advanced Usage

### Run Individual Components

```bash
# Run only the backend
docker-compose run --rm -p 3001:3001 peptide-app sh -c "cd backend && npm run start:prod"

# Run Python scripts directly
docker-compose run --rm peptide-app python3 scripts/predict_new.py

# Access container shell
docker-compose run --rm peptide-app bash
```

### Development Mode

For development with live reloading:

```bash
# Use volume mounts for live code changes
docker-compose -f docker-compose.dev.yml up
```

Create `docker-compose.dev.yml`:
```yaml
version: '3.8'
services:
  peptide-app:
    build: .
    ports:
      - "3000:3000"
      - "3001:3001"
    volumes:
      - ./src:/app/src
      - ./scripts:/app/scripts
      - ./backend/src:/app/backend/src
      - ./app:/app/app
      - ./components:/app/components
    environment:
      - NODE_ENV=development
```

### Clean Up Docker Resources

```bash
# Stop and remove containers
docker-compose down

# Remove containers and volumes
docker-compose down -v

# Remove all unused Docker resources
docker system prune -a

# Remove only this project's images
docker-compose down --rmi all
```

### Update the Application

```bash
# Pull latest changes from GitHub
git pull origin main

# Rebuild and restart
docker-compose down
docker-compose build --no-cache
docker-compose up
```

---

## 📊 Performance Tips

### For Better Performance

1. **Allocate more resources to Docker**:
   - Open Docker Desktop → Settings → Resources
   - Increase CPU cores (4+ recommended)
   - Increase Memory (8GB+ recommended)

2. **Use SSD storage** for Docker volumes

3. **Close unnecessary applications** while training

4. **Use build cache**:
   ```bash
   # Don't use --no-cache unless necessary
   docker-compose build
   ```

### For Faster Builds

```bash
# Use BuildKit for faster builds
DOCKER_BUILDKIT=1 docker-compose build

# Build with multiple cores
docker-compose build --parallel
```

---

## 🆘 Getting Help

### Check Logs

```bash
# View all logs
docker-compose logs

# View specific service logs
docker-compose logs peptide-app

# Follow logs in real-time
docker-compose logs -f

# View last 100 lines
docker-compose logs --tail=100
```

### Inspect Container

```bash
# List running containers
docker-compose ps

# Access container shell
docker-compose exec peptide-app bash

# Check container health
docker inspect peptide-toxicity-app | grep -A 10 Health
```

### Common Commands Quick Reference

```bash
# Start application
docker-compose up -d

# Stop application
docker-compose down

# Restart application
docker-compose restart

# View logs
docker-compose logs -f

# Rebuild
docker-compose build --no-cache

# Update and restart
git pull && docker-compose down && docker-compose up --build -d

# Train models
docker-compose run --rm peptide-app python3 scripts/train_pipeline.py

# Clean everything
docker-compose down -v && docker system prune -a
```

---

## ✅ Success Checklist

- [ ] Docker Desktop installed and running
- [ ] Project downloaded/cloned
- [ ] Docker image built successfully (`docker-compose build`)
- [ ] Data prepared (either downloaded or custom data added)
- [ ] Models trained (if using real predictions)
- [ ] Application started (`docker-compose up`)
- [ ] Frontend accessible at http://localhost:3000
- [ ] Backend accessible at http://localhost:3001
- [ ] Test prediction works

---

## 🎉 You're Ready!

Once you see these messages in the logs:
```
Backend started with PID: ...
Frontend started with PID: ...
========================================
Application is ready!
Frontend: http://localhost:3000
Backend API: http://localhost:3001
========================================
```

Your application is fully operational! Visit http://localhost:3000 to start predicting peptide toxicity.

---

## 📚 Additional Resources

- [Docker Documentation](https://docs.docker.com/)
- [Docker Compose Documentation](https://docs.docker.com/compose/)
- [Project README](README.md)
- [Installation Guide](INSTALLATION.md)
- [GitHub Repository](https://github.com/Maaskk/peptide-toxicity-prediction)

---

**Need more help?** Check the project's GitHub Issues or create a new issue with:
1. Your operating system
2. Docker version (`docker --version`)
3. Error message or logs
4. Steps you followed

