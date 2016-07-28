import requests
import config
from cache.factories.CacheFactory import CacheFactory
from .AbstractGitlabElementController import AbstractGitlabElementController
from factories.NoteFactory import NoteFactory


class NoteController(AbstractGitlabElementController):

    def __init__(self, project, issue, _id=None, _json={}):

        self._project = project
        self._issue = issue

        if _json:
            self._note = NoteFactory.factory(project, issue, _json=_json)
        elif _id:
            self._note = NoteController.find(_id)
        else:
            raise ValueError()

    def getProject(self):
        return self._project

    def getIssue(self):
        return self._issue

    def getNote(self):
        return self._note

    def getModel(self):
        return self._note

    @classmethod
    def getCacheKey(cls, project, issue, _id):
        return "projects:{}:issues:{}:note:{}".format(project.id, issue.id, _id)

    @classmethod
    def getCacheListKey(cls, project, issue, *args):
        return "projects:{}:issues:{}:notes".format(project.id, issue.id)

    @classmethod
    def requestsById(cls, project, issue, _id):
        return requests.get("{}/api/v3/projects/{}/issues/{}/notes/{}".format(config.HOST, project.id, issue.id, _id), headers={"PRIVATE-TOKEN": config.PRIVATE_TOKEN}).json()

    @classmethod
    def requestsAll(cls, project, issue, page, per_page):
        return requests.get("{}/api/v3/projects/{}/issues/{}/notes?page={}&per_page={}".format(config.HOST, project.id, issue.id, page, per_page), headers={"PRIVATE-TOKEN": config.PRIVATE_TOKEN}).json()
