import re
from models.Note import Note

regex = re.compile(".*from \*\*([a-zA-Z]+)\*\* to \*\*([a-zA-Z]+)\*\*.*")


class KanbanNote(Note):

    def __init__(self, project, issue, id=0, json_note={}):
        super(KanbanNote, self).__init__(project, issue, id, json_note)
        column_state_match = regex.match(self.body)
        self.kanban_state_from = None
        self.kanban_state_to = None
        if column_state_match:
            self.kanban_state_from = column_state_match.groups()[0]
            self.kanban_state_to = column_state_match.groups()[1]
