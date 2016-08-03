import redis
import json
from abc import ABCMeta, abstractmethod
from . import config


class CacheFactory(object):
    cache = None

    def cnx():
        if not CacheFactory.cache:
            cache_config = config.CACHE_CONFIG
            if cache_config['type'] == 'redis':
                CacheFactory.cache = RedisCache(**cache_config)
            else:
                CacheFactory.cache = NoCache()
        return CacheFactory.cache


class AbstractCache(metaclass=ABCMeta):

    @abstractmethod
    def get(self, _id):
        pass

    @abstractmethod
    def set(self, _id, value, expire=60):
        pass

    @abstractmethod
    def findAllLike(self, pattern):
        pass

    @abstractmethod
    def findList(self, _id):
        pass

    @abstractmethod
    def decr(self, _id):
        pass

    @abstractmethod
    def incr(self, _id):
        pass

    @abstractmethod
    def pushToList(self, _id, *args):
        pass

    @abstractmethod
    def delete(self, _id):
        pass

    @abstractmethod
    def removeAllValues(self, _id, value):
        pass

    @abstractmethod
    def listLen(self, _id):
        pass


class NoCache(AbstractCache):

    def get(self, _id):
        return None

    def set(self, _id, _dict, expire=60):
        return True

    def findAllLike(self, pattern):
        return []

    def findList(self, _id):
        return []

    def decr(self, _id):
        return 0

    def incr(self, _id):
        return 0

    def pushToList(self, _id, *args):
        return True

    def delete(self, _id):
        return True

    def removeAllValues(self, _id, value):
        return True

    def listLen(self, _id):
        return 0


class RedisCache(AbstractCache):

    def __init__(self, type='redis', host='localhost', port=6379, db=0, password=None):
        self.redis_instance = redis.StrictRedis(host=host, port=port, db=db, password=password)

    def get(self, _id):
        result = self.redis_instance.get(_id)

        if not result:
            return None

        return json.loads(result.decode('utf-8'))

    def set(self, _id, _value=None, _dict={}, expire=0):

        if _value is not None:
            result = self.redis_instance.set(_id, _value)
        elif _dict:
            result = self.redis_instance.set(_id, json.dumps(_dict))
        else:
            raise ValueError("At least one of _value or _dict must be set")

        if expire:
            self.redis_instance.expire(_id, expire)
        return result

    def findAllLike(self, pattern):
        keys = self.redis_instance.keys(pattern)
        return [self.get(key) for key in keys]

    def findList(self, _id):
        return self.redis_instance.lrange(_id, 0, -1)

    def decr(self, _id):
        return self.redis_instance.decr(_id)

    def incr(self, _id):
        return self.redis_instance.incr(_id)

    def listLen(self, _id):
        return self.redis_instance.llen(_id)

    def pushToList(self, _id, *args):
        return self.redis_instance.lpush(_id, *args)

    def delete(self, _id):
        return self.redis_instance.delete(_id)

    def removeAllValues(self, _id, value):
        return self.redis_instance.lrem(_id, 0, value)
