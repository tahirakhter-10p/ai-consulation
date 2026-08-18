from app.repositories.appointment_repository import AppointmentRepository
from app.repositories.consultation_repository import ConsultationRepository


class DashboardService:
    """Build dashboard metrics from consultation and appointment data."""

    def __init__(
        self,
        consultation_repository: ConsultationRepository,
        appointment_repository: AppointmentRepository,
    ) -> None:
        self._consultation_repository = consultation_repository
        self._appointment_repository = appointment_repository

    async def get_statistics(self) -> dict[str, int | float]:
        """Return the consultation count, appointment count, and conversion percentage."""

        consultations = await self._consultation_repository.list()
        appointments = await self._appointment_repository.get_all()
        total_consultations = len(consultations)
        booked_appointments = len(appointments)

        return {
            "total_consultations": total_consultations,
            "booked_appointments": booked_appointments,
            "conversion_rate": self.calculate_conversion_rate(
                booked_appointments=booked_appointments,
                total_consultations=total_consultations,
            ),
        }

    @staticmethod
    def calculate_conversion_rate(*, booked_appointments: int, total_consultations: int) -> float:
        """Calculate the percentage of consultations that resulted in an appointment."""

        if total_consultations == 0:
            return 0.0
        return round((booked_appointments / total_consultations) * 100, 2)
