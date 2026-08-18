from datetime import UTC, datetime
from decimal import Decimal
from types import SimpleNamespace
from uuid import uuid4

import pytest

from app.ai.schemas.recommendation import AIRecommendation
from app.data.treatments import TREATMENT_SEED_DATA
from app.models.enums import ConsultationStatus
from app.schemas.recommendation import RecommendationResponse
from app.services.appointment_service import AppointmentService
from app.services.recommendation_service import RecommendationService

pytestmark = pytest.mark.unit


class ConsultationRepositoryStub:
    def __init__(self) -> None:
        self.consultation = SimpleNamespace(id=uuid4())
        self.updated_status = None

    async def get_by_id(self, consultation_id):
        return self.consultation

    async def update_status(self, consultation_id, status):
        self.updated_status = status
        return self.consultation


class TreatmentRepositoryStub:
    def __init__(self, treatments) -> None:
        self.treatments = treatments

    async def list_active(self):
        return self.treatments

    async def get_by_ids(self, treatment_ids):
        return [item for item in self.treatments if item.id in treatment_ids]

    async def get_by_id(self, treatment_id):
        return next((item for item in self.treatments if item.id == treatment_id), None)

    async def get_by_name(self, name):
        return next((item for item in self.treatments if item.name.lower() == name.lower()), None)


@pytest.fixture
def treatment():
    return SimpleNamespace(
        id=uuid4(),
        name="Dermal Fillers",
        specialty="Dermatology",
        description="Database description.",
        price=Decimal("850.00"),
        price_min=Decimal("600.00"),
        price_max=Decimal("1200.00"),
        duration_minutes=45,
        location="Downtown Medical Center (Primary)",
        default_target_area="Nasolabial Folds",
        is_active=True,
    )


@pytest.mark.asyncio
async def test_recommendation_resolves_ai_ids_to_database_metadata(treatment) -> None:
    consultation_repository = ConsultationRepositoryStub()
    recommendation_repository = SimpleNamespace()
    recommendation_repository.get_by_consultation_id = lambda consultation_id: None

    async def get_missing(consultation_id):
        return None

    saved = {}

    async def save(**values):
        saved.update(values)
        return SimpleNamespace(**values)

    recommendation_repository.get_by_consultation_id = get_missing
    recommendation_repository.save = save

    async def get_conversation(consultation_id):
        return [SimpleNamespace(role=SimpleNamespace(value="user"), content="Fine lines")]

    async def generate(messages, treatments):
        return AIRecommendation(
            patient_summary="Patient summary",
            recommended_treatment_ids=[treatment.id],
            ai_reasoning="Database-backed selection.",
        )

    service = RecommendationService(
        consultation_repository,
        SimpleNamespace(get_conversation=get_conversation),
        recommendation_repository,
        TreatmentRepositoryStub([treatment]),
        SimpleNamespace(generate_recommendation=generate),
    )

    await service.generate_recommendation(consultation_id=consultation_repository.consultation.id)

    snapshot = saved["recommended_treatments"][0]
    assert snapshot["treatment_id"] == str(treatment.id)
    assert snapshot["description"] == "Database description."
    assert snapshot["specialty"] == "Dermatology"
    assert snapshot["price"] == "850.00"
    assert snapshot["priority"] == 1


@pytest.mark.asyncio
async def test_appointment_resolves_legacy_name_to_treatment_reference(treatment) -> None:
    consultation_repository = ConsultationRepositoryStub()

    async def get_no_appointment(consultation_id):
        return None

    async def create(**values):
        return SimpleNamespace(id=uuid4(), **values)

    appointment_repository = SimpleNamespace(
        get_by_consultation_id=get_no_appointment,
        create=create,
    )
    service = AppointmentService(
        consultation_repository,
        appointment_repository,
        TreatmentRepositoryStub([treatment]),
    )

    appointment = await service.book_appointment(
        consultation_id=consultation_repository.consultation.id,
        treatment_id=None,
        treatment="dermal fillers",
        appointment_datetime=datetime(2026, 8, 20, 10, tzinfo=UTC),
        location="Main Clinic",
    )

    assert appointment.treatment_id == treatment.id
    assert appointment.treatment == treatment.name
    assert appointment.treatment_record is treatment
    assert consultation_repository.updated_status is ConsultationStatus.BOOKED


def test_legacy_recommendation_json_remains_readable() -> None:
    response = RecommendationResponse.model_validate(
        {
            "patient_summary": "Legacy summary",
            "recommended_treatments": [
                {"name": "Legacy treatment", "description": "Legacy description"}
            ],
            "ai_reasoning": None,
        }
    )

    assert response.recommended_treatments[0].treatment_id is None


def test_seed_catalog_covers_required_specialties_with_operational_data() -> None:
    required_specialties = {
        "General Physician",
        "Cardiology",
        "Neurology",
        "Dermatology",
        "Ophthalmology",
        "Dentistry",
        "Orthopedics",
        "ENT",
        "Gastroenterology",
        "Gynecology",
    }

    assert len(TREATMENT_SEED_DATA) == 29
    assert required_specialties <= {item["specialty"] for item in TREATMENT_SEED_DATA}
    assert len({item["id"] for item in TREATMENT_SEED_DATA}) == len(TREATMENT_SEED_DATA)
    assert all(item["description"] for item in TREATMENT_SEED_DATA)
    assert all(item["is_active"] is True for item in TREATMENT_SEED_DATA)


def test_pdf_backed_seed_values_are_preserved() -> None:
    dermal = next(item for item in TREATMENT_SEED_DATA if item["name"] == "Dermal Fillers")
    laser = next(item for item in TREATMENT_SEED_DATA if item["name"] == "Laser Resurfacing")

    assert dermal["price"] == Decimal("850.00")
    assert dermal["duration_minutes"] == 45
    assert dermal["location"] == "Downtown Medical Center"
    assert laser["price"] is None
    assert laser["price_min"] == Decimal("400.00")
    assert laser["price_max"] == Decimal("800.00")
    assert laser["duration_minutes"] == 60


def test_user_supplied_treatments_are_in_seed_catalog() -> None:
    supplied_names = {
        "Dermal Fillers",
        "Laser Resurfacing",
        "General Physician Consultation",
        "Comprehensive Dental Examination",
        "Professional Dental Cleaning",
        "Dental Filling",
        "Cardiology Consultation",
        "ECG Examination",
        "Neurology Consultation",
        "Dermatology Consultation",
        "Ophthalmology Consultation",
        "ENT Consultation",
        "Orthopedic Consultation",
        "Physiotherapy Assessment",
        "Nutrition Consultation",
    }

    assert supplied_names <= {item["name"] for item in TREATMENT_SEED_DATA}
