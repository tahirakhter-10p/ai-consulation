from unittest.mock import AsyncMock

import pytest

from app.repositories.treatment_repository import TreatmentRepository

pytestmark = pytest.mark.unit


@pytest.mark.asyncio
async def test_list_active_filters_inactive_treatments_and_orders_by_name() -> None:
    scalar_result = SimpleScalarResult([])
    session = SimpleSession(scalar_result)
    repository = TreatmentRepository(session)  # type: ignore[arg-type]

    assert await repository.list_active() == []

    statement = session.scalars.await_args.args[0]
    compiled = str(statement.compile(compile_kwargs={"literal_binds": True}))
    assert "treatments.is_active IS true" in compiled
    assert "ORDER BY treatments.name ASC" in compiled


class SimpleScalarResult:
    def __init__(self, values: list[object]) -> None:
        self._values = values

    def all(self) -> list[object]:
        return self._values


class SimpleSession:
    def __init__(self, result: SimpleScalarResult) -> None:
        self.scalars = AsyncMock(return_value=result)
