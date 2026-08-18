from typing import Annotated

from fastapi import Depends

from app.ai.service import AIService
from app.dependencies.ai import get_ai_service
from app.dependencies.database import DatabaseSession
from app.repositories.appointment_repository import AppointmentRepository
from app.repositories.consultation_repository import ConsultationRepository
from app.repositories.message_repository import MessageRepository
from app.repositories.recommendation_repository import RecommendationRepository
from app.repositories.treatment_repository import TreatmentRepository
from app.services.appointment_service import AppointmentService
from app.services.consultation_service import ConsultationService
from app.services.dashboard_service import DashboardService
from app.services.recommendation_service import RecommendationService
from app.services.treatment_service import TreatmentService

AIServiceDependency = Annotated[AIService, Depends(get_ai_service)]


def get_dashboard_service(session: DatabaseSession) -> DashboardService:
    """Inject dashboard repositories sharing the request's database session."""

    return DashboardService(ConsultationRepository(session), AppointmentRepository(session))


def get_consultation_service(
    session: DatabaseSession, ai_service: AIServiceDependency
) -> ConsultationService:
    """Inject consultation repositories and the configured AI service."""

    return ConsultationService(
        ConsultationRepository(session),
        MessageRepository(session),
        RecommendationRepository(session),
        ai_service,
    )


def get_recommendation_service(
    session: DatabaseSession, ai_service: AIServiceDependency
) -> RecommendationService:
    """Inject recommendation workflow dependencies using one request session."""

    return RecommendationService(
        ConsultationRepository(session),
        MessageRepository(session),
        RecommendationRepository(session),
        TreatmentRepository(session),
        ai_service,
    )


def get_appointment_service(session: DatabaseSession) -> AppointmentService:
    """Inject appointment repositories sharing the request's database session."""

    return AppointmentService(
        ConsultationRepository(session),
        AppointmentRepository(session),
        TreatmentRepository(session),
    )


def get_treatment_service(session: DatabaseSession) -> TreatmentService:
    return TreatmentService(TreatmentRepository(session))


DashboardServiceDependency = Annotated[DashboardService, Depends(get_dashboard_service)]
ConsultationServiceDependency = Annotated[ConsultationService, Depends(get_consultation_service)]
RecommendationServiceDependency = Annotated[
    RecommendationService, Depends(get_recommendation_service)
]
AppointmentServiceDependency = Annotated[AppointmentService, Depends(get_appointment_service)]
TreatmentServiceDependency = Annotated[TreatmentService, Depends(get_treatment_service)]
