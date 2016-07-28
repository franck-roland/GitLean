from abc import ABCMeta, abstractmethod
from cache.factories.CacheFactory import CacheFactory


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

    @classmethod
    def getCacheKey(cls, *args):
        raise NotImplementedError

    @classmethod
    def getCacheListKey(cls, *args):
        raise NotImplementedError

    @classmethod
    def requestsById(cls, *args):
        raise NotImplementedError

    @classmethod
    def requestsAll(cls, *args, **kwargs):
        raise NotImplementedError

    @classmethod
    def find(cls, *args):
        _json = CacheFactory.cnx().get(cls.getCacheKey(*args))
        if not _json:
            _json = cls.__findFromHTTPQuery(*args)
        return cls(*args, _json=_json).getModel()

    @classmethod
    def findAll(cls, *args, **kwargs):
        _jsons = []
        cache_keys = CacheFactory.cnx().findList(cls.getCacheListKey(*args))

        if not cache_keys:
            _jsons = cls.__findAllFromHTTPQuery(*args, **kwargs)

        else:
            for cache_key in cache_keys:

                _json = CacheFactory.cnx().get(cache_key)

                if not _json:
                    CacheFactory.cnx().removeAllValues(cls.getCacheListKey(*args), cache_key)
                    cache_key = cache_key.decode('utf-8')
                    params = list(args)
                    params.append(cls.getIdFromCacheKey(cache_key))
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
    def __findAllFromHTTPQuery(cls, *args, **kwargs):
        page = 1
        per_page = 10
        _jsons = []
        while True:
            result = cls.requestsAll(*args, page, per_page, **kwargs)

            if not result:
                break

            for _json in result:
                params = list(args)
                params.append(cls.getIdFieldFromJson(_json))
                CacheFactory.cnx().set(cls.getCacheKey(*params), _json)
                CacheFactory.cnx().pushToList(cls.getCacheListKey(*params), cls.getCacheKey(*params))
            _jsons += result
            page += 1

        return _jsons
