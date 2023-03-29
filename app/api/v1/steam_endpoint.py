from fastapi import APIRouter, Depends

from app import entities
from app.api.deps import get_current_moder, get_steam_api
from app.db.models import Moderator
from app.services.steam.steam_api import SteamAPI

router = APIRouter(tags=['Steam'])


@router.get('/user/avatar/{steamid}', response_model=entities.SteamAvatarResponse)
async def get_steam_user_avatar(
    steamid: int, *, moderator: Moderator = Depends(get_current_moder), steam_api: SteamAPI = Depends(get_steam_api)
) -> entities.SteamAvatarResponse:
    player = await steam_api.get_steam_player(steamid)
    return entities.SteamAvatarResponse(avatarUrl=player.avatarmedium, avatarFullUrl=player.avatarfull)
