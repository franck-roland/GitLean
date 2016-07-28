import requests
import config
from models.Project import Project
from .AbstractGitlabElementController import AbstractGitlabElementController


class ProjectController(AbstractGitlabElementController):

    def __init__(self, _id=None, _json={}):

        if _json:
            self._project = Project(_json=_json)
        elif _id:
            self._project = ProjectController.find(_id)
        else:
            raise ValueError()

    def getProject(self):
        return self._project

    def getModel(self):
        return self._project

    @classmethod
    def getCacheKey(cls, _id):
        return "projects:{}".format(_id)

    @classmethod
    def getCacheListKey(cls, *args):
        return "projects"

    @classmethod
    def requestsById(cls, _id):
        return requests.get("{}/api/v3/projects/{}".format(config.HOST, _id), headers={"PRIVATE-TOKEN": config.PRIVATE_TOKEN}).json()

    @classmethod
    def requestsAll(cls, page, per_page):
        return requests.get("{}/api/v3/projects?page={}&per_page={}".format(config.HOST, page, per_page), headers={"PRIVATE-TOKEN": config.PRIVATE_TOKEN}).json()
