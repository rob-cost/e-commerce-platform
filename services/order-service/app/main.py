from fastapi import FastAPI
from app.routers import order_router
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI(title="Product Service")

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(order_router.router)