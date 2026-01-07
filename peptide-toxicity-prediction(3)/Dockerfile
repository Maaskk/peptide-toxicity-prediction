# Multi-stage Dockerfile for Peptide Toxicity Prediction Application
# This file builds both the Python ML backend and Node.js API/frontend

# Stage 1: Python ML Environment
FROM python:3.9-slim as python-base

WORKDIR /app

# Install system dependencies for Python packages
RUN apt-get update && apt-get install -y \
    gcc \
    g++ \
    make \
    && rm -rf /var/lib/apt/lists/*

# Copy Python requirements and install dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir --upgrade pip && \
    pip install --no-cache-dir -r requirements.txt

# Copy Python ML code
COPY src/ ./src/
COPY scripts/ ./scripts/
COPY results/ ./results/
COPY data/ ./data/

# Stage 2: Node.js Backend
FROM node:18-slim as backend-build

WORKDIR /app/backend

# Copy backend package files
COPY backend/package*.json ./

# Install backend dependencies
RUN npm ci --only=production

# Copy backend source
COPY backend/ ./

# Build backend
RUN npm run build

# Stage 3: Next.js Frontend Build
FROM node:18-slim as frontend-build

WORKDIR /app

# Copy frontend package files
COPY package*.json ./
COPY pnpm-lock.yaml ./

# Install pnpm and dependencies
RUN npm install -g pnpm && \
    pnpm install --frozen-lockfile

# Copy frontend source
COPY app/ ./app/
COPY components/ ./components/
COPY hooks/ ./hooks/
COPY lib/ ./lib/
COPY public/ ./public/
COPY styles/ ./styles/
COPY next.config.mjs ./
COPY tsconfig.json ./
COPY postcss.config.mjs ./
COPY components.json ./

# Build frontend
RUN pnpm run build

# Stage 4: Final Runtime Image
FROM node:18-slim

WORKDIR /app

# Install Python 3.9
RUN apt-get update && apt-get install -y \
    python3 \
    python3-pip \
    && rm -rf /var/lib/apt/lists/*

# Copy Python environment from python-base
COPY --from=python-base /usr/local/lib/python3.9/site-packages /usr/local/lib/python3.9/site-packages
COPY --from=python-base /app/src ./src
COPY --from=python-base /app/scripts ./scripts
COPY --from=python-base /app/results ./results
COPY --from=python-base /app/data ./data

# Copy backend build
COPY --from=backend-build /app/backend/node_modules ./backend/node_modules
COPY --from=backend-build /app/backend/dist ./backend/dist
COPY --from=backend-build /app/backend/package.json ./backend/
COPY backend/src ./backend/src

# Copy frontend build
COPY --from=frontend-build /app/.next ./.next
COPY --from=frontend-build /app/node_modules ./node_modules
COPY --from=frontend-build /app/package.json ./
COPY --from=frontend-build /app/public ./public

# Create necessary directories
RUN mkdir -p /app/backend/data /app/data/raw /app/data/processed /app/results

# Expose ports
# 3000 - Next.js frontend
# 3001 - NestJS backend
EXPOSE 3000 3001

# Create startup script
RUN echo '#!/bin/bash\n\
echo "Starting Peptide Toxicity Prediction Application..."\n\
echo ""\n\
echo "Starting NestJS Backend on port 3001..."\n\
cd /app/backend && npm run start:prod &\n\
BACKEND_PID=$!\n\
echo "Backend started with PID: $BACKEND_PID"\n\
echo ""\n\
sleep 5\n\
echo "Starting Next.js Frontend on port 3000..."\n\
cd /app && npm start &\n\
FRONTEND_PID=$!\n\
echo "Frontend started with PID: $FRONTEND_PID"\n\
echo ""\n\
echo "========================================"\n\
echo "Application is ready!"\n\
echo "Frontend: http://localhost:3000"\n\
echo "Backend API: http://localhost:3001"\n\
echo "========================================"\n\
echo ""\n\
wait $BACKEND_PID $FRONTEND_PID\n\
' > /app/start.sh && chmod +x /app/start.sh

CMD ["/app/start.sh"]

