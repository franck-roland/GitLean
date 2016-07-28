from abc import ABCMeta, abstractmethod
from cache.factories.CacheFactory import CacheFactory


class AbstractGitlabElementController(metaclass=ABCMeta):

    @abstractmethod
    def getModel(self):
        pass

    @classmethod
    def getCacheKey(cls, project, _id):
        raise NotImplementedError

    @classmethod
    def getCacheListKey(cls, project):
        raise NotImplementedError

    @classmethod
    def requestsById(cls, project, _id):
        raise NotImplementedError

    @classmethod
    def requestsAll(cls, project, page, per_page):
        raise NotImplementedError

    @classmethod
    def find(cls, *args):
        _json = CacheFactory.cnx().get(cls.getCacheKey(*args))
        if not _json:
            _json = cls.__findFromHTTPQuery(*args)
        return cls(*args, _json=_json).getModel()

    @classmethod
    def findAll(cls, *args):
        _jsons = []
        _names = CacheFactory.cnx().findList(cls.getCacheListKey(*args))
        if not _names:
            _jsons = cls.__findAllFromHTTPQuery(*args)
        else:
            for _name in _names:
                _json = CacheFactory.cnx().get(_name)
                if not _json:
                    CacheFactory.cnx().removeAllValues(cls.getCacheListKey(*args), _name)
                    _name = _name.decode('utf-8')
                    params = list(args)
                    params.append(_name[_name.rfind(":") + 1:])
                    _json = cls.__findFromHTTPQuery(*params)
                if _json:
                    _jsons.append(_json)
        return [cls(*args, _json=_json).getModel() for _json in _jsons]

    @classmethod
    def __findFromHTTPQuery(cls, *args):
        _json = cls.requestsById(*args)
        if _json:
            CacheFactory.cnx().set(cls.getCacheKey(*args), _json)
            CacheFactory.cnx().pushToList(cls.getCacheListKey(*args), cls.getCacheKey(*args))
        return _json

    @classmethod
    def __findAllFromHTTPQuery(cls, *args):
        page = 1
        per_page = 10
        _jsons = []
        while True:
            result = cls.requestsAll(*args, page, per_page)

            if not result:
                break

            for _json in result:
                params = list(args)
                params.append(_json['id'])
                CacheFactory.cnx().set(cls.getCacheKey(*params), _json)
                CacheFactory.cnx().pushToList(cls.getCacheListKey(*params), cls.getCacheKey(*params))
            _jsons += result
            page += 1

        return _jsons
