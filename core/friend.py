import requests


class Friend:

    def __init__(self, data: dict) -> None:
        self.username = data["name"]
        self.display_name = data["displayName"]


class FriendScraper:

    def __init__(self, user_id: int) -> None:
        self.user_id = user_id

    @staticmethod
    def get_names() -> list:
        response = requests.get("https://raw.githubusercontent.com/dominictarr/random-name/master/first-names.txt")
        return response.text.splitlines()

    def parse_friends(self) -> list:
        friend_names = []
        names = FriendScraper.get_names()
        friends = self.get_friends()
        for friend in friends:
            if friend.display_name.title() in names and friend.display_name != friend.username:
                friend_names.append(
                    friend.display_name
                )

        return friend_names

    def get_friends(self) -> list:
        response = requests.get(f"https://friends.roblox.com/v1/users/{self.user_id}/friends?userSort=StatusFrequents")
        friends = []
        for user in response.json()["data"]:
            friends.append(Friend(user))

        return friends
