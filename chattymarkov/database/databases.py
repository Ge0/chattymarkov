"""
Redis database for chattimarkov.
"""
import redis

from .base import AbstractDatabase


class RedisDatabase(AbstractDatabase):
    def __init__(self, host="localhost", port=6739, db=0,
                 unix_socket_path=None):

        self._db = int(db)

        if unix_socket_path is not None:
            self._unix_socket_path = unix_socket_path
            self.handle = redis.StrictRedis(unix_socket_path=unix_socket_path,
                                            db=db)
        else:
            self._host = host
            self._port = int(port)
            self.handle = redis.StrictRedis(host=host, port=port, db=db)

    @property
    def host(self):
        return self._host

    @property
    def port(self):
        return self._port

    @property
    def db(self):
        return self._db

    @property
    def unix_socket_path(self):
        return self._unix_socket_path

    def add(self, key, element):
        return self.handle.sadd(key, element.encode()) > 0

    def random(self, key):
        element = self.handle.srandmember(key)
        if element is not None:
            return element.decode()

    def get(self, key):
        element = self.handle.get(key)
        if element is not None:
            return element.decode()

    def set(self, key, value):
        self.handle.set(key, value)
