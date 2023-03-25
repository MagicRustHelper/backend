from fastapi import APIRouter, Depends, HTTPException, Response, status
from loguru import logger
from sqlalchemy.ext.asyncio import AsyncSession

from app import entities
from app.api.deps import get_current_moder, get_session, get_vk_auth
from app.core import security
from app.db import crud
from app.db.models import Moderator
from app.services.vk.vk_auth import VKAuth

router = APIRouter(tags=['Auth'])


@router.get('/vk', response_model=entities.BearerToken)
async def vk_auth(
    code: str, *, session: AsyncSession = Depends(get_session), vk_auth: VKAuth = Depends(get_vk_auth)
) -> entities.BearerToken:
    try:
        oauth2_credentials = await vk_auth.get_oauth2_credentials(code)
    except Exception as ex:
        logger.warning(f'Bad authorize with code: {code}')
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail='Authorize failed',
        ) from ex

    moderator = await crud.moderator.get_moder_by_vk(session, oauth2_credentials.user_id)
    if not moderator:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='Moderator not found')

    token_payload = entities.TokenPayload(db_id=moderator.id)
    bearer_token = security.create_access_token(token_payload)
    return entities.BearerToken(token=bearer_token)


@router.get('/validate', response_class=Response, status_code=204)
async def validate(*, moderator: Moderator = Depends(get_current_moder)) -> None:
    if moderator:
        return Response(status_code=status.HTTP_204_NO_CONTENT)
    else:
        return Response(status_code=status.HTTP_401_UNAUTHORIZED)
