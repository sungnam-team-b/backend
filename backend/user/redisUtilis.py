import redis
import json
import time

from django.core.cache import cache

rds = redis.Redis(host='mysqldb', port=6379)


class Red():
    def set(cache_key, time):
        rds.set(cache_key, time)
        return True

    def get(cache_key):
        print(cache_key)
        cache_data = rds.get(cache_key)
        if not cache_data :
            return None
        cache_data = json.loads(cache_data)

        return cache_data
