import requests
import config
from .AbstractGitlabElementController import AbstractGitlabElementController
from models.Milestone import Milestone


class MilestoneController(AbstractGitlabElementController):

    def __init__(self, project, _id=None, _json={}):

        self.project = project
        self._id = _id
        self._milestone = None
        if _json:
            self._milestone = Milestone(project, _json=_json)

    def getInstanciationFields(self):
        return [self.project]

    def getProject(self):
        return self.project

    def getMilestone(self):
        return self._milestone

    def getModel(self):
        return self._milestone

    def getCacheKey(self):
        return "projects:{}:milestones:{}".format(self.project.id, self._id)

    def getCacheListKey(self):
        return "projects:{}:milestones".format(self.project.id)

    def requestsById(self):
        return requests.get("{}/api/v3/projects/{}/milestones/{}".format(config.HOST, self.project.id, self._id), headers={"PRIVATE-TOKEN": config.PRIVATE_TOKEN}).json()

    def requestsAll(self, page, per_page):
        request = "{}/api/v3/projects/{}/milestones".format(config.HOST, self.project.id)
        request_parameters = "page={}&per_page={}".format(page, per_page)
        return requests.get(request + "?" + request_parameters, headers={"PRIVATE-TOKEN": config.PRIVATE_TOKEN}).json()
