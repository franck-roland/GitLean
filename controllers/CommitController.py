import requests
import config
from .AbstractGitlabElementController import AbstractGitlabElementController
from models.Commit import Commit


class CommitController(AbstractGitlabElementController):

    def __init__(self, project, _id=None, _json={}):

        self.project = project
        self._id = _id
        self.commit = None
        if _json:
            self.commit = Commit(project, _json=_json)

    def getInstanciationFields(self):
        return [self.project]

    def getProject(self):
        return self.project

    def getCommit(self):
        return self.commit

    def getModel(self):
        return self.commit

    def getCacheKey(self):
        return "projects:{}:commits:{}".format(self.project.id, self._id)

    def getCacheListKey(self):
        return "projects:{}:commits".format(self.project.id)

    def requestsById(self):
        return requests.get("{}/api/v3/projects/{}/repository/commits/{}".format(config.HOST, self.project.id, self._id), headers={"PRIVATE-TOKEN": config.PRIVATE_TOKEN}).json()

    def requestsAll(self, page, per_page):
        # No pagination on /commits
        if page != 1:
            return []
        request = "{}/api/v3/projects/{}/repository/commits".format(config.HOST, self.project.id)
        request_parameters = "page={}&per_page={}".format(page, per_page)
        print(request + "?" + request_parameters)
        return requests.get(request + "?" + request_parameters, headers={"PRIVATE-TOKEN": config.PRIVATE_TOKEN}).json()
