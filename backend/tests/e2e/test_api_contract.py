from types import SimpleNamespace
from uuid import uuid4

import httpx
import pytest

from app.dependencies.services import get_consultation_service
from app.main import app
from app.models.enums import ConsultationStatus

pytestmark = pytest.mark.e2e


class ConsultationServiceStub:
    async def list_consultation_records(self, *, search=None, status=None):
        return [
            SimpleNamespace(
                consultation=SimpleNamespace(
                    id=uuid4(),
                    patient_name="Ada Lovelace",
                    primary_concern="Headache",
                    status=ConsultationStatus.PENDING,
                ),
                recommended_procedure="Neurology Consultation",
            )
        ]


async def get_consultation_service_stub() -> ConsultationServiceStub:
    """Provide the deterministic service stub without invoking the sync DI path."""

    return ConsultationServiceStub()


@pytest.mark.asyncio
async def test_health_response_uses_standard_envelope() -> None:
    async with httpx.AsyncClient(
        transport=httpx.ASGITransport(app=app), base_url="http://testserver"
    ) as client:
        response = await client.get("/health")

    assert response.status_code == 200
    assert response.json() == {
        "success": True,
        "message": "Application is healthy.",
        "data": {"status": "ok"},
    }


@pytest.mark.asyncio
async def test_consultation_list_returns_actual_recommended_procedure() -> None:
    app.dependency_overrides[get_consultation_service] = get_consultation_service_stub
    try:
        async with httpx.AsyncClient(
            transport=httpx.ASGITransport(app=app), base_url="http://testserver"
        ) as client:
            response = await client.get("/api/v1/consultations")
    finally:
        app.dependency_overrides.clear()

    assert response.status_code == 200
    assert response.json()["data"][0]["recommended_procedure"] == "Neurology Consultation"


@pytest.mark.asyncio
async def test_validation_errors_use_documented_400_envelope() -> None:
    app.dependency_overrides[get_consultation_service] = get_consultation_service_stub
    try:
        async with httpx.AsyncClient(
            transport=httpx.ASGITransport(app=app), base_url="http://testserver"
        ) as client:
            response = await client.post("/api/v1/consultations", json={})
    finally:
        app.dependency_overrides.clear()

    assert response.status_code == 400
    assert response.json()["success"] is False
    assert response.json()["message"] == "Validation failed."


def test_openapi_includes_documented_versioned_routes() -> None:
    schema = app.openapi()
    expected_paths = {
        "/api/v1/dashboard",
        "/api/v1/consultations",
        "/api/v1/consultations/{consultation_id}",
        "/api/v1/consultations/{consultation_id}/messages",
        "/api/v1/consultations/{consultation_id}/recommendation",
        "/api/v1/consultations/{consultation_id}/appointment",
        "/api/v1/appointments",
        "/api/v1/treatments",
    }

    assert expected_paths <= set(schema["paths"])
