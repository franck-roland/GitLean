from .AbstractCache import AbstractCache


class NoCache(AbstractCache):

    def get(self, _id):
        return None

    def set(self, _id, _dict, expire=60):
        return True

    def findAllLike(self, pattern):
        return []

    def findList(self, _id):
        return []

    def pushToList(self, _id, *args):
        return True

    def delete(self, _id):
        return True

    def removeAllValues(self, _id, value):
        return True
