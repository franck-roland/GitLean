import config
import requests
from .Commit import Commit


class Tag:

    def __init__(self, project, name="", _json={}):
        if len(name.strip()):
            _json = requests.get("{}/api/v3/projects/{}/repository/tags/{}".format(config.HOST, project.id, name), headers={"PRIVATE-TOKEN": config.PRIVATE_TOKEN}).json()
        self.name = _json['name']
        self.commit = Commit(project, sha=_json['commit']['id'])
        self.release = _json['release']
        self.message = _json['message']
