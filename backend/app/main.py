from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from .core.config.settings import settings
from .presentation.api.v1.router import router as v1_router

app = FastAPI(title=settings.PROJECT_NAME, version=settings.VERSION)

app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.BACKEND_CORS_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(v1_router, prefix=settings.API_V1_STR)

@app.get("/")
def root():
    return {"message": "QuantumPilot AI - NeuralUCB Autopilot for IBM Quantum", "docs": "/docs"}
