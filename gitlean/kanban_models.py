import re
from .models import Issue, Note


class KanbanIssue(Issue):
    regex = re.compile("KB\[stage\]\[[0-9]+\]\[([a-zA-Z]+)\]")

    def __init__(self, project, _json={}):
        super(KanbanIssue, self).__init__(project, _json)

        self.kanban_state = None
        for label in self.labels:
            match = KanbanIssue.regex.match(label)
            if match:
                self.kanban_state = match.groups()[0]

        self.kanban_transition_notes = []

    def findAllTransitionNotes(self):
        if not self.kanban_transition_notes:
            self.kanban_transition_notes = sorted([note for note in self.findAllNotes() if getattr(note, 'kanban_state_to', '')], key=lambda x: x.created_at)
        return self.kanban_transition_notes


class KanbanNote(Note):
    regex = re.compile(".*from \*\*([a-zA-Z]+)\*\* to \*\*([a-zA-Z]+)\*\*.*")

    def __init__(self, issue, _json={}):
        super(KanbanNote, self).__init__(issue, _json)
        column_state_match = KanbanNote.regex.match(self.body)
        self.kanban_state_from = None
        self.kanban_state_to = None
        if column_state_match:
            self.kanban_state_from = column_state_match.groups()[0]
            self.kanban_state_to = column_state_match.groups()[1]
