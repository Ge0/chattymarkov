"""Database interfaces for chattimarkov."""
import atexit
import json
import os.path
import random

import aioredis
import redis

from .base import AbstractDatabase


class RedisDatabasePropertyMixin:
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


class RedisDatabaseAsync(RedisDatabasePropertyMixin):

    def __init__(self, host="localhost", port=6739, db=0,
                 unix_socket_path=None, password=None):
        self._conn = None
        self._db = int(db)
        self._password = password
        self._unix_socket_path = None

        if unix_socket_path is not None:
            self._unix_socket_path = unix_socket_path
        else:
            self._host = host
            self._port = int(port)

    async def connect(self):
        """Create the connection pool."""
        if self._unix_socket_path is not None:
            self._connection_pool = await aioredis.create_pool(
                self._unix_socket_path, minsize=5, maxsize=10,
                db=self._db, password=self._password)
        else:
            self._connection_pool = await aioredis.create_pool(
                (self._host, self._port),
                minsize=5, maxsize=10,
                db=self._db, password=self._password)

    async def add(self, key, element):
        async with self._connection_pool as conn:
            return await conn.execute('SADD', key, element.encode()) > 0

    async def random(self, key):
        async with self._connection_pool as conn:
            element = await conn.execute('SRANDMEMBER', key)
            if element is not None:
                return element.decode()

    async def get(self, key):
        async with self._connection_pool as conn:
            element = await conn.execute('GET', key)
            if element is not None:
                return element.decode()

    async def set(self, key, value):
        async with self._connection_pool as conn:
            await conn.execute('SET', key, value)


class RedisDatabase(AbstractDatabase, RedisDatabasePropertyMixin):
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


class MemoryDatabaseAsync:
    """Asynchronous memory database class for chattymarkov.

    This is just a volatile, in-memory database which is built either from a
    pre-existing dictionary or from scratch. Upon object destruction, the
    database is not saved.

    """
    def __init__(self, db=None, *args, **kwargs):
        if db is None:
            self.db = {}
        else:
            self.db = db

    async def add(self, key, element):
        if key not in self.db:
            self.db[key] = []
        if type(self.db[key]) is not list:
            return False

        if element not in self.db[key]:
            self.db[key].append(element)

    async def random(self, key):
        if key not in self.db:
            return None
        elif type(self.db[key]) is not list:
            return None
        else:
            return random.choice(self.db[key])

    def get(self, key, default=None):
        return self.db.get(key, default)

    def set(self, key, value):
        self.db[key] = value


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

        super().__init__(db, *args, **kwargs)

        atexit.register(self.cleanup)

    def cleanup(self):
        with open(self.filepath, "w") as stream:
            json.dump(self.db, stream)
