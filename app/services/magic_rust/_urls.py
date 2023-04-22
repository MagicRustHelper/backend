from app.core import settings

STATS_API: str = settings.MAGIC_STATS_API_LINK
MODERS_API: str = settings.MAGIC_MODERS_API_LINK
SITE_API: str = 'https://api.mrust.ru/'


class StatsMethods:
    PLAYER_STATS = STATS_API + 'getPlayerStat.php'
    SERVER_STATS = STATS_API + 'getServerPlayers_2.php'


class ModersMethods:
    PLAYERS_ONLINE = MODERS_API + 'getOnlinePlayers.php'


class SiteMethods:
    BAN_LIST = SITE_API + 'players/getBanList.php'
