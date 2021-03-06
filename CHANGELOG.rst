Changelog All notable changes to this project will be documented in this
file.

The format is based on `Keep a
Changelog <http://keepachangelog.com/en/1.0.0/>`__ and this project
adheres to `Semantic Versioning <http://semver.org/spec/v2.0.0.html>`__.

[Unreleased] 2020-09-22
-----------------------

Changed
~~~~~~~

- Add an extra prefix on the learn method


[1.3.0] 2020-09-02
------------------

Changed
~~~~~~~

- Accept standard redis URL for connection strings.

[1.2.8] 2020-09-02
------------------

Added
~~~~~

- Option to force async mode.

[1.2.7] 2019-05-12
------------------

Fixed
~~~~~

- Use await into context managers for RedisDatabaseAsync

[1.2.6] 2019-05-12
------------------

Fixed
~~~~~

- Use connection pool the right way in RedisDatabaseAsync

[1.2.5] 2019-05-11
------------------

Fixed
~~~~~

- Forward db number and password through connection pool in RedisDatabaseAsync

[1.2.4] 2019-05-11
------------------

Fixed
~~~~~

- Use connection pool for RedisDatabaseAsync

[1.2.3] 2019-05-11
------------------

Added
~~~~~

- Added MemoryAsync class

[1.2.2] 2019-01-10
------------------

Fixed
~~~~~

- Fixed RedisDatabaseAsync class

[1.2.1] 2019-01-04
------------------

Fixed
~~~~~

- Add redis to project dependencies.

[1.2.0] 2018-12-07
------------------

Added
~~~~~

-  Add asynchronous support for redis databases.

.. _section-1:

[1.1.1] 2018-04-21
------------------

Changed
~~~~~~~

-  Fix bug with installation.

.. _section-2:

[1.1.0] 2017-11-25
------------------

.. _added-1:

Added
~~~~~

-  Redis databases have password option.

.. _section-3:

[1.0.2] - 2017-11-21
--------------------

.. _changed-1:

Changed
~~~~~~~

-  Add documentation.

.. _section-4:

[1.0.1] - 2017-11-21
--------------------

.. _added-2:

Added
~~~~~

-  Long description in rst format. ### Changed
-  Fix changelog typo.

.. _section-5:

[1.0.0] - 2017-11-21
--------------------

.. _added-3:

Added
~~~~~

-  Add tests. ### Change.
-  Use connection strings for databases.

.. _section-6:

[0.0.4] - 2017-10-07
--------------------

.. _changed-2:

Changed
~~~~~~~

-  Reupload python package on pypi.

.. _section-7:

[0.0.3] - 2017-10-07
--------------------

.. _added-4:

Added
~~~~~

-  codecov badge in the README.md file. ### Changed
-  Fix setup.py to get a static version number.
-  Refactore setup.py.

.. _section-8:

[0.0.2] - 2017-10-07
--------------------

.. _added-5:

Added
~~~~~

-  Changelog file.
-  Travis checks for flake8, isort and code coverage.

.. _changed-3:

Changed
~~~~~~~

-  Fix typos.
-  Fix setup.py.

.. _section-9:

[0.0.1] - 2017-10-06
--------------------

.. _added-6:

Added
~~~~~

-  chattymarkov code base.
-  Memory database.
-  JSON database.
-  Redis database.
-  Tests.
