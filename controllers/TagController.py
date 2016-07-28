import requests
import config
from .AbstractGitlabElementController import AbstractGitlabElementController
from models.Tag import Tag


class TagController(AbstractGitlabElementController):

    def __init__(self, project, _id=None, _json={}):

        self._project = project

        if _json:
            self._tag = Tag(project, _json=_json)
        elif _id:
            self._tag = TagController.find(project, _id)
        else:
            raise ValueError()

    def getProject(self):
        return self._project

    def getTag(self):
        return self._tag

    def getModel(self):
        return self._tag

    @classmethod
    def getIdFieldFromJson(cls, _json):
        return _json['name']

    @classmethod
    def getCacheKey(cls, project, _name):
        return "projects:{}:tags:{}".format(project.id, _name.replace(':', '___;___'))

    @classmethod
    def getIdFromCacheKey(cls, cache_key):
        return cache_key[cache_key.rfind(":") + 1:].replace('___;___', ':')

    @classmethod
    def getCacheListKey(cls, project, *args):
        return "projects:{}:tags".format(project.id)

    @classmethod
    def requestsById(cls, project, _id):
        return requests.get("{}/api/v3/projects/{}/repository/tags/{}".format(config.HOST, project.id, _id), headers={"PRIVATE-TOKEN": config.PRIVATE_TOKEN}).json()

    @classmethod
    def requestsAll(cls, project, page, per_page):
        # No pagination on /tags
        if page != 1:
            return []
        request = "{}/api/v3/projects/{}/repository/tags".format(config.HOST, project.id)
        request_parameters = "page={}&per_page={}".format(page, per_page)
        return requests.get(request + "?" + request_parameters, headers={"PRIVATE-TOKEN": config.PRIVATE_TOKEN}).json()
