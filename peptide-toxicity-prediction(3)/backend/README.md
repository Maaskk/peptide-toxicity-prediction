# Peptide Toxicity Prediction - NestJS Backend

Professional REST API for peptide toxicity prediction using machine learning.

## Features

- RESTful API with Swagger documentation
- Python ML model integration
- Request validation
- CORS enabled
- Batch predictions
- Analysis endpoints
- History tracking

## Installation

```bash
cd backend
npm install
```

## Running the API

```bash
# Development mode
npm run start:dev

# Production mode
npm run build
npm run start:prod
```

## API Endpoints

### Predictions
- `POST /api/predictions/single` - Predict single sequence
- `POST /api/predictions/batch` - Batch predictions
- `GET /api/predictions/models` - Get available models
- `GET /api/predictions/:id` - Get prediction by ID

### Analysis
- `POST /api/analysis/features` - Extract features
- `POST /api/analysis/physicochemical` - Get properties

### History
- `GET /api/history` - Get prediction history
- `GET /api/history/stats` - Get statistics

## API Documentation

Visit `http://localhost:3001/api/docs` for interactive Swagger documentation.

## Environment Variables

Create a `.env` file:

```
PORT=3001
NODE_ENV=development
```

## Testing

```bash
# Example: Predict single sequence
curl -X POST http://localhost:3001/api/predictions/single \
  -H "Content-Type: application/json" \
  -d '{"sequence": "ACDEFGHIK", "model": "ensemble"}'
