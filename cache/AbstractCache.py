from abc import ABCMeta, abstractmethod


class AbstractCache(metaclass=ABCMeta):

    @abstractmethod
    def get(self, _id):
        pass

    @abstractmethod
    def set(self, _id, value, expire=60):
        pass

    @abstractmethod
    def findAllLike(self, pattern):
        pass

    @abstractmethod
    def findList(self, _id):
        pass

    @abstractmethod
    def pushToList(self, _id, *args):
        pass

    @abstractmethod
    def delete(self, _id):
        pass
