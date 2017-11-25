import json
import os
import tempfile
import unittest

import six

from chattymarkov import ChattyMarkov
from chattymarkov.database import (JSONFileDatabase, MemoryDatabase,
                                   RedisDatabase)


class TestChattyMarkov(unittest.TestCase):
    def setUp(self):
        empty_memory = []
        self.json_file = tempfile.NamedTemporaryFile(delete=False)
        if six.PY3:
            self.json_file.write(json.dumps(empty_memory).encode())
        else:
            self.json_file.write(json.dumps(empty_memory))
        self.json_file.close()

    def tearDown(self):
        os.unlink(self.json_file.name)

    def test_init(self):
        """Test the __init__ method of ChattyMarkov."""
        c = ChattyMarkov("memory://")
        self.assertTrue(isinstance(c.db, MemoryDatabase))

        c = ChattyMarkov("json://{}".format(self.json_file.name))
        self.assertTrue(isinstance(c.db, JSONFileDatabase))

        c = ChattyMarkov("redis:///path/to/socket.sock")
        self.assertTrue(isinstance(c.db, RedisDatabase))
        self.assertEquals(c.db.unix_socket_path, "/path/to/socket.sock")
        self.assertEquals(c.db.db, 0)

        c = ChattyMarkov("redis://1.2.3.4:8765;db=3;password=foobar")
        self.assertEquals(c.db.host, "1.2.3.4")
        self.assertEquals(c.db.port, 8765)
        self.assertEquals(c.db.password, "foobar")
        self.assertEquals(c.db.db, 3)
