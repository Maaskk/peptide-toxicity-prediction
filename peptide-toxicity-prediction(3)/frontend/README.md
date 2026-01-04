# Peptide Toxicity Prediction - Vue.js Frontend

Professional bioinformatics dashboard for peptide toxicity prediction.

## Features

- Modern Vue 3 with Composition API
- TypeScript for type safety
- Tailwind CSS for styling
- Vue Router for navigation
- Responsive design
- Dark mode support
- Real-time predictions
- Feature analysis
- Prediction history

## Installation

```bash
cd frontend
npm install
```

## Development

```bash
npm run dev
```

Visit `http://localhost:3000`

## Build for Production

```bash
npm run build
```

## Project Structure

```
src/
├── views/          # Page components
├── components/     # Reusable components
├── services/       # API services
├── router/         # Route configuration
├── assets/         # CSS and static files
└── main.ts         # App entry point
```

## Environment Variables

Create a `.env` file:

```
VITE_API_URL=http://localhost:3001
