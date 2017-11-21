"""Chattymarkov database submodule.

This submodule gathers all the supported database formats.
"""
# flake8: noqa
from .json import JSONFileDatabase
from .memory import MemoryDatabase
from .redis import RedisDatabase


class ChattymarkovDatabaseError(Exception):
    """Base exception class for chattymarkov.database related errors."""


class UnknownDatabasePrefixerror(ChattymarkovDatabaseError):
    """Exception class for unknown database prefixes errors."""


class InvalidConnectionStringError(ChattymarkovDatabaseError):
    """Exception class for invalid connection string error."""


_DATABASE_PREFIXES = {}


def database(prefix):
    """Wrap a function responsible for building a database."""

    def wrapper(func):
        """Register `func` in the global `_DATABASE_PREFIXES` hash."""
        _DATABASE_PREFIXES[prefix] = func
        return func
    return wrapper


def get_database_builder(prefix):
    """Get the function associated to `prefix` to instanciate a database.
    
    This function is a simple interface around the `_DATABASE_PREFIXES` hash.

    Args:
        prefix (str): the prefix's database function.

    Raises:
        UnknownDatabasePrefixError: the prefix is not recognized.

    Returns:
        function: the function assiociated to the `prefix`.
    """
    if prefix not in _DATABASE_PREFIXES:
        raise UnknownDatabasePrefixError(
            "Database prefix '{}' is unknown.".format(prefix))
    return _DATABASE_PREFIXES[prefix]


@database('redis')
def build_redis_database(resource):
    """Build a `RedisDatabase` instance to communicate with a redis server.

    Args:
        resource (str): a string that represents connection information.

    Returns:
        RedisDatabase: instance to communicate with the redis server.
    """
    whitelist = {'db'}
    extra_params = {}

    connection, *params = resource.split(';')

    # Parse additional parameters, if any
    if len(params) > 0:
        for param in params:
            key, equal, value = param.partition('=')
            if key in whitelist:
                extra_params[key] = value

    if connection.startswith('/'):
        # UNIX socket connection
        return RedisDatabase(unix_socket_path=connection,
                             **extra_params)
    else:
        # TCP socket connection
        host, colon, port = connection.partition(':')
        if host != '' and colon == ':' and port.isnumeric():
            return RedisDatabase(host=host, port=int(port),
                                 **extra_params)


def build_database_connection(connect_string):
    """Build a database connection based on `connect_string`.

    Args:
        connect_string (str): connection string for the database connection.

    Raises:
        InvalidConnectionStringError: raised when the `connect_string` is
            invalid.
        UnknownDatabasePrefixError: raised when the database prefix is
            unknown.
    Returns:
        AbstractDatabase: an instance of AbstractDatabase that handle a
            connection to the desired database.
    """
    prefix, colon_slash_slash, resource = connect_string.partition('://')
    if resource != '':
        builder = get_database_builder(prefix)
        return builder(resource)
    else:
        raise InvalidConnectionStringError(
            "Invalid connection string '{}'. Must be of the form "
            "prefix://resource;param1=value1;param2=value2...")
