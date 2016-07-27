import requests
import config
from models.Project import Project
from cache.factories.CacheFactory import CacheFactory
from .AbstractGitlabElementController import AbstractGitlabElementController


class ProjectController(AbstractGitlabElementController):

    def __init__(self, _id=None, _json={}):
        if _id:
            self._project = ProjectController.find(_id)
        elif _json:
            self._project = Project(_json=_json)
        else:
            raise ValueError()

    def getProject(self):
        return self._project

    @classmethod
    def find(cls, _id):
        _json = CacheFactory.cnx().get("projects:{}".format(_id))
        if not _json:
            return cls.__findFromHTTPQuery(_id)
        return cls(_json=_json).getProject()

    @classmethod
    def findAll(cls):
        _jsons = []
        _names = CacheFactory.cnx().findList("projects")
        if not _names:
            return cls.__findAllFromHTTPQuery()
        else:
            for _name in _names:
                _json = CacheFactory.cnx().get(_name)
                if not _json:
                    CacheFactory.cnx().delete("projects")
                    return cls.__findAllFromHTTPQuery()
                _jsons.append(_json)
        return [ProjectController(_json=_json).getProject() for _json in _jsons]

    @classmethod
    def __findFromHTTPQuery(cls, _id):
        _json = requests.get("{}/api/v3/projects/{}".format(config.HOST, _id),
                             headers={"PRIVATE-TOKEN": config.PRIVATE_TOKEN}).json()
        if _json:
            CacheFactory.cnx().set("projects:{}".format(_json['id']), _json)
            CacheFactory.cnx().pushToList("projects", "projects:{}".format(_json['id']))
        return Project(_json=_json)

    @classmethod
    def __findAllFromHTTPQuery(cls):
        _jsons = requests.get("{}/api/v3/projects".format(config.HOST),
                              headers={"PRIVATE-TOKEN": config.PRIVATE_TOKEN}).json()
        for _json in _jsons:
            CacheFactory.cnx().set("projects:{}".format(_json['id']), _json)
            CacheFactory.cnx().pushToList("projects", "projects:{}".format(_json['id']))
        return [ProjectController(_json=_json).getProject() for _json in _jsons]
