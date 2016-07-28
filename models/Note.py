from dateutil.parser import parse


class Note:

    def __init__(self, issue, _json={}):
        self.id = _json['id']
        self.body = _json['body']
# self.created_at = 0
# if 'created_at' in _json:
        self.created_at = parse(_json['created_at'])
        self.author_id = _json['author']['id']
        self.issue = issue
