# E-commerce Platform

A microservices-based e-commerce platform built with FastAPI (Python) and React (TypeScript).

## Architecture

- **Frontend**: React + TypeScript + Vite
- **Backend**: FastAPI (Python) with microservices
- **Database**: PostgreSQL (separate DB per service)
- **Cache/Broker**: Redis
- **Development**: Hybrid approach (Docker for infrastructure, local for services)

## Services

- **API Gateway** (Port 8000): Entry point, routing, authentication
- **User Service** (Port 8001): User management, authentication
- **Product Service** (Port 8002): Product catalog, categories
- **Order Service** (Port 8003): Shopping cart, order management
- **Inventory Service** (Port 8004): Stock management
- **Payment Service** (Port 8005): Payment processing

## Quick Start

### 1. Start Infrastructure (PostgreSQL + Redis)

```bash
docker-compose up -d
```

### 2. Setup Backend Services

For each service you want to work on:

```bash
cd services/user-service  # or any other service
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
pip install -r requirements.txt
cp .env.example .env
# Edit .env with your configuration
uvicorn app.main:app --reload --port 8001
```

### 3. Setup Frontend

```bash
cd frontend
npm install
npm run dev
```

### 4. Or Use Helper Scripts

```bash
# Start everything
./infrastructure/scripts/start-all.sh

# Stop everything
./infrastructure/scripts/stop-all.sh
```

## Development Workflow

1. Start Docker infrastructure: `docker-compose up -d`
2. Work on individual services locally with hot reload
3. Frontend runs on http://localhost:5173
4. API Gateway on http://localhost:8000

## Project Structure

```
ecommerce-platform/
├── frontend/                 # React frontend
├── services/                 # Backend microservices
│   ├── api-gateway/
│   ├── user-service/
│   ├── product-service/
│   ├── order-service/
│   ├── inventory-service/
│   └── payment-service/
├── shared/                   # Shared code
├── infrastructure/           # DevOps configs
└── docs/                     # Documentation
```

## Documentation

See `docs/` folder for detailed documentation on:
- API specifications
- Database schemas
- Architecture decisions
- Deployment guides
