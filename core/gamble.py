import requests


class GambleScraper:

    def __init__(self, user_id: int) -> None:
        self.user_id = user_id
        self.stats = {}
        self.headers = {"User-Agent": "Mozilla/5.0 (X11; CrOS armv7l 13597.84.0) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/104.0.5112.105 Safari/537.36"}

    def rbxflip(self) -> None:
        try:
            links = {"money_profit": 0, "robux_profit": 1}
            profits = {}
            for currency, game_id in links.items():
                response = requests.get(f"https://api.rbxflip.com/wagers/users/{self.user_id}/history?page=0&gameKind={game_id}")
                total_profit = response.json()["metadata"]["totalProfit"]
                if total_profit != 0:
                    profits[currency] = total_profit

                if profits:
                    self.stats["rbxflip"] = profits
        except:
            pass

    def bloxflip(self) -> None:
        try:
            response = requests.get(f"https://api.bloxflip.com/user/lookup/{self.user_id}", headers=self.headers)
            response_json = response.json()
            if not response_json["success"]:
                return

            for word in ["username", "success"]:
                response_json.pop(word)

            self.stats["bloxflip"] = response_json

        except:
            pass

    def run(self):
        self.rbxflip()
        self.bloxflip()
        return self.stats
