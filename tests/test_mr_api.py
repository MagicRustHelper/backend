import pytest

from app.services.magic_rust.magic_rust_api import MagicRustAPI


async def test_mr_get_players(mocked_mr_api, mr_players_response):
    mr_api: MagicRustAPI = mocked_mr_api(mr_players_response)
    players = await mr_api.get_online_players()
    assert len(players) > 0
    player = players[0]
    assert player.steamid is not None
    assert player.nickname is not None
    assert player.ip is not None
    assert player.first_join is not None


@pytest.mark.online
async def test_get_banned_players_online():
    mr_api = MagicRustAPI()
    all_bans = await mr_api.get_banned_steamids()
    assert len(all_bans) > 0
