import requests
import config
from models.Project import Project
from .AbstractGitlabElementController import AbstractGitlabElementController


class ProjectController(AbstractGitlabElementController):

    def __init__(self, _id=None, _json={}):

        self._id = _id
        self.project = None
        if _json:
            self.project = Project(_json=_json)

    def getInstanciationFields(self):
        return []

    def getProject(self):
        return self.project

    def getModel(self):
        return self.project

    def getCacheKey(self):
        if not self._id:
            raise ValueError
        return "projects:{}".format(self._id)

    def getCacheListKey(self):
        return "projects"

    def requestsById(self):
        if not self._id:
            raise ValueError
        return requests.get("{}/api/v3/projects/{}".format(config.HOST, self._id), headers={"PRIVATE-TOKEN": config.PRIVATE_TOKEN}).json()

    def requestsAll(self, page, per_page):
        return requests.get("{}/api/v3/projects?page={}&per_page={}".format(config.HOST, page, per_page), headers={"PRIVATE-TOKEN": config.PRIVATE_TOKEN}).json()
