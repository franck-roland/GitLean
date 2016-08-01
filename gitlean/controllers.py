import requests
from abc import ABCMeta, abstractmethod
from . import config, models
from .cache import CacheFactory
from .factories import IssueFactory, NoteFactory


class AbstractGitlabElementController(metaclass=ABCMeta):

    @classmethod
    def getIdFieldFromJson(cls, _json):
        return _json['id']

    @classmethod
    def getIdFromCacheKey(cls, cache_key):
        return cache_key[cache_key.rfind(":") + 1:]

    @abstractmethod
    def getModel(self):
        pass

    @abstractmethod
    def getInstanciationFields(self):
        pass

    @classmethod
    def getFieldNameFromParameterName(cls, parameter_name):
        return parameter_name

    def getCacheKey(self):
        raise NotImplementedError

    def getCacheListKey(self):
        raise NotImplementedError

    def requestsById(self):
        raise NotImplementedError

    def requestsAll(self, page, per_page, **kwargs):
        raise NotImplementedError

    @classmethod
    def filter(cls, results, **kwargs):
        return results

    def find(self):
        _json = CacheFactory.cnx().get(self.getCacheKey())
        if not _json:
            _json = self.__findFromHTTPQuery()
        return self.getModel()

    def findAll(self, **kwargs):
        _jsons = []
        cache_keys = CacheFactory.cnx().findList(self.getCacheListKey())

        if not cache_keys:
            _jsons = self.__findAllFromHTTPQuery(**kwargs)

        else:
            for cache_key in cache_keys:

                _json = CacheFactory.cnx().get(cache_key)

                if not _json:
                    CacheFactory.cnx().removeAllValues(self.getCacheListKey(), cache_key)
                    cache_key = cache_key.decode('utf-8')
                    self._id = self.getIdFromCacheKey(cache_key)
                    _json = self.__findFromHTTPQuery()

                if _json:
                    _jsons.append(_json)

        return [self.__class__(*list(self.getInstanciationFields()), _json=_json).getModel() for _json in _jsons]

    def __findFromHTTPQuery(self):
        _json = self.requestsById()
        if _json:
            CacheFactory.cnx().set(self.getCacheKey(), _json)
            CacheFactory.cnx().pushToList(self.getCacheListKey(), self.getCacheKey())
        return _json

    def __findAllFromHTTPQuery(self, **kwargs):
        page = 1
        per_page = 10
        _jsons = []
        while True:
            result = self.requestsAll(page, per_page, **kwargs)

            if not result:
                break

            for _json in result:
                self._id = self.getIdFieldFromJson(_json)
                CacheFactory.cnx().set(self.getCacheKey(), _json)
                CacheFactory.cnx().pushToList(self.getCacheListKey(), self.getCacheKey())
            _jsons += result
            page += 1

        return _jsons


class CommitController(AbstractGitlabElementController):

    def __init__(self, project, _id=None, _json={}):

        self.project = project
        self._id = _id
        self.commit = None
        if _json:
            self.commit = models.Commit(project, _json=_json)

    def getInstanciationFields(self):
        return [self.project]

    def getProject(self):
        return self.project

    def getCommit(self):
        return self.commit

    def getModel(self):
        return self.commit

    def getCacheKey(self):
        return "projects:{}:commits:{}".format(self.project.id, self._id)

    def getCacheListKey(self):
        return "projects:{}:commits".format(self.project.id)

    def requestsById(self):
        return requests.get("{}/api/v3/projects/{}/repository/commits/{}".format(config.HOST, self.project.id, self._id), headers={"PRIVATE-TOKEN": config.PRIVATE_TOKEN}).json()

    def requestsAll(self, page, per_page):
        # No pagination on /commits
        if page != 1:
            return []
        request = "{}/api/v3/projects/{}/repository/commits".format(config.HOST, self.project.id)
        request_parameters = "page={}&per_page={}".format(page, per_page)
        print(request + "?" + request_parameters)
        return requests.get(request + "?" + request_parameters, headers={"PRIVATE-TOKEN": config.PRIVATE_TOKEN}).json()


