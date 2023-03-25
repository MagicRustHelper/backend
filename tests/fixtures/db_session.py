import pytest
from sqlalchemy.ext.asyncio import AsyncSession

from app.db.session import SessinLocal


@pytest.fixture
def db_session() -> AsyncSession:
    return SessinLocal()
