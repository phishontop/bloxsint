from .utils.http import *


class Games:
    
    def __init__(self, robloxId):
        self.robloxId = robloxId
        self.universeIds = []
        self.gamesPlayed = []
        
    def getBadges(self):
        placeIds = []
        badges = http.get(f"https://badges.roblox.com/v1/users/{self.robloxId}/badges?limit=25&sortOrder=Desc")
        for badge in badges.json()["data"]:
            placeIds.append(
                badge["awarder"]["id"]    
            )
            
        return placeIds
    
    def getGamesPlayed(self):
        universeIdString = ",".join(self.universeIds)
        gameInfo = http.get(f"https://games.roblox.com/v1/games?universeIds={universeIdString}")
        for game in gameInfo.json()["data"]:
            self.gamesPlayed.append(
                game["name"]
            )
        return self.gamesPlayed

    def getUniverseId(self, placeId):
        r = http.get(f"https://api.roblox.com/universes/get-universe-containing-place?placeid={placeId}")
        
        self.universeIds.append(
            str(r.json()["UniverseId"])
        )