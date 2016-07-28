import requests
import config
from controllers.IssueController import IssueController
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
            self.issues = IssueController.findAll(self.project, milestone=self)
        return self.issues
