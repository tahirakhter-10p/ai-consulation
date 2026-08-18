from datetime import UTC, datetime
from types import SimpleNamespace
from unittest.mock import AsyncMock
from uuid import uuid4

import pytest

from app.ai.schemas.recommendation import AIRecommendation
from app.core.exceptions import (
    AIServiceError,
    ConflictError,
    InvalidOperationError,
    ResourceNotFoundError,
)
from app.models.enums import ConsultationStatus, MessageRole
from app.services.appointment_service import AppointmentService
from app.services.consultation_service import ConsultationService
from app.services.dashboard_service import DashboardService
from app.services.recommendation_service import RecommendationService
from app.services.treatment_service import TreatmentService

pytestmark = pytest.mark.unit


def consultation_service(**overrides):
    dependencies = {
        "consultation_repository": SimpleNamespace(
            create=AsyncMock(),
            get_by_id=AsyncMock(),
            list=AsyncMock(return_value=[]),
            update_status=AsyncMock(),
        ),
        "message_repository": SimpleNamespace(
            save=AsyncMock(),
            get_conversation=AsyncMock(return_value=[]),
        ),
        "recommendation_repository": SimpleNamespace(get_by_consultation_id=AsyncMock()),
        "ai_service": SimpleNamespace(generate_chat_response=AsyncMock()),
    }
    dependencies.update(overrides)
    return ConsultationService(**dependencies), dependencies


@pytest.mark.asyncio
async def test_consultation_create_normalizes_text_and_rejects_blank_values() -> None:
    repository = SimpleNamespace(create=AsyncMock(return_value=SimpleNamespace()))
    service, _ = consultation_service(consultation_repository=repository)

    await service.create_consultation(patient_name="  Ada  ", primary_concern=" Headache ")

    repository.create.assert_awaited_once_with(patient_name="Ada", primary_concern="Headache")
    with pytest.raises(InvalidOperationError):
        await service.create_consultation(patient_name=" ", primary_concern="Headache")


@pytest.mark.asyncio
async def test_consultation_lookup_update_and_conversation_require_existing_record() -> None:
    consultation_id = uuid4()
    repository = SimpleNamespace(
        get_by_id=AsyncMock(return_value=None),
        update_status=AsyncMock(return_value=None),
    )
    service, _ = consultation_service(consultation_repository=repository)

    with pytest.raises(ResourceNotFoundError):
        await service.get_consultation(consultation_id)
    with pytest.raises(ResourceNotFoundError):
        await service.update_status(consultation_id, ConsultationStatus.BOOKED)
    with pytest.raises(ResourceNotFoundError):
        await service.get_conversation(consultation_id)


@pytest.mark.asyncio
async def test_consultation_listing_normalizes_optional_search() -> None:
    repository = SimpleNamespace(list=AsyncMock(return_value=[]))
    service, _ = consultation_service(consultation_repository=repository)

    await service.list_consultations(search="  Ada  ", status=ConsultationStatus.PENDING)
    await service.list_consultations(search="   ")

    assert repository.list.await_args_list[0].kwargs == {
        "search": "Ada",
        "status": ConsultationStatus.PENDING,
    }
    assert repository.list.await_args_list[1].kwargs == {"search": None, "status": None}


@pytest.mark.asyncio
async def test_send_message_persists_normalized_user_and_ai_messages() -> None:
    consultation_id = uuid4()
    consultation = SimpleNamespace(id=consultation_id)
    user_message = SimpleNamespace(role=MessageRole.USER, content="Hello")
    assistant_message = SimpleNamespace(role=MessageRole.ASSISTANT, content="Hi")
    message_repository = SimpleNamespace(
        save=AsyncMock(side_effect=[user_message, assistant_message]),
        get_conversation=AsyncMock(return_value=[user_message]),
    )
    ai_service = SimpleNamespace(
        generate_chat_response=AsyncMock(return_value=SimpleNamespace(content="Hi"))
    )
    service, _ = consultation_service(
        consultation_repository=SimpleNamespace(get_by_id=AsyncMock(return_value=consultation)),
        message_repository=message_repository,
        ai_service=ai_service,
    )

    result = await service.send_message(consultation_id=consultation_id, message="  Hello  ")

    assert result == (user_message, assistant_message)
    assert message_repository.save.await_args_list[0].kwargs["content"] == "Hello"
    assert message_repository.save.await_args_list[1].kwargs["role"] is MessageRole.ASSISTANT
    assert ai_service.generate_chat_response.await_args.args[0][0].content == "Hello"


@pytest.mark.asyncio
async def test_dashboard_statistics_and_zero_conversion() -> None:
    service = DashboardService(
        SimpleNamespace(list=AsyncMock(return_value=[1, 2, 3])),
        SimpleNamespace(get_all=AsyncMock(return_value=[1, 2])),
    )

    assert await service.get_statistics() == {
        "total_consultations": 3,
        "booked_appointments": 2,
        "conversion_rate": 66.67,
    }
    assert service.calculate_conversion_rate(booked_appointments=0, total_consultations=0) == 0.0


@pytest.mark.asyncio
async def test_treatment_service_returns_repository_catalog() -> None:
    treatments = [SimpleNamespace(id=uuid4())]
    repository = SimpleNamespace(list_active=AsyncMock(return_value=treatments))
    service = TreatmentService(repository)

    assert await service.list_treatments() is treatments
    repository.list_active.assert_awaited_once_with()


