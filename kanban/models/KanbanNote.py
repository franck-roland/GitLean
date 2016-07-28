import re
from models.Note import Note

regex = re.compile(".*from \*\*([a-zA-Z]+)\*\* to \*\*([a-zA-Z]+)\*\*.*")


class KanbanNote(Note):

    def __init__(self, issue, _json={}):
        super(KanbanNote, self).__init__(issue, _json)
        column_state_match = regex.match(self.body)
        self.kanban_state_from = None
        self.kanban_state_to = None
        if column_state_match:
            self.kanban_state_from = column_state_match.groups()[0]
            self.kanban_state_to = column_state_match.groups()[1]
