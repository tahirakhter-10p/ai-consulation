import os

os.environ.setdefault(
    "AI_CONSULTATION_DATABASE_URL",
    "postgresql+asyncpg://test:test@localhost:5432/ai_consultation_test",
)
