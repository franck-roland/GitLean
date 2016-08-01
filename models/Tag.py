

class Tag:

    def __init__(self, project, _json={}):
        self.name = _json['name']
        self.commit_id = _json['commit']['id']
        self.release = _json['release']
        self.message = _json['message']
