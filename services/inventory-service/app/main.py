from fastapi import FastAPI
from app.routers import inventory_router
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI(title="inventory-service")

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(inventory_router.router)