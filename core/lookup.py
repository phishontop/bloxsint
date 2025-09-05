from .friend import FriendScraper
from .gamble import GambleScraper
from .game import GameScraper
from .group import GroupScraper
from .profile import ProfileScraper
from .website import WebsiteScraper
from .utilities.database import Database
from .names import PreviousNameScraper

import time
import json


class Lookup:

    def __init__(self, roblox_id: int, args) -> None:
        self.roblox_id = roblox_id
        self.args = args
        self.database = None
        self.stats = {"roblox_id": roblox_id}

    def run(self):
        start = time.time()

        if self.args.database:
            self.database = Database(self.args.database)
            result = self.database.query({"roblox_id": self.roblox_id})

            if result:
                self.stats = result[0]

            else:
                self.new_lookup()
                self.database.insert(data=self.stats)

        else:
            self.new_lookup()

        print(f"Lookup completed in {round(time.time() - start, 2)}s")

    def new_lookup(self):
        functions = {
            "friends": FriendScraper(user_id=self.roblox_id).parse_friends,
            # "gambling_info": GambleScraper(user_id=self.roblox_id).run,
            "personal_info": [
                GroupScraper(user_id=self.roblox_id, cookie=self.args.cookie).parse_posts,
                ProfileScraper(user_id=self.roblox_id).scrape_bio
            ],
            "games_played": GameScraper(user_id=self.roblox_id, game_limit=self.args.game_limit).run,
            # "websites": WebsiteScraper(user_id=self.roblox_id).run,
            "previous_names": PreviousNameScraper(user_id=self.roblox_id).get_names
        }

        for key, func in functions.items():
            self.stats[key] = Lookup.run_func(func)

        self.set_game_cap()
        self.dump_stats()

    def set_game_cap(self):
        """Sets the games played to the limit of the game-limit argument (default: 10)"""
        game_limit = int(self.args.game_limit)
        games_played = self.stats["games_played"]

        if game_limit <= len(games_played):
            self.stats["games_played"] = games_played[0:game_limit]

    def dump_stats(self):
        """Dumps the stats to the file if the arg is set"""
        if self.args.file:
            with open(rf"results/{self.args.file}", 'w') as file:
                file.write(json.dumps(self.stats, indent=4))

    @staticmethod
    def run_func(func):
        results = {}
        if isinstance(func, list):
            for i in func:
                results = {**i(), **results}
        else:
            results = func()

        return results
