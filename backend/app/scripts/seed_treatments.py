import asyncio

from sqlalchemy.dialects.postgresql import insert

from app.data.treatments import TREATMENT_SEED_DATA
from app.database.session import AsyncSessionFactory
from app.models.treatment import Treatment


async def seed_treatments() -> None:
    """Upsert the documented treatment catalog without creating duplicates."""

    update_columns = {
        column: getattr(insert(Treatment).excluded, column)
        for column in (
            "name",
            "specialty",
            "description",
            "price",
            "price_min",
            "price_max",
            "duration_minutes",
            "location",
            "default_target_area",
            "is_active",
        )
    }
    statement = insert(Treatment).values(TREATMENT_SEED_DATA)
    statement = statement.on_conflict_do_update(index_elements=[Treatment.id], set_=update_columns)

    async with AsyncSessionFactory.begin() as session:
        await session.execute(statement)


if __name__ == "__main__":
    asyncio.run(seed_treatments())
