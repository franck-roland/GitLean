from .GitlabElementFactory import GitlabElementFactory
from kanban.models.KanbanNote import KanbanNote
from models import Note


class NoteFactory(GitlabElementFactory):

    @classmethod
    def kanbanFactory(cls, issue, _json={}):
        return KanbanNote(issue, _json=_json)

    @classmethod
    def normalFactory(cls, issue, _json={}):
        return Note(issue, _json=_json)
