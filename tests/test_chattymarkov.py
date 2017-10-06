from chattymarkov import ChattyMarkov
from chattymarkov.database import MemoryDatabase


class TestChattyMarkov:
    def test_init_memory(self):
        assert ChattyMarkov(MemoryDatabase()) is not None
