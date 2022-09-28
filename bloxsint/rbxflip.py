from .utils.http import *


class Rbxflip:
    
    def __init__(self, robloxId):
        self.robloxId = robloxId
        self.username = self.getUsername()
        
    def getUsername(self):
        r = http.get(f"https://users.roblox.com/v1/users/{self.robloxId}")
        return r.json()["name"]
    
    def getData(self):
        data = http.get(f"https://legacy.rbxflip-apis.com/users/{self.username}")
        return data.json()
        
        
    