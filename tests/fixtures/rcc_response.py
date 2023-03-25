import random
import time
from typing import NamedTuple

import pytest

from app.entities.RCC_entites import RCCErrorsMessages


class RCCCheckParams(NamedTuple):
    server_name: str = 'MagicRust'
    moder_steamid: str = '76561111111111111'
    check_time: int | None = None


class RCCBanParams(NamedTuple):
    reason: str = 'Читы'
    server_name: str = 'MagicRust'
    ban_time: int | None = None
    unban_time: int = 0
    active: bool = True


rcc_bans = {
    '76561111111111111': [
        RCCBanParams('Читы', 'RUST ROOM', ban_time=10),
        RCCBanParams('макро', 'STATE', active=False),
        RCCBanParams('dz', 'RUST CASTA'),
    ],
    '76561111111111112': [RCCBanParams('2+'), RCCBanParams('макро', 'ULTIMATE')],
    '76561111111111113': [RCCBanParams('dz', 'RUST CASTA')],
}

rcc_checks = {
    '76561111111111111': [RCCCheckParams('MagicRust', check_time=1), RCCCheckParams('Grand rust', check_time=20)],
    '76561111111111112': [RCCCheckParams('ROOM')],
    '76561111111111113': [RCCCheckParams('BRO RUST', moder_steamid=None)],
}


@pytest.fixture
def rcc_player_response() -> dict:
    steamid = random.choice(list(rcc_bans.keys()))
    return _generate_rcc_player(steamid=steamid)


@pytest.fixture
def rcc_players_responses() -> dict:
    return [_generate_rcc_player(steamid=steamid) for steamid in rcc_bans.keys()]


@pytest.fixture
def rcc_error_response() -> dict:
    error_message = random.choice(list(RCCErrorsMessages)).value
    return _generate_error_response(error_message)


def _generate_rcc_player(
    status: str = 'success', steamid: str = '76561111111111111', error_message: str | None = None
) -> dict:
    return {
        'status': status,
        'steamid': steamid,
        'errorreason': error_message,
        'rcc_checks': random.randint(0, 5),
        'last_check': [_generate_rcc_check(check_param) for check_param in rcc_checks[steamid]],
        'last_ip': ['192.168.0.1'],
        'last_nick': 'MaHryCT',
        'bans': [_generate_rcc_ban(ban_param) for ban_param in rcc_bans[steamid]],
        'proofs': ['http://memesmix.net/media/created/qxi3kl.jpg'],
    }


def _generate_error_response(error_message: str | None = None) -> dict:
    return {
        'status': 'error',
        'errorreason': error_message,
    }


def _generate_rcc_check(check_param: RCCCheckParams) -> dict:
    return {
        'moderSteamID': check_param.moder_steamid,
        'serverName': check_param.server_name,
        'time': check_param.check_time or time.time(),
    }


def _generate_rcc_ban(ban_params: RCCBanParams) -> dict:
    return {
        'banID': random.randint(1, 10000000),
        'reason': ban_params.reason,
        'serverName': ban_params.server_name,
        'OVHserverID': random.randint(1, 100),
        'banDate': ban_params.ban_time or time.time(),
        'unbanDate': ban_params.unban_time,
        'active': ban_params.active,
    }
