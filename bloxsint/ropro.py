from .utils.http import *


class Ropro:
    
    def __init__(self, robloxId):
        self.robloxId = robloxId
        
    def getData(self):
        data = http.get(f"https://api.ropro.io/getUserInfoTest.php?userid={self.robloxId}&myid=1")
        return data.json()