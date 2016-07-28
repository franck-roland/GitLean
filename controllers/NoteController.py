import requests
import config
from .AbstractGitlabElementController import AbstractGitlabElementController
from factories.NoteFactory import NoteFactory


class NoteController(AbstractGitlabElementController):

    def __init__(self, issue, _id=None, _json={}):

        self.issue = issue
        self._id = _id
        self._note = None
        if _json:
            self._note = NoteFactory.factory(issue, _json=_json)

    def getInstanciationFields(self):
        return [self.issue]

    def getIssue(self):
        return self.issue

    def getNote(self):
        return self._note

    def getModel(self):
        return self._note

    def getCacheKey(self):
        return "projects:{}:issues:{}:notes:{}".format(self.issue.project.id, self.issue.id, self._id)

    def getCacheListKey(self):
        return "projects:{}:issues:{}:notes".format(self.issue.project.id, self.issue.id)

    def requestsById(self):
        return requests.get("{}/api/v3/projects/{}/issues/{}/notes/{}".format(config.HOST, self.issue.project.id, self.issue.id, self._id), headers={"PRIVATE-TOKEN": config.PRIVATE_TOKEN}).json()

    def requestsAll(self, page, per_page):
        return requests.get("{}/api/v3/projects/{}/issues/{}/notes?page={}&per_page={}".format(config.HOST, self.issue.project.id, self.issue.id, page, per_page), headers={"PRIVATE-TOKEN": config.PRIVATE_TOKEN}).json()
