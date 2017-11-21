import unittest

from chattymarkov import database


class TestDatabase(unittest.TestCase):
    def test_build_database_connection(self):
        """Test `build_database_connection` of `chattymarkov.database`."""
        redis_socket_connection = database.build_database_connection(
            "redis:///path/to/redis/unix_socket.sock;db=1")
        self.assertEquals(redis_socket_connection.db, 1)
        self.assertEquals(redis_socket_connection.unix_socket_path,
                          "/path/to/redis/unix_socket.sock")

        redis_socket_connection = database.build_database_connection(
            "redis://localhost:12345;db=3")
        self.assertEquals(redis_socket_connection.db, 3)
        self.assertEquals(redis_socket_connection.host, "localhost")
        self.assertEquals(redis_socket_connection.port, 12345)
