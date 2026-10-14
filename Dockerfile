
# Stage 1: Build the React frontend
FROM node:22-alpine AS frontend-build

WORKDIR /frontend

COPY package*.json ./
RUN npm ci

COPY . .
RUN npm run build


# Stage 2: Run the FastAPI backend
FROM python:3.12-slim

WORKDIR /app

COPY backend/requirements.txt ./requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

COPY backend ./backend
COPY --from=frontend-build /frontend/dist ./dist

WORKDIR /app/backend

ENV PYTHONUNBUFFERED=1

CMD ["sh", "-c", "uvicorn app.main:app --host 0.0.0.0 --port ${PORT:-10000}"]