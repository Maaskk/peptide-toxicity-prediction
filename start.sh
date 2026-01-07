#!/bin/bash
# Complete startup script for Peptide Toxicity Prediction Platform

set -e

echo "🚀 Starting Peptide Toxicity Prediction Platform..."
echo ""

# Load nvm if available
export NVM_DIR="$HOME/.nvm"
[ -s "$NVM_DIR/nvm.sh" ] && source "$NVM_DIR/nvm.sh"

# Check Node.js
if ! command -v node &> /dev/null; then
    echo "❌ Node.js not found. Installing..."
    if [ -s "$NVM_DIR/nvm.sh" ]; then
        nvm install 18
        nvm use 18
    else
        echo "Please install Node.js manually: brew install node"
        exit 1
    fi
fi

echo "✅ Node.js: $(node --version)"
echo "✅ npm: $(npm --version)"
echo ""

# Check if models are trained
if [ ! -f "results/trained_models.pkl" ]; then
    echo "⚠️  Models not found. Training models..."
    python3 scripts/train_pipeline.py
fi

echo ""
echo "📦 Installing backend dependencies..."
cd backend
if [ ! -d "node_modules" ]; then
    npm install
fi

echo ""
echo "📦 Installing frontend dependencies..."
cd ../frontend
if [ ! -d "node_modules" ]; then
    npm install
fi

cd ..

echo ""
echo "🎯 Starting servers..."
echo ""

# Start backend in background
echo "Starting backend on http://localhost:3001..."
cd backend
npm run start:dev > ../backend.log 2>&1 &
BACKEND_PID=$!
echo "Backend PID: $BACKEND_PID"

# Wait for backend to start
sleep 5

# Start frontend in background
echo "Starting frontend on http://localhost:3000..."
cd ../frontend
npm run dev > ../frontend.log 2>&1 &
FRONTEND_PID=$!
echo "Frontend PID: $FRONTEND_PID"

cd ..

echo ""
echo "✅ Platform is starting!"
echo ""
echo "📍 Backend API: http://localhost:3001"
echo "📍 API Docs: http://localhost:3001/api/docs"
echo "📍 Frontend: http://localhost:3000"
echo ""
echo "📝 Logs:"
echo "   - Backend: tail -f backend.log"
echo "   - Frontend: tail -f frontend.log"
echo ""
echo "🛑 To stop: kill $BACKEND_PID $FRONTEND_PID"
echo ""

# Save PIDs
echo "$BACKEND_PID $FRONTEND_PID" > .server_pids

