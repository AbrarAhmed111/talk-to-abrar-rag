"""
Health Check & Status Endpoints.
Reports operational health and active LLM gateway deployments.
"""

from fastapi import APIRouter
from src.app.core.config import get_settings
from src.app.services import gateway, rag_pipeline

router = APIRouter(tags=["Health"])


@router.get("/health", summary="Health check")
async def health_check():
    """Returns system status, RAG knowledge index state, and active LLM gateway deployment statistics."""
    settings = get_settings()
    available = gateway.get_available_deployments()

    # Normally initialized once via main.py's lifespan startup hook, before any
    # request is served. Guarded here too so /health reflects real state even
    # if hit in a context where that startup hook didn't run (e.g. certain
    # test harnesses that construct the ASGI app without triggering lifespan).
    if not rag_pipeline.is_initialized:
        rag_pipeline.initialize()

    return {
        "status": "healthy",
        "app_name": settings.APP_NAME,
        "environment": settings.ENVIRONMENT,
        "knowledge_index": {
            "disabled": False,
            "indexed_chunks": rag_pipeline.vector_store.total_docs,
            "source": rag_pipeline.knowledge_dir,
        },
        "gateway": {
            "total_deployments": len(gateway.deployments),
            "available_deployments": len(available),
            "deployments": [
                {
                    "name": d.name,
                    "provider": d.provider,
                    "model": d.default_model,
                    "is_available": d.is_available,
                    "is_disabled": d.is_permanently_disabled,
                }
                for d in gateway.deployments
            ],
        },
    }
