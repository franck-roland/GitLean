import requests
import config
from cache.factories.CacheFactory import CacheFactory
from .AbstractGitlabElementController import AbstractGitlabElementController
from factories.NoteFactory import NoteFactory


class NoteController(AbstractGitlabElementController):

    def __init__(self, project, issue, _id=None, _json={}):
        self._project = project
        self._issue = issue
        if _id:
            self._note = NoteController.find(_id)
        elif _json:
            self._note = NoteFactory.factory(project, issue, _json=_json)
        else:
            raise ValueError()

    def getProject(self):
        return self._project

    def getIssue(self):
        return self._issue

    def getNote(self):
        return self._note

    @classmethod
    def find(cls, project, issue, _id):
        _json = CacheFactory.cnx().get("projects:{}:issues:{}:notes:{}".format(project.id, issue.id, _id))
        if not _json:
            return cls.__findFromHTTPQuery(_id, project, issue)
        return cls(_json=_json).getNote()

    @classmethod
    def findAll(cls, project, issue):
        _jsons = []
        _names = CacheFactory.cnx().findList("projects:{}:issues:{}:notes".format(project.id, issue.id))
        if not _names:
            return cls.__findAllFromHTTPQuery(project, issue)
        else:
            for _name in _names:
                _json = CacheFactory.cnx().get(_name)
                if not _json:
                    CacheFactory.cnx().delete("projects:{}:issues:{}:notes".format(project.id, issue.id))
                    return cls.__findAllFromHTTPQuery(project, issue)
                _jsons.append(_json)
        return [NoteController(project, issue, _json=_json).getNote() for _json in _jsons]

    @classmethod
    def __findFromHTTPQuery(cls, project, issue, _id):
        _json = requests.get("{}/api/v3/projects/{}/issues/{}/notes/{}".format(config.HOST, project.id, issue.id, _id),
                             headers={"PRIVATE-TOKEN": config.PRIVATE_TOKEN}).json()
        if _json:
            CacheFactory.cnx().set("projects:{}:issues:{}:notes:{}".format(project.id, issue.id, _json['id']), _json)
            CacheFactory.cnx().pushToList("projects:{}:issues:{}:notes".format(project.id, issue.id),
                                          "projects:{}:issues:{}:notes:{}".format(project.id, issue.id, _json['id']))
        return NoteFactory.factory(project, issue, _json=_json)

    @classmethod
    def __findAllFromHTTPQuery(cls, project, issue):
        page = 1
        per_page = 10
        _jsons = []
        while True:
            result = requests.get("{}/api/v3/projects/{}/issues/{}/notes?page={}&per_page={}".format(config.HOST, project.id, issue.id, page, per_page),
                                  headers={"PRIVATE-TOKEN": config.PRIVATE_TOKEN}).json()
            if not result:
                break
            _jsons += result
            page += 1

        for _json in _jsons:
            CacheFactory.cnx().set("projects:{}:issues:{}:notes:{}".format(project.id, issue.id, _json['id']), _json)
            CacheFactory.cnx().pushToList("projects:{}:issues:{}:notes".format(project.id, issue.id),
                                          "projects:{}:issues:{}:notes:{}".format(project.id, issue.id, _json['id']))
        return [NoteController(project, issue, _json=_json).getNote() for _json in _jsons]
