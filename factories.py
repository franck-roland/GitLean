import config
from abc import ABCMeta
from kanban.models.KanbanIssue import KanbanIssue
from kanban.models.KanbanNote import KanbanNote
from models import Issue
from models import Note


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


class IssueFactory(GitlabElementFactory):

    @classmethod
    def kanbanFactory(cls, project, _json={}):
        return KanbanIssue(project, _json)

    @classmethod
    def normalFactory(cls, project, _json={}):
        return Issue(project, _json)


class NoteFactory(GitlabElementFactory):

    @classmethod
    def kanbanFactory(cls, issue, _json={}):
        return KanbanNote(issue, _json=_json)

    @classmethod
    def normalFactory(cls, issue, _json={}):
        return Note(issue, _json=_json)
