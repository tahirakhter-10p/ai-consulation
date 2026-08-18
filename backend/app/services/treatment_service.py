from app.models.treatment import Treatment
from app.repositories.treatment_repository import TreatmentRepository


class TreatmentService:
    """Expose the treatment catalog without adding recommendation workflow logic."""

    def __init__(self, treatment_repository: TreatmentRepository) -> None:
        self._treatment_repository = treatment_repository

    async def list_treatments(self) -> list[Treatment]:
        return await self._treatment_repository.list_active()
