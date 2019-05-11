"""Chattymarkov database submodule.

This submodule gathers all the supported database formats.
"""
from .databases import (JSONFileDatabase, MemoryDatabase, MemoryDatabaseAsync,
                        RedisDatabase, RedisDatabaseAsync)


class ChattymarkovDatabaseError(Exception):
    """Base exception class for chattymarkov.database related errors."""


class UnknownDatabasePrefixError(ChattymarkovDatabaseError):
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


def _get_connection_params(resource):
    """Extract connection and params from `resource`."""
    args = resource.split(';')
    if len(args) > 1:
        return args[0], args[1:]
    else:
        return args[0], []


@database("redis_async")
def build_redis_database_async(resource: str):
    """Build a `RedisDatabaseAsync` instance to communicate with a redis
    server.

    See also:
        `build_redis_database`

    """
    return build_redis_database(resource, True)


@database('redis')
def build_redis_database(resource: str, is_async: bool = False):
    """Build a `RedisDatabase` or a `RedisDatabaseAsync` instance to
    communicate with a redis server.

    Args:
        resource (str): a string that represents connection information.
        is_async (bool): True to build a `RedisDatabaseAsync` instance,
            False to build a `RedisDatabase` instance.

    Returns:
        An instance to communicate with the redis server.
    """
    whitelist = {'password', 'db'}
    extra_params = {}

    connection, params = _get_connection_params(resource)

    # Parse additional parameters, if any
    if len(params) > 0:
        for param in params:
            key, equal, value = param.partition('=')
            if key in whitelist:
                extra_params[key] = value

    if connection.startswith('/'):
        # UNIX socket connection
        if is_async:
            return RedisDatabaseAsync(unix_socket_path=connection,
                                      **extra_params)
        else:
            return RedisDatabase(unix_socket_path=connection,
                                 **extra_params)
    else:
        # TCP socket connection
        host, colon, port = connection.partition(':')

        if host != '' and colon == ':' and port.isnumeric():
            if is_async:
                return RedisDatabaseAsync(host=host, port=int(port),
                                          **extra_params)
            else:
                return RedisDatabase(host=host, port=int(port),
                                     **extra_params)


@database('memory')
def build_memory_database(resource):
    """Build a `MemoryDatabase` instance.

    Args:
        resource (str): path to the memory location. It has actually no sense
            at that time. Should be "memory://" anyway.

    Returns:
        MemoryDatabase: an instance of MemoryDatabase that handles a
            connection to the desired database.
    """
    return MemoryDatabase()


@database("memory_async")
def build_async_memory_database(resource):
    """Build a `MemoryDatabaseAsync` instance.

    Args:
        resource (str): path to the memory location. It has actually no sense
            at that time. Should be "async_memory://" anyway.

    Returns:
        MemoryDatabaseAsync: an instance of MemoryDatabaseAsync that handles a
            connection to the desired database.

    """
    return MemoryDatabaseAsync()


@database('json')
def build_json_database(resource):
    """Build a `JSONFileDatabase` instance.

    Args:
        resource (str): path to the JSON file representing the database. If
            the file is not empty, it will be loaded. In every cases, upon
            instance destruction, the database will be stored in the specified
            file.

    Returns:
        JSONFileDatabase: an instance of JSONFileDatabase that handles a
            connection to the desired database.
    """
    return JSONFileDatabase(resource)


def build_database_connection(connect_string):
    """Build a database connection based on *connect_string*.

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
    if colon_slash_slash != '':
        builder = get_database_builder(prefix)
        return builder(resource)
    else:
        raise InvalidConnectionStringError(
            "Invalid connection string '{}'. Must be of the form "
            "prefix://[resource[;param1=value1;param2=value2...]]".format(
                prefix))
