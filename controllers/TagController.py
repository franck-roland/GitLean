import requests
import config
from .AbstractGitlabElementController import AbstractGitlabElementController
from models.Tag import Tag


class TagController(AbstractGitlabElementController):

    def __init__(self, project, _id=None, _json={}):

        self.project = project
        self._id = _id
        self._tag = None
        if _json:
            self._tag = Tag(project, _json=_json)

    def getProject(self):
        return self.project

    def getTag(self):
        return self._tag

    def getModel(self):
        return self._tag

    def getInstanciationFields(self):
        return [self.project]

    @classmethod
    def getIdFieldFromJson(cls, _json):
        return _json['name']

    @classmethod
    def getIdFromCacheKey(cls, cache_key):
        return cache_key[cache_key.rfind(":") + 1:].replace('___;___', ':')

    def getCacheKey(self):
        return "projects:{}:tags:{}".format(self.project.id, self._id.replace(':', '___;___'))

    def getCacheListKey(self):
        return "projects:{}:tags".format(self.project.id)

    def requestsById(self):
        return requests.get("{}/api/v3/projects/{}/repository/tags/{}".format(config.HOST, self.project.id, self._id), headers={"PRIVATE-TOKEN": config.PRIVATE_TOKEN}).json()

    def requestsAll(self, page, per_page):
        # No pagination on /tags
        if page != 1:
            return []
        request = "{}/api/v3/projects/{}/repository/tags".format(config.HOST, self.project.id)
        request_parameters = "page={}&per_page={}".format(page, per_page)
        return requests.get(request + "?" + request_parameters, headers={"PRIVATE-TOKEN": config.PRIVATE_TOKEN}).json()
