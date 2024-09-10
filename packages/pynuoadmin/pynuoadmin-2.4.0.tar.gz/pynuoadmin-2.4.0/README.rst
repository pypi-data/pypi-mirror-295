==================
NuoDB - Pynuoadmin
==================

.. contents::

This package enables the nuoadmin client management of a NuoDB database
without the need to install the full NuoDB product distribution on a
client machine.

Requirements
------------

* Python -- one of the following:

  - CPython_ >= 3.6 or == 2.7

* NuoDB -- one of the following:

  - NuoDB_ >= 5.0


If you haven't done so already, and plan to use pynuoadmin with the NuoDB
Community Edition, visit `Download and Install NuoDB`_.

Installation
------------

The last stable release is available on PyPI and can be installed with
``pip``::

    $ pip install 'pynuoadmin[completion]'
    $ eval "$(register-python-argcomplete nuocmd)"

We recommend installing using the "completion" module, to enable command
line argument completion.

Alternatively (e.g. if ``pip`` is not available), a tarball can be
`downloaded from PyPI <https://pypi.org/project/pynuoadmin/#files>`_ and
installed with setuptools::

    $ tar xzf pynuoadmin-*.tar.gz
    $ cd nuodb-pynuoadmin*
    $ python setup.py install

The tar file and folder nuodb-pynuoadmin* can be safely removed after
installation.

Example
-------

Run the following command to confirm the pynuoadmin package is installed
properly::

    $ nuocmd show domain


Resources
---------

NuoDB Documentation: https://doc.nuodb.com/

License
-------

Pynuoadmin is licensed under a `BSD 3-Clause License`_.

.. _BSD 3-Clause License: https://github.com/nuodb/nuodb-python/blob/master/LICENSE
.. _Download and Install NuoDB: https://doc.nuodb.com/nuodb/latest/quick-start-guide/
.. _NuoDB: https://www.3ds.com/nuodb-distributed-sql-database/
.. _CPython: https://www.python.org/
