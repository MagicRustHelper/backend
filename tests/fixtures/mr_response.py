import random
import time

import pytest

nicknames = ['MaHryCT', 'cr1sTioj', 'SilentAPony', 'Trix', 'Black+Cube', 'SHooTeR', 'magicow', 'never lucky']
servers = list(range(19))


@pytest.fixture
def mr_players_response() -> list[dict]:
    return [_generate_player_response() for _ in range(10)]


def _generate_player_response() -> None:
    return {
        'id': _random_steamid(),
        'ip': _random_ip(),
        'nickname': random.choice(nicknames),
        'firstjoin': time.time(),
        'server': random.choice(servers),
        'vk': None,
        'stats': None,
    }


def _random_steamid() -> str:
    return f'765611{random.randint(1000000000, 9999999999)}'


def _random_ip() -> str:
    return f'{random.randint(0, 255)}.{random.randint(0, 255)}.{random.randint(0, 255)}.{random.randint(0, 255)}'
