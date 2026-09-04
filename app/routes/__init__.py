"""
Chargeback Evidence AI - API Routes
"""

from app.routes.auth_routes import router as auth_router
from app.routes.case_routes import router as case_router
from app.routes.agent_routes import router as agent_router
from app.routes.fraud_routes import router as fraud_router
from app.routes.pipeline_routes import router as pipeline_router

__all__ = [
    "auth_router",
    "case_router",
    "agent_router",
    "fraud_router",
    "pipeline_router"
]