class IssueController(AbstractGitlabElementController):

    def __init__(self, project, _id=None, _json={}):

        self.project = project
        self._id = _id
        self.issue = None
        if _json:
            self.issue = IssueFactory.factory(project, _json=_json)

    def getInstanciationFields(self):
        return [self.project]

    def getProject(self):
        return self.project

    def getIssue(self):
        return self.issue

    def getModel(self):
        return self.issue

    def getCacheKey(self):
        return "projects:{}:issues:{}".format(self.project.id, self._id)

    def getCacheListKey(self):
        return "projects:{}:issues".format(self.project.id)

    def requestsById(self):
        return requests.get("{}/api/v3/projects/{}/issues/{}".format(config.HOST, self.project.id, self._id), headers={"PRIVATE-TOKEN": config.PRIVATE_TOKEN}).json()

    def requestsAll(self, page, per_page, milestone=None):
        request = "{}/api/v3/projects/{}/issues".format(config.HOST, self.project.id)
        request_parameters = "page={}&per_page={}".format(page, per_page)
        if milestone:
            request_parameters += "&milestone=" + milestone.title
        return requests.get(request + "?" + request_parameters, headers={"PRIVATE-TOKEN": config.PRIVATE_TOKEN}).json()


class MilestoneController(AbstractGitlabElementController):

    def __init__(self, project, _id=None, _json={}):

        self.project = project
        self._id = _id
        self._milestone = None
        if _json:
            self._milestone = models.Milestone(project, _json=_json)

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


class NoteController(AbstractGitlabElementController):

    def __init__(self, issue, _id=None, _json={}):

        self.issue = issue
        self._id = _id
        self._note = None
        if _json:
            self._note = NoteFactory.factory(issue, _json=_json)

    def getInstanciationFields(self):
        return [self.issue]

    def getIssue(self):
        return self.issue

    def getNote(self):
        return self._note

    def getModel(self):
        return self._note

    def getCacheKey(self):
        return "projects:{}:issues:{}:notes:{}".format(self.issue.project.id, self.issue.id, self._id)

    def getCacheListKey(self):
        return "projects:{}:issues:{}:notes".format(self.issue.project.id, self.issue.id)

    def requestsById(self):
        return requests.get("{}/api/v3/projects/{}/issues/{}/notes/{}".format(config.HOST, self.issue.project.id, self.issue.id, self._id), headers={"PRIVATE-TOKEN": config.PRIVATE_TOKEN}).json()

    def requestsAll(self, page, per_page):
        return requests.get("{}/api/v3/projects/{}/issues/{}/notes?page={}&per_page={}".format(config.HOST, self.issue.project.id, self.issue.id, page, per_page), headers={"PRIVATE-TOKEN": config.PRIVATE_TOKEN}).json()


class ProjectController(AbstractGitlabElementController):

    def __init__(self, _id=None, _json={}):

        self._id = _id
        self.project = None
        if _json:
            self.project = models.Project(_json=_json)

    def getInstanciationFields(self):
        return []

    def getProject(self):
        return self.project

    def getModel(self):
        return self.project

    def getCacheKey(self):
        if not self._id:
            raise ValueError
        return "projects:{}".format(self._id)

    def getCacheListKey(self):
        return "projects"

    def requestsById(self):
        if not self._id:
            raise ValueError
        return requests.get("{}/api/v3/projects/{}".format(config.HOST, self._id), headers={"PRIVATE-TOKEN": config.PRIVATE_TOKEN}).json()

    def requestsAll(self, page, per_page):
        return requests.get("{}/api/v3/projects?page={}&per_page={}".format(config.HOST, page, per_page), headers={"PRIVATE-TOKEN": config.PRIVATE_TOKEN}).json()


class TagController(AbstractGitlabElementController):

    def __init__(self, project, _id=None, _json={}):

        self.project = project
        self._id = _id
        self._tag = None
        if _json:
            self._tag = models.Tag(project, _json=_json)

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
