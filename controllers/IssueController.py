import requests
import config
from cache.factories.CacheFactory import CacheFactory
from .AbstractGitlabElementController import AbstractGitlabElementController
from factories.IssueFactory import IssueFactory


class IssueController(AbstractGitlabElementController):

    def __init__(self, project, _id=None, _json={}):
        self._project = project
        if _id:
            self._issue = IssueController.find(_id)
        elif _json:
            self._issue = IssueFactory.factory(project, _json=_json)
        else:
            raise ValueError()

    def getProject(self):
        return self._project

    def getIssue(self):
        return self._issue

    @classmethod
    def find(cls, project, _id):
        _json = CacheFactory.cnx().get("projects:{}:issues:{}".format(project.id, _id))
        if not _json:
            return cls.__findFromHTTPQuery(_id, project)
        return cls(_json=_json).getIssue()

    @classmethod
    def findAll(cls, project):
        _jsons = []
        _names = CacheFactory.cnx().findList("projects:{}:issues".format(project.id))
        if not _names:
            return cls.__findAllFromHTTPQuery(project)
        else:
            for _name in _names:
                _json = CacheFactory.cnx().get(_name)
                if not _json:
                    CacheFactory.cnx().delete("projects:{}:issues".format(project.id))
                    return cls.__findAllFromHTTPQuery(project)
                _jsons.append(_json)
        return [IssueController(project, _json=_json).getIssue() for _json in _jsons]

    @classmethod
    def __findFromHTTPQuery(cls, project, _id):
        _json = requests.get("{}/api/v3/projects/{}/issues/{}".format(config.HOST, project.id, _id),
                             headers={"PRIVATE-TOKEN": config.PRIVATE_TOKEN}).json()
        if _json:
            CacheFactory.cnx().set("projects:{}:issues:{}".format(project.id, _json['id']), _json)
            CacheFactory.cnx().pushToList("projects:{}:issues".format(project.id), "projects:{}:issues:{}".format(project.id, _json['id']))
        return IssueFactory.factory(project, _json=_json)

    @classmethod
    def __findAllFromHTTPQuery(cls, project):
        page = 1
        per_page = 10
        _jsons = []
        while True:
            result = requests.get("{}/api/v3/projects/{}/issues?page={}&per_page={}".format(config.HOST, project.id, page, per_page),
                                  headers={"PRIVATE-TOKEN": config.PRIVATE_TOKEN}).json()
            if not result:
                break
            _jsons += result
            page += 1

        for _json in _jsons:
            CacheFactory.cnx().set("projects:{}:issues:{}".format(project.id, _json['id']), _json)
            CacheFactory.cnx().pushToList("projects:{}:issues".format(project.id), "projects:{}:issues:{}".format(project.id, _json['id']))
        return [IssueController(project, _json=_json).getIssue() for _json in _jsons]
