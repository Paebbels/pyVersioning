.. _NEWS:

News
####

See :gh:`pyVersioning Release Pages <Paebbels/pyVersioning/releases>` for detail release notes on every release.


Version 0.19.0 (2026)
*********************

.. topic:: :gh:`v0.19.0 - unreleased <Paebbels/pyVersioning/releases/v0.19.0>`

   .. rubric:: Breaking Changes

   * ⚠️ Derived exceptions end in ``Error``: ``ServiceException`` |rarr|
     :exc:`~pyVersioning.CIService.ServiceError`, ``ToolException`` |rarr| :exc:`~pyVersioning.ToolError`. The root
     :exc:`~pyVersioning.VersioningException` keeps its name. The old names are gone, not kept as aliases.

   .. rubric:: Changes

   * pyTooling 10.1 is required; Python 3.11 to 3.15 are supported.

   .. rubric:: Documentation

   * The documentation is built with pyTooling.Sphinx instead of sphinx-reports: dependency tables, badges, and report
     pages per testsuite, source file and module.

   .. rubric:: CI Pipeline

   * Pipeline on pyTooling/Actions ``@r9``, tested with Python 3.11 to 3.15. A release is checked for a matching version
     and a version not yet on PyPI; only the wheel is published on PyPI.
