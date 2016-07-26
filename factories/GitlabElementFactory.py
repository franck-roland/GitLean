import config
from abc import ABCMeta


class GitlabElementFactory(metaclass=ABCMeta):

    @classmethod
    def factory(cls, *args, **kwargs):
        if config.MANAGEMENT_ENV == "kanban":
            return cls.kanbanFactory(*args, **kwargs)
        else:
            return cls.normalFactor(*args, **kwargs)

    @classmethod
    def kanbanFactory(cls, *args, **kwargs):
        pass

    @classmethod
    def normalFactory(cls, *args, **kwargs):
        pass
