from chattymarkov.database import MemoryDatabase


class TestMemoryDatabase:
    def setup_method(self, method):
        self.db = MemoryDatabase()

    def test_add(self):
        """Test the `add` method from the MemoryDatabase class."""
        self.db.add('foo', 'bar')
        assert 'foo' in self.db.db
        assert 'bar' in self.db.db['foo']
