from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
from loguru import logger
from sqlalchemy.ext.asyncio import AsyncSession

from app.core import security
from app.db import crud
from app.db.models import Moderator
from app.db.session import SessinLocal
from app.services.magic_rust.magic_rust_api import MagicRustAPI
from app.services.RCC.rcc_api import RustCheatCheckAPI
from app.services.steam.steam_api import SteamAPI
from app.services.vk.vk_auth import VKAuth


async def get_session() -> AsyncSession:
    try:
        session = SessinLocal()
        yield session
    finally:
        await session.close()


async def get_current_moder(
    session: AsyncSession = Depends(get_session),
    bearer: HTTPAuthorizationCredentials = Depends(HTTPBearer(scheme_name='Bearer')),
) -> Moderator:
    try:
        token_payload = security.get_token_payload(bearer.credentials)
    except Exception as ex:
        print(ex)
        logger.warning(f'Cant auth user with bearer {bearer}')
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail='Auth failed',
        ) from ex
    moderator = await crud.moderator.get(session, id=token_payload.db_id)
    if not moderator:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='Moderator not found')
    logger.info(f'Auth  {moderator.name}: {moderator.id}')
    return moderator


async def get_current_superuser(moderator: Moderator = Depends(get_current_moder)) -> Moderator:
    if moderator.is_superuser:
        return moderator
    raise HTTPException(status.HTTP_403_FORBIDDEN, detail='Access denied')


def get_rcc_api() -> RustCheatCheckAPI:
    return RustCheatCheckAPI()


def get_mr_api() -> MagicRustAPI:
    return MagicRustAPI()


def get_vk_auth() -> VKAuth:
    return VKAuth()


def get_steam_api() -> SteamAPI:
    return SteamAPI()
