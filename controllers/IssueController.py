import requests
import config
from cache.factories.CacheFactory import CacheFactory
from .AbstractGitlabElementController import AbstractGitlabElementController
from factories.IssueFactory import IssueFactory


class IssueController(AbstractGitlabElementController):

    def __init__(self, project, _id=None, _json={}):

        self._project = project

        if _json:
            self._issue = IssueFactory.factory(project, _json=_json)
        elif _id:
            self._issue = IssueController.find(_id)
        else:
            raise ValueError()

    def getProject(self):
        return self._project

    def getIssue(self):
        return self._issue

    def getModel(self):
        return self._issue

    @classmethod
    def getCacheKey(cls, project, _id):
        return "projects:{}:issues:{}".format(project.id, _id)

    @classmethod
    def getCacheListKey(cls, project, *args):
        return "projects:{}:issues".format(project.id)

    @classmethod
    def requestsById(cls, project, _id):
        return requests.get("{}/api/v3/projects/{}/issues/{}".format(config.HOST, project.id, _id), headers={"PRIVATE-TOKEN": config.PRIVATE_TOKEN}).json()

    @classmethod
    def requestsAll(cls, project, page, per_page):
        return requests.get("{}/api/v3/projects/{}/issues?page={}&per_page={}".format(config.HOST, project.id, page, per_page), headers={"PRIVATE-TOKEN": config.PRIVATE_TOKEN}).json()
