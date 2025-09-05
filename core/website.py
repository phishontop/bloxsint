import requests


class WebsiteScraper:
    
    def __init__(self, user_id: int) -> None:
        self.user_id = user_id
        self._username = None
        self.stats = {}

    @staticmethod
    def parse_log_option(step: dict, response) -> bool:
        log_options = step["log_option"]
        if log_options:
            if log_options["type"] == "float":
                return float(response.json()[log_options["key"]]) > log_options["more"]

        else:
            return False

    def parse_steps(self, steps: list) -> dict:
        stats = {}
        session = requests.Session()
        for step in steps:

            if step.get("payload"):
                response = session.post(
                    url=step["url"],
                    json=step["payload"],
                    headers=step["headers"]
                )

            else:
                response = session.get(
                    url=step["url"],
                    headers=step["headers"]
                )

            if step["log"]:
                log_options = step.get("log_option")
                if log_options:
                    if WebsiteScraper.parse_log_option(step=step, response=response):
                        stats = {**response.json(), **stats}

                else:
                    stats = {**response.json(), **stats}

        return stats

    @property
    def username(self) -> str:
        if not self._username:
            response = requests.get(f"https://users.roblox.com/v1/users/{self.user_id}")
            self._username = response.json()["name"]

        return self._username

    def scrape_info(self):
        websites = {
            "bloxboost": {
                "base_url": "https://bloxboost.com",
                "url": "https://api.bloxboost.com/users/info/{}",
                "arg": self.user_id,
                "not_found": "User not found",
                "data_key": "data"
            },
            "buxfun": {
                "base_url": "https://bux.fun/",
                "steps": [
                    {
                        "url": "https://bux.fun/auth/roblox",
                        "payload": {"roblox_username": self.username, "password": ""},
                        "headers": {"User-Agent": "Mozilla/5.0 (X11; CrOS armv7l 13597.84.0) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/104.0.5112.105 Safari/537.36"},
                        "log": False
                    },
                    {
                        "url": "https://bux.fun/api/account/balance2",
                        "headers": {"User-Agent": "Mozilla/5.0 (X11; CrOS armv7l 13597.84.0) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/104.0.5112.105 Safari/537.36"},
                        "log_option": {"key": "balance", "type": "float", "more": 0},
                        "log": True
                    }
                    
                ]
            },
            "bloxearn": {
                "base_url": "https://bloxearn.com/",
                "steps": [
                    {
                        "url": "https://api.bloxearn.com/auth/login",
                        "payload": {"username": self.username},
                        "headers": {"User-Agent": "Mozilla/5.0 (X11; CrOS armv7l 13597.84.0) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/104.0.5112.105 Safari/537.36"},
                        "log": False
                    },
                    {
                        "url": "https://api.bloxearn.com/user",
                        "headers": {"User-Agent": "Mozilla/5.0 (X11; CrOS armv7l 13597.84.0) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/104.0.5112.105 Safari/537.36"},
                        "log": True
                    }
                ]
            }
        }

        for options in websites.values():
            if options.get("steps"):
                step_stats = self.parse_steps(steps=options["steps"])
                if step_stats:
                    self.stats[options["base_url"]] = step_stats

            else:
                url = options["url"].format(options["arg"])
                try:
                    response = requests.get(url)
                    if options["not_found"] not in response.text:
                        self.stats[options["base_url"]] = response.json()[options["data_key"]]

                except:
                    pass

    def run(self):
        self.scrape_info()
        return self.stats
