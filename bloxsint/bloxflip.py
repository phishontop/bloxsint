from .utils.http import *


class Bloxflip:
    
    def __init__(self, robloxId):
        self.robloxId = robloxId
        
    def getData(self):
        data = http.get(f"https://api.bloxflip.com/user/lookup/{self.robloxId}")
        return data.json()
