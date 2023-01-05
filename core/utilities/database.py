import pymongo


class Database:

    def __init__(self, url: str) -> None:
        self.database = pymongo.MongoClient(url)["bloxsint"]["users"]

    def query(self, search: dict):
        results = []
        query_result = self.database.find(search)
        for result in query_result:
            results.append(result)

        return results

    def insert(self, data: dict):
        self.database.insert_one(data)
