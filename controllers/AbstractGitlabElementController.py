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
