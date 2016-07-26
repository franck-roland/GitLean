import config
from cache.RedisCache import RedisCache
from cache.NoCache import NoCache


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
