.. |img-pyVersioning-github| image:: https://img.shields.io/badge/Paebbels-pyVersioning-323131.svg?logo=github&longCache=true
   :alt: Sourcecode on GitHub
   :height: 22
   :target: https://github.com/Paebbels/pyVersioning
.. |img-pyVersioning-license| image:: https://img.shields.io/badge/Apache%20License,%202.0-bd0000.svg?longCache=true&label=license&logo=Apache&logoColor=D22128
   :alt: License
   :height: 22
.. |img-pyVersioning-tag| image:: https://img.shields.io/github/v/tag/Paebbels/pyVersioning?logo=GitHub&include_prereleases
   :alt: GitHub tag (latest SemVer incl. pre-release
   :height: 22
   :target: https://github.com/Paebbels/pyVersioning/tags
.. |img-pyVersioning-release| image:: https://img.shields.io/github/v/release/Paebbels/pyVersioning?logo=GitHub&include_prereleases
   :alt: GitHub release (latest SemVer incl. including pre-releases
   :height: 22
   :target: https://github.com/Paebbels/pyVersioning/releases/latest
.. |img-pyVersioning-date| image:: https://img.shields.io/github/release-date/Paebbels/pyVersioning?logo=GitHub
   :alt: GitHub release date
   :height: 22
   :target: https://github.com/Paebbels/pyVersioning/releases
.. |img-pyVersioning-lib-status| image:: https://img.shields.io/librariesio/release/pypi/pyVersioning
   :alt: Libraries.io status for latest release
   :height: 22
   :target: https://libraries.io/github/Paebbels/pyVersioning
.. |img-pyVersioning-req-status| image:: https://img.shields.io/requires/github/Paebbels/pyVersioning
   :alt: Requires.io
   :height: 22
   :target: https://requires.io/github/Paebbels/pyVersioning/requirements/?branch=master
.. |img-pyVersioning-travis| image:: https://img.shields.io/travis/com/Paebbels/pyVersioning?logo=Travis
   :alt: Travis - Build on 'master'
   :height: 22
   :target: https://travis-ci.com/Paebbels/pyVersioning
.. |img-pyVersioning-pypi-tag| image:: https://img.shields.io/pypi/v/pyVersioning?logo=PyPI
   :alt: PyPI - Tag
   :height: 22
   :target: https://pypi.org/project/pyVersioning/
.. |img-pyVersioning-pypi-status| image:: https://img.shields.io/pypi/status/pyVersioning?logo=PyPI
   :alt: PyPI - Status
   :height: 22
.. |img-pyVersioning-pypi-python| image:: https://img.shields.io/pypi/pyversions/pyVersioning?logo=PyPI
   :alt: PyPI - Python Version
   :height: 22
.. |img-pyVersioning-lib-dep| image:: https://img.shields.io/librariesio/dependent-repos/pypi/pyVersioning
   :alt: Dependent repos (via libraries.io)
   :height: 22
   :target: https://github.com/Paebbels/pyVersioning/network/dependents
.. |img-pyVersioning-codacy-quality| image:: https://img.shields.io/codacy/grade/b63aac7ef7e34baf829f11a61574bbaf?logo=codacy
   :alt: Codacy - Quality
   :height: 22
   :target: https://www.codacy.com/manual/Paebbels/pyVersioning
.. |img-pyVersioning-codacy-coverage| image:: https://img.shields.io/codacy/coverage/b63aac7ef7e34baf829f11a61574bbaf?logo=codacy
   :alt: Codacy - Line Coverage
   :height: 22
   :target: https://www.codacy.com/manual/Paebbels/pyVersioning
.. |img-pyVersioning-codecov-coverage| image:: https://codecov.io/gh/Paebbels/pyVersioning/branch/master/graph/badge.svg
   :alt: Codecov - Branch Coverage
   :height: 22
   :target: https://codecov.io/gh/Paebbels/pyVersioning
.. |img-pyVersioning-lib-rank| image:: https://img.shields.io/librariesio/sourcerank/pypi/pyVersioning
   :alt: Libraries.io SourceRank
   :height: 22
   :target: https://libraries.io/github/Paebbels/pyVersioning/sourcerank
.. |img-pyVersioning-rtd| image:: https://img.shields.io/readthedocs/pyversioning
   :alt: Read the Docs
   :height: 22
   :target: https://pyVersioning.readthedocs.io/en/latest/

|img-pyVersioning-github| |img-pyVersioning-tag| |img-pyVersioning-release| |img-pyVersioning-date| |br|
|img-pyVersioning-lib-status| |img-pyVersioning-req-status| |img-pyVersioning-lib-dep| |br|
|img-pyVersioning-travis| |img-pyVersioning-pypi-tag| |img-pyVersioning-pypi-status| |img-pyVersioning-pypi-python| |br|
|img-pyVersioning-codacy-quality| |img-pyVersioning-codacy-coverage| |img-pyVersioning-codecov-coverage| |img-pyVersioning-lib-rank| |br|
|img-pyVersioning-rtd| |img-pyVersioning-license|

.. code-block:: text

              __     __            _             _
    _ __  _   \ \   / /__ _ __ ___(_) ___  _ __ (_)_ __   __ _
   | '_ \| | | \ \ / / _ \ '__/ __| |/ _ \| '_ \| | '_ \ / _` |
   | |_) | |_| |\ V /  __/ |  \__ \ | (_) | | | | | | | | (_| |
   | .__/ \__, | \_/ \___|_|  |___/_|\___/|_| |_|_|_| |_|\__, |
   |_|    |___/                                          |___/


pyVersioning Documentation
##########################

The Python package `pyVersioning` offers a template tool to write version information for any programming language as a
source file that can be included into the normal build flow.

The main idea is to provide a unified tool to collect all necessary version information from a configuration file, user
defined parameters, version control systems (e.g. Git) or environment variables. Especially the latter ones can be
tricky in CI environments, as every CI service uses different environment variables.

.. topic:: Planned features

   * read template from ``STDIN``.
   * add C++ example
   * add VHDL example

Use Cases
*********

* Integrate version information from e.g. Git into current builds

Supported Version Control Systems
*********************************

* `Git <https://git-scm.com/>`__
* `Subversion (SVN) <https://subversion.apache.org/>`__ (planned)
* more to come

Supported CI Services
*********************

* `Appveyor <https://www.appveyor.com/>`__
* `GitHub Actions <https://github.com/>`__
* `GitLab <https://about.gitlab.com/>`__
* `Travis-CI <https://www.travis-ci.com/>`__
* more to come


Supported Languages
*******************

* Any language


Tested with ...
***************

* ANSI C
* VHDL


Examples
********

* ANSI C Example
* VHDL Example


.. _CONTRIBUTORS:

Contributors
************

* `Patrick Lehmann <https://GitHub.com/Paebbels>`__ (Maintainer)
* `and more... <https://GitHub.com/Paebbels/pyVersioning/graphs/contributors>`__


.. _LICENSE:

License
*******

.. only:: html

   This Python package (source code) is licensed under `Apache License 2.0 <Code-License.html>`__. |br|
   The accompanying documentation is licensed under `Creative Commons - Attribution 4.0 (CC-BY 4.0) <Doc-License.html>`__.

.. only:: latex

   This Python package (source code) is licensed under **Apache License 2.0**. |br|
   The accompanying documentation is licensed under **Creative Commons - Attribution 4.0 (CC-BY 4.0)**.


.. toctree::
   :caption: Overview
   :hidden:

   Installation
   Dependency

.. raw:: latex

   \part{Main Documentation}

.. toctree::
   :caption: Details
   :hidden:

   Usage
   VersionControlSystems
   CIServices
   Languages

.. toctree::
   :caption: Templates
   :hidden:

   templates/index
   templates/ANSI-C

.. toctree::
   :caption: Examples
   :hidden:

   examples/ANSI-C
   examples/VHDL

.. raw:: latex

   \part{References and Reports}

.. toctree::
   :caption: References and Reports
   :hidden:

   CommandLineInterface
   Python Class Reference <pyVersioning/pyVersioning>
   unittests/index
   coverage/index
   Doc. Coverage Report <DocCoverage>
   Static Type Check Report ➚ <typing/index>

.. raw:: latex

   \part{Appendix}

.. toctree::
   :caption: Appendix
   :hidden:

   License
   Doc-License
   Glossary
   genindex
   Python Module Index <modindex>
   TODO
