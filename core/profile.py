import requests
import string


class ProfileScraper:

    def __init__(self, user_id: int) -> None:
        self.user_id = user_id
        self.stats = {}

    @property
    def bio(self) -> str:
        response = requests.get(f"https://users.roblox.com/v1/users/{self.user_id}")
        return response.json()["description"]

    @staticmethod
    def valid_word(word: str, requirements: [dict, list]) -> bool:
        if len(word) == requirements["length"] or requirements["length"] == 999:
            if requirements["end"]:
                return ProfileScraper.valid_end(word=word, end_dict=requirements["end"])

            if requirements["has"]:
                return ProfileScraper.valid_has(word=word, has_list=requirements["has"])

            return word.isnumeric() == requirements["number"]

    @staticmethod
    def valid_end(word: str, end_dict: dict) -> bool:
        if len(word) > end_dict["length"]:
            return word[-end_dict["length"]:].isnumeric() == end_dict["number"]
        else:
            return False

    @staticmethod
    def valid_has(word: str, has_list: list) -> bool:
        for char in string.punctuation:
            word = word.replace(char, " ")

        for word in word.split(" "):
            for need in has_list:
                if need.lower() == word.lower():
                    return True

        return False

    @staticmethod
    def check_word(name, word, requirement) -> dict:
        if ProfileScraper.valid_word(word=word, requirements=requirement):
            return {name: requirement['value']}
        else:
            return {}

    def scrape_data(self, count, words) -> None:
        word = words[count]
        scrape_dict = {
            "age": {"length": 2, "value": word, "number": True, "end": None, "has": None},
            "gender": [
                {"length": 999, "value": "male", "number": False, "end": None, "has": ["he", "him", "his"]},
                {"length": 999, "value": "female", "number": False, "end": None, "has": ["she", "her", "hers"]},
            ],

            "discord": [
                {"length": 4, "value": f"{words[count - 1]}#{word}", "number": True, "end": None, "has": None},
                {"length": 999, "value": word, "number": False, "has": None, "end": {"number": True, "length": 4}}
            ]
        }

        for name, requirements in scrape_dict.items():
            if isinstance(requirements, list):
                for requirement in requirements:
                    response = ProfileScraper.check_word(name=name, word=word, requirement=requirement)
                    self.stats = {**response, **self.stats}

            else:
                response = ProfileScraper.check_word(name=name, word=word, requirement=requirements)
                self.stats = {**response, **self.stats}

    def scrape_bio(self) -> dict:
        words = self.bio.split()
        for count, word in enumerate(words):
            self.scrape_data(count, words)

        return self.stats
