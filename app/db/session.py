from sqlalchemy.ext.asyncio import async_sessionmaker, create_async_engine

from app.core import settings

engine = create_async_engine(settings.SQLALCHEMY_DATABASE_URI)

SessinLocal = async_sessionmaker(
    autoflush=False,
    expire_on_commit=False,
    bind=engine,
)
