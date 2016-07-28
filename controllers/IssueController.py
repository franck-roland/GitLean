import requests
import config
from .AbstractGitlabElementController import AbstractGitlabElementController
from factories.IssueFactory import IssueFactory


class IssueController(AbstractGitlabElementController):

    def __init__(self, project, _id=None, _json={}):

        self.project = project
        self._id = _id
        self.issue = None
        if _json:
            self.issue = IssueFactory.factory(project, _json=_json)

    def getInstanciationFields(self):
        return [self.project]

    def getProject(self):
        return self.project

    def getIssue(self):
        return self.issue

    def getModel(self):
        return self.issue

    def getCacheKey(self):
        return "projects:{}:issues:{}".format(self.project.id, self._id)

    def getCacheListKey(self):
        return "projects:{}:issues".format(self.project.id)

    def requestsById(self):
        return requests.get("{}/api/v3/projects/{}/issues/{}".format(config.HOST, self.project.id, self._id), headers={"PRIVATE-TOKEN": config.PRIVATE_TOKEN}).json()

    def requestsAll(self, page, per_page, milestone=None):
        request = "{}/api/v3/projects/{}/issues".format(config.HOST, self.project.id)
        request_parameters = "page={}&per_page={}".format(page, per_page)
        if milestone:
            request_parameters += "&milestone=" + milestone.title
        return requests.get(request + "?" + request_parameters, headers={"PRIVATE-TOKEN": config.PRIVATE_TOKEN}).json()
