from controllers.NoteController import NoteController


class Issue:

    def __init__(self, project, _json={}):
        self.project = project
        self.id = _json['id']
        self.project_id = _json['project_id']
        self.author_id = _json['author']['id']

        self.assignee_id = 0
        if _json['assignee']:
            self.assignee_id = _json['assignee']['id']

        self.milestone_id = 0
        if _json['milestone']:
            self.milestone_id = _json['milestone']['id']

        self.description = _json['description']
        self.state = _json['state']
        self.iid = _json['iid']
        self.labels = _json['labels']
        self.title = _json['title']
        self.updated_at = _json['updated_at']
        self.created_at = _json['created_at']
        self.due_date = 0
        if 'due_date' in _json:
            self.due_date = _json['due_date']
        self.notes = []

    def findAllNotes(self):
        if not self.notes:
            self.notes = sorted(NoteController(self).findAll(), key=lambda x: x.created_at)
        return self.notes
