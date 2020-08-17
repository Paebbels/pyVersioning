Dependencies
############

.. |img-pyVersioning-lib-status| image:: https://img.shields.io/librariesio/release/pypi/pyVersioning
   :alt: Libraries.io status for latest release
   :height: 22
   :target: https://libraries.io/github/Paebbels/pyVersioning
.. |img-pyVersioning-req-status| image:: https://img.shields.io/requires/github/Paebbels/pyVersioning
   :alt: Requires.io
   :height: 22
   :target: https://requires.io/github/Paebbels/pyVersioning/requirements/?branch=master

+------------------------------------------+------------------------------------------+
| `Libraries.io <https://libraries.io/>`_  | `Requires.io <https://requires.io/>`_    |
+==========================================+==========================================+
| |img-pyVersioning-lib-status|            | |img-pyVersioning-req-status|            |
+------------------------------------------+------------------------------------------+


Mandatory Dependencies
**********************

Installing Requirements Manually
================================

Use the :file:`requirements.txt` file to install all dependencies via ``pip3``
or install the package directly from PyPI (see :ref:`INSTALL`).

.. code-block:: shell

   pip3 install -U -r requirements.txt


Dependency List
===============

.. |img-autocomplete-github| image:: https://img.shields.io/badge/rodricios-autocomplete-323131.svg?logo=github&longCache=true
   :alt: Sourcecode on GitHub
   :height: 22
   :target: https://github.com/rodricios/autocomplete
.. |img-autocomplete-pypi-license| image:: https://img.shields.io/pypi/l/autocomplete
   :alt: License shown at PyPI
   :height: 22
   :target: https://pypi.org/project/autocomplete/
.. |img-autocomplete-pypi-version| image:: https://img.shields.io/pypi/v/autocomplete
   :alt: Version shown at PyPI
   :height: 22
   :target: https://pypi.org/project/autocomplete/
.. |img-autocomplete-rtd| replace:: README
.. _img-autocomplete-rtd: https://github.com/rodricios/autocomplete/blob/master/README.rst

.. # image:: https://img.shields.io/readthedocs/pyVersioning
   :alt: Read the Docs
   :height: 22
   :target: https://pyVersioning.readthedocs.io/en/latest/

+----------------+---------------------------+----------------------------------------+--------------------------------------+--------------------------+
| Package        | Repository                | PyPI - Latest                          | PyPI - License                       | Documentation            |
+================+===========================+========================================+======================================+==========================+
| autocomplete   | |img-autocomplete-github| | |img-autocomplete-pypi-version|        | |img-autocomplete-pypi-license|      | |img-autocomplete-rtd|_  |
+----------------+---------------------------+----------------------------------------+--------------------------------------+--------------------------+


Optional Dependencies for Build and Test
****************************************

Installing Requirements Manually
================================

Use the :file:`tests/requirements.txt` file to install all dependencies via
``pip3``. The file will recursively install the mandatory dependencies too.

.. code-block:: shell

   pip3 install -U -r tests/requirements.txt

.. |img-coverage-github| image:: https://img.shields.io/badge/nedbat-coveragepy-323131.svg?logo=github&longCache=true
   :alt: Sourcecode on GitHub
   :height: 22
   :target: https://github.com/nedbat/coveragepy
.. |img-coverage-pypi-license| image:: https://img.shields.io/pypi/l/coverage
   :alt: License shown at PyPI
   :height: 22
   :target: https://pypi.org/project/coverage/
.. |img-coverage-pypi-version| image:: https://img.shields.io/pypi/v/coverage
   :alt: Version shown at PyPI
   :height: 22
   :target: https://pypi.org/project/coverage/
.. |img-coverage-rtd| image:: https://img.shields.io/readthedocs/coverage
   :alt: Read the Docs
   :height: 22
   :target: https://coverage.readthedocs.io/en/latest/

.. |img-codacy-github| image:: https://img.shields.io/badge/codacy-python--codacy--coverage-323131.svg?logo=github&longCache=true
   :alt: Sourcecode on GitHub
   :height: 22
   :target: https://github.com/codacy/python-codacy-coverage
.. |img-codacy-pypi-license| image:: https://img.shields.io/pypi/l/codacy-coverage
   :alt: License shown at PyPI
   :height: 22
   :target: https://pypi.org/project/codacy-coverage/
