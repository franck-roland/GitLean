from .Commit import Commit


class Tag:

    def __init__(self, project, _json={}):
        self.name = _json['name']
        self.commit = Commit(project, sha=_json['commit']['id'])
        self.release = _json['release']
        self.message = _json['message']
