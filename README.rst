Chattymarkov
============

|codecov| |travis build| |pypi version|

Description
-----------

Chattymarkov is a python module that lets you generate random sentences
through a markov chain algorithm.

It is useful mostly for bots which are aimed at learning from user’s
chat and generate totally w.t.f. answers.

The library can support multiple databases, especially redis which is
quite suitable to store relevant information for markov chains.

Installation
------------

.. code:: bash

    pip install chattymarkov

Examples
--------

From ``examples/memory.py``

.. code:: python

    #!/usr/bin/env python3
    from chattymarkov import ChattyMarkov

    markov = ChattyMarkov("memory://")
    markov.learn("My favorite animal is the crocodile")
    markov.learn("The word animal is six letters long")
    print(markov.generate())

Here the ``markov`` instance learns two sentences (presumably gathered
from a chat network such as IRC or Discord). What is interesting is that
the ‘animal is’ sequence appears twice. So the ``generate()`` method,
which returns a completely random result, may return an entirely built
sentence which hasn’t been ever written by anyone:

.. code:: bash

    $ ./memory.py
    The word animal is the crocodile
    $ ./memory
    My favorite animal is six letters long

The more sentences, the funnier generated ones.


Supported databases
-------------------

-   Redis **(recommended)**: you can either provide a unix socket path (e.g.
    ``redis:///path/to/unix_socket.sock;db=0;password=foobar`` or a
    ``host:port`` (e.g ``redis://localhost:6739;db=0``). Extra parameters are
    separated by semi-colons after the unix socket path / host:port descriptor.
    For the async version, use ``redis_async://`` instead.
-   JSON: you can provide a path to a file that will be formated with JSON.
    Example: ``json:///path/to/file.json``
-   Memory: in-memory database, just provide ``memory://`` as a connect
    string. For the async version, use ``memory_async://`` instead.

Contribute
----------

If you want to add some support to a database or redesign the library,
please make a pull request so we can discuss about it.

Todo
----

-  Support other databases?

.. |codecov| image:: https://codecov.io/gh/Ge0/chattymarkov/branch/master/graph/badge.svg
   :target: https://codecov.io/gh/Ge0/chattymarkov
.. |travis build| image:: https://travis-ci.org/Ge0/chattymarkov.svg?branch=master
.. |pypi version| image:: https://badge.fury.io/py/chattymarkov.svg
   :target: https://badge.fury.io/py/chattymarkov
