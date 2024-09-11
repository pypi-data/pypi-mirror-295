:title: Installing

Installing
==========

The module is known to pip and Debian-based distributions as
``gerritlib``.

``pip``::

    pip install gerritlib

``easy_install``::

    easy_install gerritlib

The module has been packaged since Ubuntu Oneiric (11.10)::

    apt-get install gerritlib

And on Fedora 19 and later::

    yum install gerritlib

For development::

    python setup.py develop


Documentation
-------------

Documentation is included in the ``doc`` folder. To generate docs
locally execute the command::

    nox -s docs

The generated documentation is then available under
``doc/build/html/index.html``.

Unit Tests
----------

Unit tests are in the ``tests`` folder.
To run the unit tests, execute the command::

    nox -s tests

* Note: Pass ``--force-python 3.x`` to run under other versions of python.

