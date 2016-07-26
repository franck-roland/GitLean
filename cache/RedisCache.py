import redis
import json
from .AbstractCache import AbstractCache


class RedisCache(AbstractCache):

    def __init__(self, type='redis', host='localhost', port=6379, db=0, password=None):
        self.redis_instance = redis.StrictRedis(host=host, port=port, db=db, password=password)

    def get(self, _id):
        result = self.redis_instance.get(_id)

        if not result:
            return None

        return json.loads(result.decode('utf-8'))

    def set(self, _id, _dict, expire=120):
        result = self.redis_instance.set(_id, json.dumps(_dict))
        self.redis_instance.expire(_id, expire)
        return result

    def findAllLike(self, pattern):
        keys = self.redis_instance.keys(pattern)
        return [self.get(key) for key in keys]

    def findList(self, _id):
        return self.redis_instance.lrange(_id, 0, -1)

    def pushToList(self, _id, *args):
        return self.redis_instance.lpush(_id, *args)

    def delete(self, _id):
        return self.redis_instance.delete(_id)
