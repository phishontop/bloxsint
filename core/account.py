import requests
from .discord import DiscordFactory


class Account:

    def __init__(self, cookie: str) -> None:
        """Represents the cookie arg object"""
        self.cookie = cookie

    @property
    def token(self) -> str:
        headers = {"Cookie": f".ROBLOSECURITY={self.cookie}"}
        response = requests.post("https://auth.roblox.com/v2/login", json={}, headers=headers)
        return response.headers['x-csrf-token']

    @staticmethod
    def get_discord_link(data: dict) -> str:
        """Gets the Discord link from the social link

        Returns:
            str: Discord url found if not found returns empty string
        """
        try:
            for social in data["data"]:
                if social["type"] == "Discord":
                    return social["url"]

        except KeyError:
            print(data)

        return ""

    def get_group_discord(self, group) -> dict:
        """Sends get request gathers the discord url if the is one linked to the group object

        Returns:
            dict: Discord Invite object or empty dict if no valid invite found
        """

        response = requests.get(
            url=f"https://groups.roblox.com/v1/groups/{group.id}/social-links",
            headers={"X-CSRF-TOKEN": self.token},
            cookies={".ROBLOSECURITY": self.cookie}
        )

        link = Account.get_discord_link(response.json())

        if link:
            code = link.split("https://discord.gg/")[1]
            invite = DiscordFactory.create_invite(code=code)

            if invite:
                return {
                    f"discord_{invite.code}": {
                        "discord_tag": invite.inviter.username,
                        "discord_id": invite.inviter.id
                    }
                }

        return {}




