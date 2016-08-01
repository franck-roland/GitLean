from .GitlabElementFactory import GitlabElementFactory
from kanban.models.KanbanIssue import KanbanIssue
from models import Issue


class IssueFactory(GitlabElementFactory):

    @classmethod
    def kanbanFactory(cls, project, _json={}):
        return KanbanIssue(project, _json)

    @classmethod
    def normalFactory(cls, project, _json={}):
        return Issue(project, _json)
