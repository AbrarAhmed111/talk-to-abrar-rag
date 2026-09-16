"""
FastAPI Application Entrypoint.
Initializes FastAPI, configures CORS, mounts API routes, and manages application lifecycle.
"""

from contextlib import asynccontextmanager
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from src.app.core.config import get_settings
from src.app.core.logging import setup_logging
from src.app.api.router import api_router
from src.app.api.routes.health import router as health_router
from src.app.services.chat_service import rag_pipeline

settings = get_settings()
setup_logging(settings.LOG_LEVEL)


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Application lifecycle management: indexes the RAG knowledge base once at startup."""
    rag_pipeline.initialize()
    yield


app = FastAPI(
    title=settings.APP_NAME,
    version="1.0.0",
    description="RAG backend for Abrar's Reflection — a grounded chatbot answering visitor questions about Abrar Ahmed's career, projects, and skills, with multi-provider LLM failover.",
    lifespan=lifespan,
)

# -----------------------------------------------------------------------------
# CORS Middleware
# -----------------------------------------------------------------------------
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.allowed_origins_list,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Mount root health check (e.g. for container health checks)
app.include_router(health_router)

# Mount central API router under /api
app.include_router(api_router)


@app.get("/", summary="Root index")
async def root():
    """Returns basic service status and documentation link."""
    return {
        "service": settings.APP_NAME,
        "status": "running",
        "docs": "/docs",
        "endpoints": {
            "chat": "/api/chat",
            "chat_stream": "/api/chat/stream",
            "health": "/health",
        },
    }