.. |img-codacy-pypi-version| image:: https://img.shields.io/pypi/v/codacy-coverage
   :alt: Version shown at PyPI
   :height: 22
   :target: https://pypi.org/project/codacy-coverage/
.. |img-codacy-rtd| replace:: README
.. _img-codacy-rtd: https://github.com/codacy/python-codacy-coverage/blob/master/README.rst

.. |img-codecov-github| image:: https://img.shields.io/badge/codecov-codecov--python-323131.svg?logo=github&longCache=true
   :alt: Sourcecode on GitHub
   :height: 22
   :target: https://github.com/codecov/codecov-python
.. |img-codecov-pypi-license| image:: https://img.shields.io/pypi/l/codecov
   :alt: License shown at PyPI
   :height: 22
   :target: https://pypi.org/project/codecov/
.. |img-codecov-pypi-version| image:: https://img.shields.io/pypi/v/codecov
   :alt: Version shown at PyPI
   :height: 22
   :target: https://pypi.org/project/codecov/
.. |img-codecov-rtd| replace:: README
.. _img-codecov-rtd: https://github.com/codecov/codecov-python/blob/master/README.md

+------------------+-----------------------+----------------------------------+---------------------------------+--------------------------+
| Package          | Repository            | PyPI - Latest                    | PyPI - License                  | Documentation            |
+==================+=======================+==================================+=================================+==========================+
| Coverage         | |img-coverage-github| | |img-coverage-pypi-version|      | |img-coverage-pypi-license|     | |img-coverage-rtd|       |
+------------------+-----------------------+----------------------------------+---------------------------------+--------------------------+
| codacy-coverage  | |img-codacy-github|   | |img-codacy-pypi-version|        | |img-codacy-pypi-license|       | |img-codacy-rtd|_        |
+------------------+-----------------------+----------------------------------+---------------------------------+--------------------------+
| codecov          | |img-codecov-github|  | |img-codecov-pypi-version|       | |img-codecov-pypi-license|      | |img-codecov-rtd|_       |
+------------------+-----------------------+----------------------------------+---------------------------------+--------------------------+



Optional Dependencies for Documentation
***************************************

Installing Requirements Manually
================================

Use the :file:`doc/requirements.txt` file to install all dependencies via
``pip3``. The file will recursively install the mandatory dependencies too.

.. code-block:: shell

   pip3 install -U -r doc/requirements.txt

+----------------------------+---------------------------------------+----------------------------------------------+--------------------------------------------------+-----------------------------------------+
| Package                    | Repository                            | PyPI - Latest                                | PyPI - License                                   | Documentation                           |
+============================+=======================================+==============================================+==================================================+=========================================+
| sphinx                     | |img-sphinx-github|                   | |img-sphinx-pypi-version|                    | |img-sphinx-pypi-license|                        | |img-sphinx-rtd|                        |
+----------------------------+---------------------------------------+----------------------------------------------+--------------------------------------------------+-----------------------------------------+
| sphinx-rtd-theme           | |img-sphinx-rtd-theme-github|         | |img-sphinx-rtd-theme-pypi-version|          | |img-sphinx-rtd-theme-pypi-license|              | |img-sphinx-rtd-theme-rtd|              |
+----------------------------+---------------------------------------+----------------------------------------------+--------------------------------------------------+-----------------------------------------+
| sphinx_fontawesome         | |img-sphinx-fontawesome-github|       | |img-sphinx-fontawesome-pypi-version|        | |img-sphinx-fontawesome-pypi-license|            | |img-sphinx-fontawesome-rtd|            |
+----------------------------+---------------------------------------+----------------------------------------------+--------------------------------------------------+-----------------------------------------+
| sphinx_autodoc_typehints   | |img-sphinx-autodoc-typehints-github| | |img-sphinx-autodoc-typehints-pypi-version|  | |img-sphinx-autodoc-typehints-pypi-license|      | |img-sphinx-autodoc-typehints-rtd|      |
+----------------------------+---------------------------------------+----------------------------------------------+--------------------------------------------------+-----------------------------------------+
| Pygments                   | |img-pygments-github|                 | |img-pygments-pypi-version|                  | |img-pygments-pypi-license|                      | |img-pygments-rtd|                      |
+----------------------------+---------------------------------------+----------------------------------------------+--------------------------------------------------+-----------------------------------------+
