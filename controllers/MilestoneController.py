import requests
import config
from .AbstractGitlabElementController import AbstractGitlabElementController
from models.Milestone import Milestone


class MilestoneController(AbstractGitlabElementController):

    def __init__(self, project, _id=None, _json={}):

        self._project = project

        if _json:
            self._milestone = Milestone(project, _json=_json)
        elif _id:
            self._milestone = MilestoneController.find(project, _id)
        else:
            raise ValueError()

    def getProject(self):
        return self._project

    def getMilestone(self):
        return self._milestone

    def getModel(self):
        return self._milestone

    @classmethod
    def getCacheKey(cls, project, _id):
        return "projects:{}:milestones:{}".format(project.id, _id)

    @classmethod
    def getCacheListKey(cls, project, *args):
        return "projects:{}:milestones".format(project.id)

    @classmethod
    def requestsById(cls, project, _id):
        return requests.get("{}/api/v3/projects/{}/milestones/{}".format(config.HOST, project.id, _id), headers={"PRIVATE-TOKEN": config.PRIVATE_TOKEN}).json()

    @classmethod
    def requestsAll(cls, project, page, per_page):
        request = "{}/api/v3/projects/{}/milestones".format(config.HOST, project.id)
        request_parameters = "page={}&per_page={}".format(page, per_page)
        return requests.get(request + "?" + request_parameters, headers={"PRIVATE-TOKEN": config.PRIVATE_TOKEN}).json()
