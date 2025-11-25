from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.routers import payment_router

app = FastAPI(title="payment-service")

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(payment_router.router)
