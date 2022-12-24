import requests


class WebsiteScraper:
    
    def __init__(self, user_id: int) -> None:
        self.user_id = user_id
        self.stats = {}
        
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
                stats = {**response.json(), **stats}
                

        return stats
            
        
    @property
    def username(self) -> str:
        response = requests.get(f"https://users.roblox.com/v1/users/{self.user_id}")
        return response.json()["name"]

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
                        "log": True
                    }
                    
                ]
                
            }
        }

        for options in websites.values():
            if options.get("steps"):
                step_stats = self.parse_steps(steps=options["steps"])
                self.stats[options["base_url"]] = step_stats

            else:
                url = options["url"].format(options["arg"])
                response = requests.get(url)
                if options["not_found"] not in response.text:
                    self.stats[options["base_url"]] = response.json()[options["data_key"]]

    def run(self):
        self.scrape_info()
        return self.stats
