.. raw:: latex

   \part{Introduction}

.. code-block:: text

              __     __            _             _
    _ __  _   \ \   / /__ _ __ ___(_) ___  _ __ (_)_ __   __ _
   | '_ \| | | \ \ / / _ \ '__/ __| |/ _ \| '_ \| | '_ \ / _` |
   | |_) | |_| |\ V /  __/ |  \__ \ | (_) | | | | | | | | (_| |
   | .__/ \__, | \_/ \___|_|  |___/_|\___/|_| |_|_|_| |_|\__, |
   |_|    |___/                                          |___/


.. shields::
   :github:                Paebbels/pyVersioning
   :pypi:                  pyVersioning
   :codacy:                fda25870e76849f48bbf7415fb6e9ccf
   :source-license:        github:LICENSE.md
   :documentation-license: CC-BY-4.0 github:doc/Doc-License.rst
   :github-action:         Pipeline.yml@main
   :documentation:         github-pages

   github, src-license, ghp-doc, doc-license
   pypi-tag, pypi-status, pypi-python
   github-action, lib-status, codacy-quality, codacy-coverage, codecov-coverage

--------------------------------------------------------------------------------

pyVersioning Documentation
##########################

The Python package ``pyVersioning`` offers a template tool to write version information for any programming language as
a source file that can be included into the normal application build flow.

The main idea is to provide a unified tool to collect all necessary version information from a configuration file, user
defined parameters, version control systems (e.g. Git) or environment variables. Especially the latter ones can be
tricky in CI environments, as every CI service uses different environment variables.

.. topic:: Planned features

   * read template from ``STDIN``.
   * add VHDL example

Use Cases
*********

* Integrate version information from e.g. Git, GitHub, GitLab, ... into current software builds.

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
* C++
* VHDL


Examples
********

* ANSI C Example
* C++ Example
* VHDL Example


.. _CONTRIBUTORS:

Contributors
************

* `Patrick Lehmann <https://GitHub.com/Paebbels>`__ (Maintainer)
* `Navid Jalali <https://GitHub.com/navidcity>`__
* `and more... <https://GitHub.com/Paebbels/pyVersioning/graphs/contributors>`__


.. _LICENSE:

License
*******

This Python package (source code) is licensed under :ref:`Apache License 2.0 <CODELICENSE>`. |br|
The accompanying documentation is licensed under :ref:`Creative Commons - Attribution 4.0 (CC-BY 4.0) <DOCLICENSE>`.


.. toctree::
   :caption: Overview
   :hidden:

   News
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
   ConfigurationFile

.. toctree::
   :caption: Templates
   :hidden:

   Templates/index
   Templates/C
   Templates/CXX

.. toctree::
   :caption: Examples
   :hidden:

   Examples/C
   Examples/CXX
   Examples/VHDL

.. raw:: latex

   \part{References and Reports}

.. toctree::
   :caption: References and Reports
   :hidden:

   CommandLineInterface
   Python Class Reference <pyVersioning/pyVersioning>
   unittests/index
   coverage/index
   Doc. Coverage Report <doccoverage/index>
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
