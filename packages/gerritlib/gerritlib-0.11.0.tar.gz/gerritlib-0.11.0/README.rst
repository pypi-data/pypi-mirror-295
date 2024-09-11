README
======

Gerritlib is a Python library for interacting with Gerrit_.
It aims to provide a more conventionally pythonic way of managing a
Gerrit instance.


To install::

    $ sudo python setup.py install

Online documentation:

* http://gerritlib.readthedocs.org/en/latest/

Developers
----------
Bug report:

* https://storyboard.openstack.org/#!/project/718

Repository:

* https://opendev.org/opendev/gerritlib

Cloning::

    git clone https://opendev.org/opendev/gerritlib

Patches are submitted via Gerrit at:

* https://review.opendev.org/

Please do not submit GitHub pull requests, they will be automatically closed.

More details on how you can contribute is available at:

* https://docs.opendev.org/opendev/infra-manual/latest/developers.html

Writing a patch
---------------

We ask that all code submissions be pep8_ and pyflakes_ clean.  The
easiest way to do that is to run nox_ before submitting code for
review in Gerrit.  It will run ``pep8`` and ``pyflakes`` in the same
manner as the automated test suite that will run on proposed
patchsets.


Installing without setup.py
---------------------------

Then install the required python packages using pip_::

    $ sudo pip install gerritlib

.. _Gerrit: https://www.gerritcodereview.com/
.. _pyflakes: https://pypi.python.org/pypi/pyflakes
.. _nox: https://nox.thea.codes/en/stable/
.. _pip: https://pypi.python.org/pypi/pip
.. _pep8: https://pypi.python.org/pypi/pep8