def appointment_service(*, consultation=None, existing=None, treatment=None, updated=None):
    consultation_repository = SimpleNamespace(
        get_by_id=AsyncMock(return_value=consultation),
        update_status=AsyncMock(return_value=updated),
    )
    appointment_repository = SimpleNamespace(
        get_by_consultation_id=AsyncMock(return_value=existing),
        create=AsyncMock(return_value=SimpleNamespace()),
        get_all=AsyncMock(return_value=[]),
    )
    treatment_repository = SimpleNamespace(
        get_by_id=AsyncMock(return_value=treatment),
        get_by_name=AsyncMock(return_value=treatment),
    )
    return (
        AppointmentService(
            consultation_repository, appointment_repository, treatment_repository
        ),
        appointment_repository,
    )


@pytest.mark.asyncio
async def test_appointment_booking_validates_preconditions() -> None:
    consultation_id = uuid4()
    values = {
        "consultation_id": consultation_id,
        "treatment_id": None,
        "treatment": None,
        "appointment_datetime": datetime.now(UTC),
        "location": "Clinic",
    }

    service, _ = appointment_service()
    with pytest.raises(ResourceNotFoundError):
        await service.book_appointment(**values)

    service, _ = appointment_service(consultation=object(), existing=object())
    with pytest.raises(ConflictError):
        await service.book_appointment(**values)

    service, _ = appointment_service(consultation=object())
    with pytest.raises(InvalidOperationError):
        await service.book_appointment(**{**values, "appointment_datetime": "tomorrow"})

    with pytest.raises(InvalidOperationError):
        await service.book_appointment(**values)


@pytest.mark.asyncio
async def test_appointment_booking_rejects_blank_location_and_concurrent_deletion() -> None:
    consultation_id = uuid4()
    treatment = SimpleNamespace(id=uuid4(), name="Consultation")
    values = {
        "consultation_id": consultation_id,
        "treatment_id": treatment.id,
        "treatment": None,
        "appointment_datetime": datetime.now(UTC),
        "location": " ",
    }
    service, appointments = appointment_service(
        consultation=object(), treatment=treatment, updated=object()
    )
    with pytest.raises(InvalidOperationError):
        await service.book_appointment(**values)

    appointments.create.return_value = SimpleNamespace()
    values["location"] = "Clinic"
    service, _ = appointment_service(consultation=object(), treatment=treatment, updated=None)
    with pytest.raises(ResourceNotFoundError):
        await service.book_appointment(**values)


@pytest.mark.asyncio
async def test_appointment_list_delegates_to_repository() -> None:
    service, repository = appointment_service()
    repository.get_all.return_value = [SimpleNamespace(id=uuid4())]

    assert await service.get_appointments() == repository.get_all.return_value


def recommendation_service(
    *, consultation=None, recommendation=None, treatments=None, selected=None
):
    treatments = [] if treatments is None else treatments
    return RecommendationService(
        SimpleNamespace(get_by_id=AsyncMock(return_value=consultation)),
        SimpleNamespace(get_conversation=AsyncMock(return_value=[])),
        SimpleNamespace(
            get_by_consultation_id=AsyncMock(return_value=recommendation),
            save=AsyncMock(),
        ),
        SimpleNamespace(
            list_active=AsyncMock(return_value=treatments),
            get_by_ids=AsyncMock(return_value=selected or []),
        ),
        SimpleNamespace(generate_recommendation=AsyncMock()),
    )


@pytest.mark.asyncio
async def test_recommendation_requires_consultation_and_unique_record() -> None:
    consultation_id = uuid4()
    with pytest.raises(ResourceNotFoundError):
        await recommendation_service().generate_recommendation(consultation_id=consultation_id)
    with pytest.raises(ConflictError):
        await recommendation_service(
            consultation=object(), recommendation=object()
        ).generate_recommendation(consultation_id=consultation_id)


@pytest.mark.asyncio
async def test_recommendation_requires_catalog_and_valid_ai_ids() -> None:
    consultation_id = uuid4()
    treatment = SimpleNamespace(
        id=uuid4(), name="Exam", specialty="General", description="Exam description"
    )
    service = recommendation_service(consultation=object())
    with pytest.raises(InvalidOperationError):
        await service.generate_recommendation(consultation_id=consultation_id)

    service = recommendation_service(consultation=object(), treatments=[treatment])
    service._ai_service.generate_recommendation.return_value = AIRecommendation(
        patient_summary="Summary",
        recommended_treatment_ids=[treatment.id, treatment.id],
        ai_reasoning=None,
    )
    with pytest.raises(AIServiceError):
        await service.generate_recommendation(consultation_id=consultation_id)

    unknown_id = uuid4()
    service._ai_service.generate_recommendation.return_value = AIRecommendation(
        patient_summary="Summary",
        recommended_treatment_ids=[unknown_id],
        ai_reasoning=None,
    )
    with pytest.raises(AIServiceError):
        await service.generate_recommendation(consultation_id=consultation_id)


@pytest.mark.asyncio
async def test_get_recommendation_handles_present_and_missing_records() -> None:
    consultation_id = uuid4()
    recommendation = SimpleNamespace(id=uuid4())
    assert (
        await recommendation_service(
            consultation=object(), recommendation=recommendation
        ).get_recommendation(consultation_id)
        is recommendation
    )
    with pytest.raises(ResourceNotFoundError):
        await recommendation_service(consultation=object()).get_recommendation(consultation_id)
