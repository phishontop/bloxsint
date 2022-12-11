import requests


class Post:

    def __init__(self, data: dict) -> None:
        """Represents a group wall post

        Params:
            data: post information
        """

        self.user_id = data["poster"]["user"]["userId"]
        self.username = data["poster"]["user"]["username"]
        self.message = data["body"]
        self.date = data["created"]


class Group:

    def __init__(self, data: dict) -> None:
        """Represents a group

        Params:
            data: group information
        """

        self.id = data["id"]
        self.name = data["name"]
        self.member_count = data["memberCount"]

    def get_posts(self) -> list:
        """Gathers the first 100 group wall posts of the group

        Returns:
            list: Post objects, can't be more than 100 objects
        """

        response = requests.get(f"https://groups.roblox.com/v2/groups/{self.id}/wall/posts?sortOrder=Desc&limit=100")
        response_json = response.json()
        posts = []
        if "errors" not in response_json:
            for post in response_json["data"]:
                if post["poster"]:
                    posts.append(Post(post))

        return posts


class GroupScraper:

    def __init__(self, user_id: int) -> None:
        self.user_id = user_id

    def get_groups(self) -> list:
        """Checks to see if the users role in the groups is the owner

        Returns:
            list:  group objects owned by the user
        """

        response = requests.get(f"https://groups.roblox.com/v2/users/{self.user_id}/groups/roles")
        groups = []
        for user_group in response.json()["data"]:
            if user_group["role"]["rank"] == 255:
                groups.append(Group(user_group["group"]))

        return groups

    @staticmethod
    def close_convo(post) -> bool:
        close = ["thx", "ty", "thank", "thanks"]
        for word in close:
            if word in post.message.lower():
                return True

        return False

    @staticmethod
    def parse_opening(post) -> dict:
        opening = {
            "birthday": {
                "keywords": ["birthday", "bday", "hbd", "b-day", "birfday"],
                "log": post.date.split("T")[0]
            }
        }

        for name, option in opening.items():
            for keyword in option["keywords"]:
                if keyword in post.message.lower():
                    return {name: option["log"]}

        return {}

    def get_posts(self) -> list:
        posts = []
        groups = self.get_groups()
        for group in groups:
            posts += group.get_posts()

        return posts

    def parse_posts(self):
        parsed_information = {}
        posts = self.get_posts()
        for ranking, post in enumerate(posts):
            if post.user_id == self.user_id:
                if GroupScraper.close_convo(post):
                    response = GroupScraper.parse_opening(
                        posts[ranking+1]
                    )

                    parsed_information = {**response, **parsed_information}

        return parsed_information
