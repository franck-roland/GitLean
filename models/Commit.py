

class Commit:

    def __init__(self, project, _json={}):
        self.project = project
        self.sha = _json['id']
        self.committed_date = None
        if 'committed_date' in _json:
            self.committed_date = _json['committed_date']
        self.message = _json['message']
        self.author_email = _json['author_email']
        self.author_name = _json['author_name']
        self.authored_date = None
        if 'authored_date' in _json:
            self.authored_date = _json['authored_date']
        self.status = None
        if 'status' in _json:
            self.status = _json['status']
        self.created_at = _json['created_at']
        self.title = _json['title']
        self.short_id = _json['short_id']
        self.parent_ids = []
        if 'parent_ids' in _json:
            self.parent_ids = _json['parent_ids']

    def getParents(self):
        from controllers.CommitController import CommitController
        return [CommitController(self.project, _id).find() for _id in self.parent_ids]
