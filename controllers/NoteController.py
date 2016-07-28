import requests
import config
from .AbstractGitlabElementController import AbstractGitlabElementController
from factories.NoteFactory import NoteFactory


class NoteController(AbstractGitlabElementController):

    def __init__(self, issue, _id=None, _json={}):

        self._issue = issue

        if _json:
            self._note = NoteFactory.factory(issue, _json=_json)
        elif _id:
            self._note = NoteController.find(issue, _id)
        else:
            raise ValueError()

    def getIssue(self):
        return self._issue

    def getNote(self):
        return self._note

    def getModel(self):
        return self._note

    @classmethod
    def getCacheKey(cls, issue, _id):
        return "projects:{}:issues:{}:note:{}".format(issue.project.id, issue.id, _id)

    @classmethod
    def getCacheListKey(cls, issue, *args):
        return "projects:{}:issues:{}:notes".format(issue.project.id, issue.id)

    @classmethod
    def requestsById(cls, issue, _id):
        return requests.get("{}/api/v3/projects/{}/issues/{}/notes/{}".format(config.HOST, issue.project.id, issue.id, _id), headers={"PRIVATE-TOKEN": config.PRIVATE_TOKEN}).json()

    @classmethod
    def requestsAll(cls, issue, page, per_page):
        return requests.get("{}/api/v3/projects/{}/issues/{}/notes?page={}&per_page={}".format(config.HOST, issue.project.id, issue.id, page, per_page), headers={"PRIVATE-TOKEN": config.PRIVATE_TOKEN}).json()
