from .GitlabElementFactory import GitlabElementFactory
from kanban.models.KanbanNote import KanbanNote
from models.Note import Note


class NoteFactory(GitlabElementFactory):

    @classmethod
    def kanbanFactory(cls, project, issue, id=0, _json={}):
        return KanbanNote(project, issue, id, _json)

    @classmethod
    def normalFactory(cls, project, issue, id=0, _json={}):
        return Note(project, issue, id, _json)
