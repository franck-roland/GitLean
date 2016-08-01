import re
from models import Issue

regex = re.compile("KB\[stage\]\[[0-9]+\]\[([a-zA-Z]+)\]")


class KanbanIssue(Issue):

    def __init__(self, project, _json={}):
        super(KanbanIssue, self).__init__(project, _json)

        self.kanban_state = None
        for label in self.labels:
            match = regex.match(label)
            if match:
                self.kanban_state = match.groups()[0]

        self.kanban_transition_notes = []

    def findAllTransitionNotes(self):
        if not self.kanban_transition_notes:
            self.kanban_transition_notes = sorted([note for note in self.findAllNotes() if getattr(note, 'kanban_state_to', '')], key=lambda x: x.created_at)
        return self.kanban_transition_notes
