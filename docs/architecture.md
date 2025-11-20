# Architecture Documentation

## Microservices Communication

[Add your architecture diagrams and decisions here]

## Database Schema

ecommerce-platform/
├── README.md
├── docker-compose.yml              # Run all services locally
├── .env.example
├── .gitignore
│
├── frontend/                        # React + TypeScript
│   ├── public/
│   ├── src/
│   │   ├── components/
│   │   ├── pages/
│   │   ├── services/              # API calls
│   │   ├── hooks/
│   │   ├── context/               # State management
│   │   ├── types/
│   │   └── utils/
│   ├── package.json
│   ├── tsconfig.json
│   └── vite.config.ts             # or webpack config
│
├── services/                       # Backend microservices
│   ├── api-gateway/
│   │   ├── app/
│   │   │   ├── main.py
│   │   │   ├── routers/
│   │   │   ├── middleware/
│   │   │   └── config.py
│   │   ├── tests/
│   │   ├── requirements.txt
│   │   ├── Dockerfile
│   │   └── README.md
│   │
│   ├── user-service/
│   │   ├── app/
│   │   │   ├── main.py
│   │   │   ├── models/
│   │   │   ├── schemas/
│   │   │   ├── routers/
│   │   │   ├── services/
│   │   │   ├── database.py
│   │   │   └── auth.py
│   │   ├── tests/
│   │   ├── alembic/              # Database migrations
│   │   ├── requirements.txt
│   │   ├── Dockerfile
│   │   └── README.md
│   │
│   ├── product-service/
│   │   ├── app/
│   │   │   ├── main.py
│   │   │   ├── models/
│   │   │   ├── schemas/
│   │   │   ├── routers/
│   │   │   ├── services/
│   │   │   └── database.py
│   │   ├── tests/
│   │   ├── alembic/
│   │   ├── requirements.txt
│   │   ├── Dockerfile
│   │   └── README.md
│   │
│   ├── order-service/
│   │   └── ... (similar structure)
│   │
│   ├── inventory-service/
│   │   └── ... (similar structure)
│   │
│   └── payment-service/
│       └── ... (similar structure)
│
├── shared/                         # Shared code/configs
│   ├── proto/                     # If using gRPC
│   ├── schemas/                   # Shared Pydantic models
│   └── utils/
│
├── infrastructure/                 # DevOps configs
│   ├── kubernetes/                # K8s configs (for later)
│   ├── nginx/                     # Reverse proxy config
│   └── scripts/
│
└── docs/                          # Documentation
    ├── architecture.md
    ├── api-specs/
    └── setup.md

## API Specifications

[Link to OpenAPI/Swagger docs]
