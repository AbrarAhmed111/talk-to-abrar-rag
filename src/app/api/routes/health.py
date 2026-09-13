"""
Health Check & Status Endpoints.
Reports operational health and active LLM gateway deployments.
"""

from fastapi import APIRouter
from src.app.core.config import get_settings
from src.app.services import gateway

router = APIRouter(tags=["Health"])


@router.get("/health", summary="Health check")
async def health_check():
    """Returns system status and active LLM gateway deployment statistics."""
    settings = get_settings()
    available = gateway.get_available_deployments()

    return {
        "status": "healthy",
        "app_name": settings.APP_NAME,
        "environment": settings.ENVIRONMENT,
        "knowledge_index": {
            "disabled": True,
            "indexed_chunks": 0,
            "source": "not_used",
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
