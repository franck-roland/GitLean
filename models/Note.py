import requests
import config
from dateutil.parser import parse


class Note:

    def __init__(self, project, issue, id=0, json_note={}):
        if id:
            json_note = requests.get("{}/api/v3/projects/{}/issues/{}/notes/{}".format(config.HOST, project.id, issue.id, id), headers={"PRIVATE-TOKEN": config.PRIVATE_TOKEN}).json()
        self.id = json_note['id']
        self.body = json_note['body']
# self.created_at = 0
# if 'created_at' in json_note:
        self.created_at = parse(json_note['created_at'])
        self.author_id = json_note['author']['id']
