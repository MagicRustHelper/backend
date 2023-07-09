from app.services.steam.steam_api import SteamAPI


class SteamFriends:
    """Helps find friends of a steam user"""

    def __init__(self) -> None:
        self.steam_client = SteamAPI()

    async def get_friends_with_include(self, steamid: int | str, include: list[str]) -> list[str]:
        friends = await self.steam_client.get_player_friend_list(steamid)
        freinds_include = [friend for friend in friends if friend.steamid in include]
        return [friend.steamid for friend in freinds_include]

    async def find_parties(self, steamids: list[str], include: list[str]) -> list[list[str]]:
        parties: dict[str, set[str]] = {}
        for steamid in steamids:
            parties[steamid] = set(await self.get_friends_with_include(steamid, include))

        remove_keys = []
        for player_steamid, player_friends in parties.items():
            for friend_steamid in player_friends:
                if friend_steamid in remove_keys:
                    continue
                parties[player_steamid] = player_friends.union(parties[friend_steamid])
                remove_keys.append(friend_steamid)

        result = []
        for owner, party in parties.items():
            if not party or owner in remove_keys:
                continue
            result.append([owner, *party])

        return result
