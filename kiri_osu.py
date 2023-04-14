import ossapi
import asyncio

#standalone osu file for dealing with osu requests.
#gamemode = ossapi.GameMode.OSU
#rankingtype = ossapi.RankingType.PERFORMANCE


class OsuPlays:

    def __init__(self, data: dict):
        self.pp = data["pp"]
        self.accuracy = data["accuracy"]
        self.beatmap_name = data["beatmap_name"]
        self.beatmap_version = data["beatmap_version"]
        self.date_achieved = data["date_achieved"]
        self.rank = data["rank"]
        self.beatmap_name = data["beatmap_name"]
        self.artist = data["artist"]
        self.difficulty = data["difficulty"]
        self.url = data["url"]
    
    def dump_dict(self):
        return self.__dict__

class OsuData(ossapi.Ossapi):

    def __init__(self, oath_code: str, client_id: str):
        self.oath_code = oath_code
        self.client_id = client_id
        super().__init__(self.client_id, self.oath_code)
    
    
    def get_user_id(self, player:str=None) -> str:
        
        if player:
            user_id = self.user(user=player, key=ossapi.UserLookupKey.USERNAME)
            
            if user_id:
                return user_id.id
            else:
                return None

    
    def get_user_plays(self, player: str, limit: int, type: str) -> list:
        #type == "recent", "best", "firsts"
        
        all_top_plays = []
        if player and isinstance(limit, int) and limit > 0 and limit <= 100 and (player_id := self.get_user_id(player)):
            all_plays = self.user_scores(user_id=player_id, include_fails=None, limit=limit, type=type)
            
            add_info = {}
            for plays in all_plays:
                add_info["pp"] = plays.pp
                add_info["accuracy"] = plays.accuracy
                add_info["beatmap_name"] = plays.beatmapset.title
                add_info["beatmap_version"] = plays.beatmap.version
                add_info["date_achieved"] = plays.created_at
                add_info["artist"] = plays.beatmapset.artist
                add_info["url"] = plays.beatmap.url
                add_info["rank"] = plays.rank
                add_info["difficulty"] = plays.beatmap.difficulty_rating
                all_top_plays.append(OsuPlays(add_info))
                print("LOADED: " + plays.beatmapset.title)
                add_info = {}
        
        return all_top_plays


if __name__ == "__main__":

    client_login = {
        "oath_code": "gkK6SDfwopiUsVcIHj2Lu5p2EA15gdLnQBRwo5kL",
        "client_id": "21288"
    }

    osu_data = OsuData(client_login["oath_code"], client_login["client_id"])
    x = osu_data.get_user_plays("lifeline", 50, "best")
    print(x)