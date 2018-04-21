"""Database interfaces for chattimarkov."""
import atexit
import json
import os.path
import random

import redis
import six

from .base import AbstractDatabase


class RedisDatabase(AbstractDatabase):
    def __init__(self, host="localhost", port=6739, db=0,
                 unix_socket_path=None, password=None):

        self._db = int(db)
        self._password = password

        if unix_socket_path is not None:
            self._unix_socket_path = unix_socket_path
            self.handle = redis.StrictRedis(unix_socket_path=unix_socket_path,
                                            db=db, password=password)
        else:
            self._host = host
            self._port = int(port)
            self.handle = redis.StrictRedis(host=host, port=port, db=db,
                                            password=password)

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
    def password(self):
        return self._password

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


class MemoryDatabase(AbstractDatabase):
    """Memory database class for chattimarkov.

    This is just a volatile, in-memory database which is built either from a
    pre-existing dictionary or from scratch. Upon object destruction, the
    database is not saved.
    """

    def __init__(self, db=None, *args, **kwargs):
        if db is None:
            self.db = {}
        else:
            self.db = db

    def add(self, key, element):
        if key not in self.db:
            self.db[key] = []
        if type(self.db[key]) is not list:
            return False

        if element not in self.db[key]:
            self.db[key].append(element)

    def random(self, key):
        if key not in self.db:
            return None
        if type(self.db[key]) is not list:
            return None
        return random.choice(self.db[key])

    def get(self, key, default=None):
        return self.db.get(key, default)

    def set(self, key, value):
        self.db[key] = value


class JSONFileDatabase(MemoryDatabase):
    """JSON database class for Chattimarkov.

    JSON files are actually not really suitable for storing a key-value
    database. Loading and storing can actually be slow, mostly if the
    chattimarkov instance is learning a lot.
    """

    def __init__(self, filepath, *args, **kwargs):
        self.filepath = filepath
        if os.path.exists(self.filepath):
            db = json.load(open(filepath))
        else:
            db = None

        if six.PY2:
            MemoryDatabase.__init__(self, db, *args, **kwargs)
        else:
            super().__init__(db, *args, **kwargs)

        atexit.register(self.cleanup)

    def cleanup(self):
        with open(self.filepath, "w") as stream:
            json.dump(self.db, stream)
