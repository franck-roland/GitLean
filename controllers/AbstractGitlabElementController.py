from abc import ABCMeta


class AbstractGitlabElementController(metaclass=ABCMeta):

    @classmethod
    def find(cls, _id):
        pass

    @classmethod
    def findAll(cls):
        pass

    @classmethod
    def __findFromHTTPQuery(cls, _id):
        pass

    @classmethod
    def __findAllFromHTTPQuery(cls):
        pass
