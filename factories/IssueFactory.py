from .GitlabElementFactory import GitlabElementFactory
from kanban.models.KanbanIssue import KanbanIssue
from models.Issue import Issue


class IssueFactory(GitlabElementFactory):

    @classmethod
    def kanbanFactory(cls, project, id=None, _json={}):
        return KanbanIssue(project, id, _json)

    @classmethod
    def normalFactory(cls, project, id=None, _json={}):
        return Issue(project, id, _json)
