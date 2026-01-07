#!/bin/bash

# Quick start script for Docker
# This script helps users get started quickly

echo "=========================================="
echo "Peptide Toxicity Prediction - Docker Setup"
echo "=========================================="
echo ""

# Check if Docker is installed
if ! command -v docker &> /dev/null; then
    echo "❌ Docker is not installed!"
    echo ""
    echo "Please install Docker Desktop:"
    echo "  - Windows/Mac: https://www.docker.com/products/docker-desktop/"
    echo "  - Linux: https://docs.docker.com/engine/install/"
    echo ""
    exit 1
fi

# Check if Docker is running
if ! docker info &> /dev/null; then
    echo "❌ Docker is not running!"
    echo ""
    echo "Please start Docker Desktop and try again."
    echo ""
    exit 1
fi

echo "✅ Docker is installed and running"
echo ""

# Check if trained models exist
if [ ! -f "results/trained_models.pkl" ]; then
    echo "⚠️  No trained models found."
    echo ""
    echo "Do you want to train models now? (This will take 10-30 minutes)"
    echo "Options:"
    echo "  1) Yes, train models now"
    echo "  2) No, start app with mock predictions (for testing)"
    echo ""
    read -p "Enter choice (1 or 2): " choice
    
    if [ "$choice" = "1" ]; then
        echo ""
        echo "Training models..."
        docker-compose build
        docker-compose run --rm peptide-app python3 scripts/train_pipeline.py
        echo ""
        echo "✅ Training complete!"
        echo ""
    else
        echo ""
        echo "Skipping training. App will use mock predictions."
        echo ""
    fi
fi

# Build and start the application
echo "Building Docker image (this may take 5-10 minutes first time)..."
docker-compose build

echo ""
echo "Starting application..."
docker-compose up -d

echo ""
echo "=========================================="
echo "✅ Application started!"
echo ""
echo "Frontend: http://localhost:3000"
echo "Backend:  http://localhost:3001"
echo ""
echo "To view logs:"
echo "  docker-compose logs -f"
echo ""
echo "To stop:"
echo "  docker-compose down"
echo "=========================================="

