from collections.abc import AsyncGenerator

from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker, create_async_engine

from app.core.config import get_settings

settings = get_settings()
engine = create_async_engine(str(settings.database_url), echo=settings.debug, pool_pre_ping=True)
AsyncSessionFactory = async_sessionmaker(engine, class_=AsyncSession, expire_on_commit=False)


async def get_async_session() -> AsyncGenerator[AsyncSession]:
    """Yield an async session and commit its request transaction on success."""

    async with AsyncSessionFactory() as session:
        async with session.begin():
            yield session
