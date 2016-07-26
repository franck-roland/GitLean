from .GitlabElementFactory import GitlabElementFactory
from kanban.models.KanbanNote import KanbanNote
from models.Note import Note


class NoteFactory(GitlabElementFactory):

    @classmethod
    def kanbanFactory(cls, project, issue, id=0, json_note={}):
        return KanbanNote(project, issue, id, json_note)

    @classmethod
    def normalFactory(cls, project, issue, id=0, json_note={}):
        return Note(project, issue, id, json_note)
