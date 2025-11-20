#!/bin/bash

echo "🛑 Stopping all services..."

# Kill Python processes
pkill -f uvicorn

# Kill npm processes
pkill -f "npm run dev"

# Stop Docker containers
docker-compose down

echo "✅ All services stopped!"
