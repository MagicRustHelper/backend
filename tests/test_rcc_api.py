from app.services.RCC.rcc_api import RustCheatCheckAPI


async def test_get_rcc_player(mocked_rcc_api, rcc_player_response):
    rcc_api: RustCheatCheckAPI = mocked_rcc_api(rcc_player_response)
    player = await rcc_api.get_rcc_player(1)
    assert player is not None
    assert player.steamid is not None


async def test_rcc_cache(mocked_rcc_api, rcc_player_response: dict):
    rcc_api: RustCheatCheckAPI = mocked_rcc_api(rcc_player_response)
    await rcc_api.get_rcc_player('ANY VALUE')
    rcc_api: RustCheatCheckAPI = mocked_rcc_api(None)
    player = await rcc_api.get_rcc_player('ANY VALUE')
    assert player is not None
    assert player.steamid == int(rcc_player_response.get('steamid'))


async def test_rcc_error_response(mocked_rcc_api, rcc_error_response):
    rcc_api: RustCheatCheckAPI = mocked_rcc_api(rcc_error_response)
    player = await rcc_api.get_rcc_player(3)
    assert player.steamid is None
    assert player.error_message is not None
