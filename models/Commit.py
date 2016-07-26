import requests
import config


class Commit:

    def __init__(self, project, sha=None, _json={}):
        if sha:
            _json = requests.get(
                "{}/api/v3/projects/{}/repository/commits/{}".format(
                    config.HOST, project.id, sha),
                headers={"PRIVATE-TOKEN": config.PRIVATE_TOKEN}).json()
        self.sha = _json['id']
        self.committed_date = _json['committed_date']
        self.message = _json['message']
        self.author_email = _json['author_email']
        self.author_name = _json['author_name']
        self.authored_date = _json['authored_date']
        self.status = _json['status']
        self.created_at = _json['created_at']
        self.title = _json['title']
        self.short_id = _json['short_id']
