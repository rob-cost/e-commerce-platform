#!/bin/bash

echo "🚀 Starting all services..."

# Start infrastructure
docker-compose up -d

# Wait for services to be ready
echo "⏳ Waiting for PostgreSQL and Redis..."
sleep 5

# Start backend services
echo "🐍 Starting backend services..."

cd services/api-gateway && uvicorn app.main:app --reload --port 8000 &
cd services/user-service && uvicorn app.main:app --reload --port 8001 &
cd services/product-service && uvicorn app.main:app --reload --port 8002 &
cd services/order-service && uvicorn app.main:app --reload --port 8003 &
cd services/inventory-service && uvicorn app.main:app --reload --port 8004 &
cd services/payment-service && uvicorn app.main:app --reload --port 8005 &

# Start frontend
echo "⚛️  Starting frontend..."
cd frontend && npm run dev &

echo "✅ All services started!"
echo "Frontend: http://localhost:5173"
echo "API Gateway: http://localhost:8000"
echo "PostgreSQL: localhost:5432"
echo "Redis: localhost:6379"
