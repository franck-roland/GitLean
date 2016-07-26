import requests
import config
from factories.IssueFactory import IssueFactory
from dateutil.parser import parse


class Milestone:

    def __init__(self, project, _id=None, _json={}):
        if _id:
            _json = requests.get(
                "{}/api/v3/projects/{}/milestones/{}".format(
                    config.HOST, project.id, _id),
                headers={"PRIVATE-TOKEN": config.PRIVATE_TOKEN}).json()
        print(_json)
        self.id = _json['id']
        self.iid = _json['iid']
        self.project = project
        self.title = _json['title']
        self.description = _json['description']
        self.due_date = _json['due_date']
        if self.due_date:
            self.due_date = parse(self.due_date)
        self.state = _json['state']
        self.updated_at = _json['updated_at']
        self.created_at = _json['created_at']
        self.issues = []

    def findAllIssues(self):
        if not self.issues:
            _jsons = requests.get(
                "{}/api/v3/projects/{}/issues/?milestone={}".format(
                    config.HOST, self.project.id, self.title),
                headers={"PRIVATE-TOKEN": config.PRIVATE_TOKEN}).json()
            self.issues = [IssueFactory.factory(self.project, _json=_json) for _json in _jsons]
        return self.issues
