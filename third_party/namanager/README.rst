=========
namanager
=========

.. include-documentation-begin-marker

.. image:: https://img.shields.io/travis/iattempt/namanager/master.svg?style=flat&label=Linux
        :target: https://travis-ci.org/iattempt/namanager
        :alt: see build status of Unix-like: https://travis-ci.org/iattempt/namanager

.. image:: https://img.shields.io/appveyor/ci/iattempt/namanager/master.svg?style=flat&label=Windows
        :target: https://ci.appveyor.com/project/iattempt/namanager
        :alt: see build status of Windows: https://ci.appveyor.com/project/iattempt/namanager/branch/master

.. image:: https://img.shields.io/codecov/c/github/iattempt/namanager/master.svg?style=flat
        :target: https://codecov.io/gh/iattempt/namanager
        :alt: see code coverage status: https://codecov.io/gh/iattempt/namanager

.. image:: https://img.shields.io/pypi/v/namanager.svg?style=flat
    :target: https://pypi.python.org/pypi/namanager

A file or/and directory name manager which could determine names are/aren't expectable, and you could also automatically rename it.

.. include-documentation-end-marker


Features
--------

* Match or ignore particular files/directories.
* Supports checking of most common format of letter-cases (upper, lower, camel, and pascal-case).
* Supports checking of convention of word separators (underscore-to-dash/dash-to-underscore).

How to use?
-----------

Installation
~~~~~~~~~~~~

* First of all check you already have **pip** installed, and then just type in:

.. code-block:: sh

    pip install namanager

* Sometimes, you need to install on offline environments, hence that you could download *wheel* s from `PyPI <https://pypi.python.org/pypi/namanager>`_ or by **pip**:

.. code-block:: sh

    pip download namanager

After moved wheels (involve dependencies) into your env, you could manually install it by following commands:

.. code-block:: sh

    pip install namanager-x.x.x-py2.py3-none-any.whl

Running
~~~~~~~

1) Configure your *settings.json*.

2) Run command

.. code-block:: sh

    namanager

If the settings file doesn't existed in your current working directory or CWD:

.. code-block:: sh

    namanager --settings /path/to/your/settings
