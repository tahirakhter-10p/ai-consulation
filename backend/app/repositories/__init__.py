"""Async SQLAlchemy repositories for database persistence."""

from app.repositories.appointment_repository import AppointmentRepository
from app.repositories.consultation_repository import ConsultationRepository
from app.repositories.message_repository import MessageRepository
from app.repositories.recommendation_repository import RecommendationRepository
from app.repositories.treatment_repository import TreatmentRepository

__all__ = [
    "AppointmentRepository",
    "ConsultationRepository",
    "MessageRepository",
    "RecommendationRepository",
    "TreatmentRepository",
]
