import requests
import config
from .AbstractGitlabElementController import AbstractGitlabElementController
from models.Commit import Commit


class CommitController(AbstractGitlabElementController):

    def __init__(self, project, _id=None, _json={}):

        self._project = project

        if _json:
            self._commit = Commit(project, _json=_json)
        elif _id:
            self._commit = CommitController.find(project, _id)
        else:
            raise ValueError()

    def getProject(self):
        return self._project

    def getCommit(self):
        return self._commit

    def getModel(self):
        return self._commit

    @classmethod
    def getCacheKey(cls, project, _name):
        return "projects:{}:commits:{}".format(project.id, _name)

    @classmethod
    def getCacheListKey(cls, project, *args):
        return "projects:{}:commits".format(project.id)

    @classmethod
    def requestsById(cls, project, _id):
        return requests.get("{}/api/v3/projects/{}/repository/commits/{}".format(config.HOST, project.id, _id), headers={"PRIVATE-TOKEN": config.PRIVATE_TOKEN}).json()

    @classmethod
    def requestsAll(cls, project, page, per_page):
        # No pagination on /commits
        if page != 1:
            return []
        request = "{}/api/v3/projects/{}/repository/commits".format(config.HOST, project.id)
        request_parameters = "page={}&per_page={}".format(page, per_page)
        return requests.get(request + "?" + request_parameters, headers={"PRIVATE-TOKEN": config.PRIVATE_TOKEN}).json()
