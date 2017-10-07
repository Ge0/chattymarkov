"""Memory database class for chattimarkov.

This is just a volatile, in-memory database which is built either from a
pre-existing dictionary or from scratch. Upon object destruction, the database
is not saved.
"""

import random

from .base import AbstractDatabase


class MemoryDatabase(AbstractDatabase):
    def __init__(self, db=None):
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
