Matchlight Python SDK
=====================

.. image:: https://img.shields.io/travis/TerbiumLabs/python-matchlightsdk.svg
   :target: https://travis-ci.org/TerbiumLabs/python-matchlightsdk

.. image:: https://img.shields.io/coveralls/TerbiumLabs/python-matchlightsdk.svg
   :target: https://coveralls.io/r/TerbiumLabs/python-matchlightsdk

Matchlight exists to quickly and privately alert its users when any of their
sensitive information appears for sale or vandalism out on the dark web. The
product is fully automated, and operates using Data Fingerprints — a one-way
representation that allows Terbium to monitor for client data without
needing to know what that data is.

The Matchlight SDK provides a Python interface to Matchlight's API, allowing
developers to create and retrieve projects, download feeds, create document,
source code, and PII records, and perform searches.

Installation
------------

Matchlight SDK is supported on Python 2.7, 3.3, 3.4, and 3.5. To install the
SDK, you'll need `pip <https://pip.pypa.io/en/stable/>`_:

.. code-block:: shell
    $ pip install matchlightsdk

Documentation
-------------

A walkthrough of the SDK features and API documentation is available at
https://python-matchlightsdk.readthedocs.io.

License
-------

The Matchlight Python SDK source code is licensed under the
`3-clause BSD License <https://opensource.org/licenses/BSD-3-Clause>`_. For
more information, please see the LICENSE file included in this repository or
source distribution.

Contributing
------------

Bug reports and pull requests are welcome. If you would like to contribute,
please create a pull request against **master**. Include unit tests if
necessary, and ensure that your code passes all linters (see tox.ini).
