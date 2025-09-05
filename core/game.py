import requests
import threading


class Game:

    def __init__(self, data: dict) -> None:
        self.badge_id = data["id"]
        self.id = data["awardingUniverse"]["id"]
        self.name = data["awardingUniverse"]["name"]


class GameScraper:

    def __init__(self, user_id: int, game_limit: int) -> None:
        self.user_id = user_id
        self.game_limit = int(game_limit)
        self.badge_ids = []
        self.games = []
        self.session = requests.Session()

    def fetch_badge_ids(self) -> None:
        cursor = ""
        while isinstance(cursor, str):
            response = requests.get(
                f"https://badges.roblox.com/v1/users/{self.user_id}/badges?limit=100&sortOrder=Desc&cursor={cursor}"
            )

            response_json = response.json()
            try:
                for badge in response_json["data"]:
                    self.badge_ids.append(badge["id"])

                cursor = response_json["nextPageCursor"]

            except KeyError:
                break

            if len(self.badge_ids) > self.game_limit:
                break

    def get_game(self, badge_id: int) -> None:
        try:
            with self.session as session:
                response = session.get(f"https://badges.roblox.com/v1/badges/{badge_id}")

            game = Game(response.json())
            if game.name not in self.games:
                self.games.append(game.name)

        except requests.exceptions.ConnectionError:
            pass

        except KeyError:
            pass

    def fetch_games(self) -> None:
        threads = []
        for badge_id in self.badge_ids:
            threads.append(threading.Thread(target=self.get_game, args=(badge_id,)))

        for thread in threads:
            thread.start()

        for thread in threads:
            thread.join()

    def run(self) -> list:
        self.fetch_badge_ids()
        self.fetch_games()
        return self.games
