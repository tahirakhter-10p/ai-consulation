from types import SimpleNamespace
from uuid import uuid4

import pytest

from app.models.enums import ConsultationStatus
from app.services.consultation_service import ConsultationService

pytestmark = pytest.mark.unit


class ConsultationRepositoryStub:
    def __init__(self, consultations: list[SimpleNamespace]) -> None:
        self.consultations = consultations

    async def list(self, *, search=None, status=None):
        return self.consultations


class RecommendationRepositoryStub:
    def __init__(self, recommendations: dict) -> None:
        self.recommendations = recommendations

    async def get_by_consultation_id(self, consultation_id):
        return self.recommendations.get(consultation_id)


@pytest.mark.asyncio
async def test_list_records_uses_first_stored_recommendation() -> None:
    recommended_consultation = SimpleNamespace(
        id=uuid4(),
        patient_name="Ada Lovelace",
        primary_concern="Headache",
        status=ConsultationStatus.PENDING,
    )
    pending_consultation = SimpleNamespace(
        id=uuid4(),
        patient_name="Grace Hopper",
        primary_concern="Cough",
        status=ConsultationStatus.PENDING,
    )
    recommendation = SimpleNamespace(
        recommended_treatments=[
            {"name": "Neurology Consultation", "description": "Specialist assessment."}
        ]
    )
    service = ConsultationService(
        ConsultationRepositoryStub([recommended_consultation, pending_consultation]),
        SimpleNamespace(),
        RecommendationRepositoryStub({recommended_consultation.id: recommendation}),
        SimpleNamespace(),
    )

    records = await service.list_consultation_records()

    assert [record.recommended_procedure for record in records] == [
        "Neurology Consultation",
        "Pending",
    ]
