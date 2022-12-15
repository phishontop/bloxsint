import requests


class Inviter:

    def __init__(self, data: dict) -> None:
        """Represents the inviter of a discord invite"""
        self.id = data["id"]
        self.username = f'{data["username"]}#{data["discriminator"]}'


class DiscordInvite:

    def __init__(self, data: dict) -> None:
        """Represents a discord server invite"""
        self.inviter = Inviter(data["inviter"])
        self.guild_name = data["guild"]["name"]
        self.code = data["code"]


class DiscordFactory:

    @staticmethod
    def create_invite(code):
        """Factory for creating the DiscordInvite object

        Arguments:
            code: invite code for a discord server

        Returns:
            DiscordInvite: if invalid return None
        """
        response = requests.get(f"https://discordapp.com/api/invite/{code}")
        response_json = response.json()
        if response_json["code"] == 10006:
            # Invite invalid return None
            return None

        else:
            # Invite valid create DiscordInvite object
            return DiscordInvite(response_json)

