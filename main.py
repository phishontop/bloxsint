from core import *


class Lookup:

    def __init__(self) -> None:
        self.roblox_id = int(input("Enter Roblox ID -> "))
        self.stats = {}

    def run(self):
        functions = {
            "friends": FriendScraper(user_id=self.roblox_id).parse_friends,
            "gambling_info": GambleScraper(user_id=self.roblox_id).run,
            "personal_info": [
                GroupScraper(user_id=self.roblox_id).parse_posts,
                ProfileScraper(user_id=self.roblox_id).scrape_bio
            ],
            "games_played": GameScraper(user_id=self.roblox_id).run
        }

        for key, func in functions.items():
            self.stats[key] = Lookup.run_func(func)

    @staticmethod
    def run_func(func):
        results = {}
        if isinstance(func, list):
            for i in func:
                results = {**i(), **results}
        else:
            results = func()

        return results


bloxsint = Lookup()
bloxsint.run()
print(bloxsint.stats)
