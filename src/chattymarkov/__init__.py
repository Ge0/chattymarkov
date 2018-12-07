"""ChattyMarkov module.

This module provides a base class to instanciate a `ChattyMarkov` class
which is responsible for learning from sentences as much as generating ones.

In order to succesfully memorise sentences, A `ChattyMarkov` instance will
rely on a database which has to inherit from the abstract interface described
`chattymarkov.database.AbstractDatabase`.

"""
from . import database


class ChattyMarkovAsync:
    """ChattyMarkov, the asyncio way.

    See also:
        `ChattyMarkov`

    """

    def __init__(self, connect_string, prefix="chattymarkov", separator="\x01",
                 stop_word="\x02"):
        """Instanciate the ChattyMarkov async class."""
        self.db = database.build_database_connection_async(connect_string)
        self.separator = separator
        self.stop_word = stop_word
        self.prefix = prefix

    async def learn(self, msg: str) -> None:
        """Learn from *msg*."""
        if not msg:
            return
        for words in await self._split_message(msg):
            key = self.separator.join(words[:-1])
            await self.db.add(self._make_key(key), words[-1])

    async def _split_message(self, msg):
        """Split *msg* to better learn from it."""
        words = msg.split(' ')
        lastword = ""
        previous = ""
        msg += " " + self.stop_word

        for word in words:
            key = self._make_key(self.separator.join([previous, lastword]))
            await self.db.add(key, word)
            yield [previous, lastword, word]
            previous = lastword
            lastword = word

    async def generate(self):
        """Generate a message by browsing the database randomly as we
        browse a markov graph, to construct a random sentence from what
        the ChattyMarkov instance has learned so far.

        Returns:
            A string which consists of a random generated sentence.

        """
        lastword = ""
        previous = ""
        out = []

        while True:
            key = self._make_key(self.separator.join([previous, lastword]))
            word = await self.db.random(key)
            if not word or word == self.stop_word:
                break
            out.append(word)
            previous = lastword
            lastword = word
        return ' '.join(out)

    def _make_key(self, key):
        """Private method. Generate a key for internal database storage,
        given the *key* parameter.

        Args:
            key: the string to generate the database key from.

        Returns:
            A key used for internal use.

        """
        return '-'.join((self.prefix, key))


class ChattyMarkov:
    """ChattyMarkov class.

    Define an interface between a user and a database in order to learn
    sentences and generate random sentences through a markov-chain-based
    algorithm.

    """

    def __init__(self, connect_string, prefix="chattymarkov", separator="\x01",
                 stop_word="\x02"):
        """Instanciate the ChattyMarkov class.

        Args:
            database: a database instance which inherits from
                AbstractDatabase.
            prefix: a prefix useful in database storage.
            separator: a separator pattern for database storage.
            stop_word: a stop-word pattern for database storage.

        """
        self.db = database.build_database_connection(connect_string)
        self.separator = separator
        self.stop_word = stop_word
        self.prefix = prefix

    def _make_key(self, key):
        """Private method. Generate a key for internal database storage,
        given the `key` parameter.

        Args:
            key: the string to generate the database key from.

        Returns:
            A key used for internal use.

        """
        return '-'.join((self.prefix, key))

    def learn(self, msg):
        """Learn from a message. This function is called in order to
        memorise a sentence provided through the parameter `msg`.

        Args:
            msg: the sentence to learn from.

        """
        if msg == '':
            return
        for words in self._split_message(msg):
            key = self.separator.join(words[:-1])
            self.db.add(self._make_key(key), words[-1])

    def generate(self):
        """Generate a message by browsing the database randomly as we
        browse a markov graph, to construct a random sentence from what
        the ChattyMarkov instance has learned so far.

        Returns:
            A string which consists of a random generated sentence.

        """
        lastword = ""
        previous = ""
        out = []

        while True:
            key = self._make_key(self.separator.join([previous, lastword]))
            word = self.db.random(key)
            if not word or word == self.stop_word:
                break
            out.append(word)
            previous = lastword
            lastword = word
        return ' '.join(out)

    def _split_message(self, msg):
        """Split message to better learn from it."""
        words = msg.split(' ')
        lastword = ""
        previous = ""
        msg += " " + self.stop_word

        for word in words:
            key = self._make_key(self.separator.join([previous, lastword]))
            self.db.add(key, word)
            yield [previous, lastword, word]
            previous = lastword
            lastword = word
