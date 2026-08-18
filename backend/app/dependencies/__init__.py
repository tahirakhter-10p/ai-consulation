"""Dependency factories for application infrastructure."""

from app.dependencies.ai import get_ai_service
from app.dependencies.services import (
    get_appointment_service,
    get_consultation_service,
    get_dashboard_service,
    get_recommendation_service,
    get_treatment_service,
)

__all__ = [
    "get_ai_service",
    "get_appointment_service",
    "get_consultation_service",
    "get_dashboard_service",
    "get_recommendation_service",
    "get_treatment_service",
]
