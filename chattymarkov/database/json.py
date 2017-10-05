"""
JSON database class for chattimarkov.

JSON files are actually not really suitable for storing a key-value database.
Loading and storing can actually be slow, mostly if the chattimarkov instance
is learning a lot.
"""

import atexit
import json
import os.path

from .memory import MemoryDatabase


class JSONFileDatabase(MemoryDatabase):
    def __init__(self, filepath, *args, **kwargs):
        self.filepath = filepath
        if os.path.exists(self.filepath):
            db = json.load(open(filepath))
        else:
            db = None
        super().__init__(self, db, *args, **kwargs)
        atexit.register(self.cleanup)

    def cleanup(self):
        with open(self.filepath, "w") as stream:
            json.dump(self.db, stream)
