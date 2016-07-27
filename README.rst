========
Overview
========

.. start-badges

.. list-table::
    :stub-columns: 1

    * - docs
      - |docs|
    * - tests
      - | |travis| |appveyor| |requires|
        | |codecov|
    * - package
      - |version| |downloads| |wheel| |supported-versions| |supported-implementations|

.. |docs| image:: https://readthedocs.org/projects/python-poetaster/badge/?style=flat
    :target: https://readthedocs.org/projects/python-poetaster
    :alt: Documentation Status

.. |travis| image:: https://travis-ci.org/jkahn/python-poetaster.svg?branch=master
    :alt: Travis-CI Build Status
    :target: https://travis-ci.org/jkahn/python-poetaster

.. |appveyor| image:: https://ci.appveyor.com/api/projects/status/github/jkahn/python-poetaster?branch=master&svg=true
    :alt: AppVeyor Build Status
    :target: https://ci.appveyor.com/project/jkahn/python-poetaster

.. |requires| image:: https://requires.io/github/jkahn/python-poetaster/requirements.svg?branch=master
    :alt: Requirements Status
    :target: https://requires.io/github/jkahn/python-poetaster/requirements/?branch=master

.. |codecov| image:: https://codecov.io/github/jkahn/python-poetaster/coverage.svg?branch=master
    :alt: Coverage Status
    :target: https://codecov.io/github/jkahn/python-poetaster

.. |version| image:: https://img.shields.io/pypi/v/poetaster.svg?style=flat
    :alt: PyPI Package latest release
    :target: https://pypi.python.org/pypi/poetaster

.. |downloads| image:: https://img.shields.io/pypi/dm/poetaster.svg?style=flat
    :alt: PyPI Package monthly downloads
    :target: https://pypi.python.org/pypi/poetaster

.. |wheel| image:: https://img.shields.io/pypi/wheel/poetaster.svg?style=flat
    :alt: PyPI Wheel
    :target: https://pypi.python.org/pypi/poetaster

.. |supported-versions| image:: https://img.shields.io/pypi/pyversions/poetaster.svg?style=flat
    :alt: Supported versions
    :target: https://pypi.python.org/pypi/poetaster

.. |supported-implementations| image:: https://img.shields.io/pypi/implementation/poetaster.svg?style=flat
    :alt: Supported implementations
    :target: https://pypi.python.org/pypi/poetaster


.. end-badges

Poetry tricks and tools for found -- and generated -- poetry.

* Free software: BSD license

Installation
============

::

    pip install poetaster

Documentation
=============

https://python-poetaster.readthedocs.io/

Development
===========

To run the all tests run::

    tox

Note, to combine the coverage data from all the tox environments run:

.. list-table::
    :widths: 10 90
    :stub-columns: 1

    - - Windows
      - ::

            set PYTEST_ADDOPTS=--cov-append
            tox

    - - Other
      - ::

            PYTEST_ADDOPTS=--cov-append tox
