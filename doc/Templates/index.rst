.. _TEMPLATES:

Writing Templates
#################

.. _TEMPLATES/Syntax:

Syntax
******

The used template format is based on Python's :meth:`str.format` method. Thus a list of predefined variables can be
embedded into a text using ``{myVariable}`` syntax. As curley braces are used to denote variables, double curley
braces will translate to curley braces in the output text, e.g. needed in C-like languages: ``{{`` |rarr| ``{`` or
``}}`` |rarr| ``}``.

.. card:: myTemplate.c.template

   .. code-block:: C

      typedef struct {{
        .field = "{myVariable}"
      }} myExample;

.. _TEMPLATES/Syntax/Member:

Member Access
=============

A variable's member (property or field) can be accessed using the dot-notation.

.. card:: myTemplate.c.template

   .. code-block:: C

      typedef struct {{
        .field = "{myVariable.myProperty}"
      }} myExample;

.. _TEMPLATES/Syntax/Method:

Method Access
=============

A variable's method can be accessed using the dot-notation.

.. card:: myTemplate.c.template

   .. code-block:: C

      typedef struct {{
        .field = "{myVariable.myMethod()}"
      }} myExample;

A typical usecase might be concatenating list elements to a comma separated string

.. card:: myTemplate.c.template

   .. code-block:: C

      typedef struct {{
        .field = "{', '.join(myVariable)}"
      }} myExample;


.. _TEMPLATES/Syntax/FunctionCall:

FunctionCall
============

A function can be called inside ``{.....}``

.. card:: myTemplate.c.template

   .. code-block:: C

      typedef struct {{
        .field = "{len(myArray)}"
      }} myExample;

.. _TEMPLATES/Syntax/Formatting:

Formatting
==========

The :ref:`Pyton string formating <string-formatting>` syntax allows for further :ref:`customizations <formatspec>` like left, middle or
right justification as well as number formating e.g. as hex-values.

.. rubric:: Examples

``{myVariable:\0<16}``
  Left justified 16-character string padded with ``\0``.
``0x{myVariable:02X}``
  Zero-padded 2-character hexadecimal number, with ``0x`` prefix and uppercase (``X``) hex-letters.
``{myVariable!s}``/``{myVariable!r}``
  Call :func:`str` or :func:`repr` on a variable.


.. _TEMPLATES/Variables:

Predefined Variables
********************

.. grid:: 2

   .. grid-item::
      :columns: 6

      *pyVersioning* offers lots of predefined variables. A full list of variables and there actual values can be
      printed using the :code:`pyVersioning variables` command in the command line interface.

      The following root-level variables are defined:

      ``version``
        Version information.
      ``git``
        Information collected from version control system Git like branch name, tag name, commit date, commit hash, ...
      ``project``
        Project information mainly provided by the :file:`.pyVersioning.yaml` configuration file.
      ``build``
        Build information mainly provided by the :file:`.pyVersioning.yaml` configuration file.
      ``tool``
        Tool information about pyVersioning.
      ``platform``
        Platform information.

      .. seealso::

         :ref:`USAGE/variables`

   .. grid-item::
      :columns: 6

      .. card:: Variables

         .. code-block:: text

            $> pyVersioning.exe variables
            version                 : v0.0.0
            tool                    : pyVersioning 0.17.0
              name                  : pyVersioning
              version               : 0.17.0
            project                 :  -  v0.0.0
              name                  :
              variant               :
              version               : v0.0.0
            build                   : <pyVersioning.Build object at 0x000001F3FF7F46C0>
              date                  : 2025-04-21
              time                  : 10:43:02.882194
              compiler              : <pyVersioning.Compiler object at 0x000001F3819B63E0>
                name                :
                version             : v0.0.0
                configuration       :
                options             :
            git                     : <pyVersioning.Git object at 0x000001F3819F5260>
              commit                : <pyVersioning.Commit object at 0x000001F3819DA920>
                hash                : 4f5b03b202887cab53ad27d80b0ed5bde028d705
                date                : 2025-04-21
                time                : 07:50:48
                author              : Patrick Lehmann <Paebbels@gmail.com>
                  name              : Patrick Lehmann
                  email             : Paebbels@gmail.com
                committer           : Patrick Lehmann <Paebbels@gmail.com>
                  name              : Patrick Lehmann
                  email             : Paebbels@gmail.com
                comment             : Fixed binary output check.

                oneline             : Fixed binary output check.
              reference             : dev
              tag                   :
              branch                : dev
              repository            : git@github.com:Paebbels/pyVersioning.git
            platform                : <pyVersioning.Platform object at 0x000001F3FF441510>
              ci_service            : NO-CI
            env                     : Environment(..........................)



.. _TEMPLATES/ConfigurationFile:

Configuration File Variables
============================

*pyVersioning* reads a :file:`.pyVersioning.yaml` file for static (per project) settings. These are also exposed as
variables.



.. _TEMPLATES/Environment:

Environment Variables
=====================

.. todo:: List environment variables.


.. _TEMPLATES/Git:

Git Variables
=============

.. _TEMPLATES/Git/Local:

Local Workstation
-----------------

.. todo:: List Git variables.



.. _TEMPLATES/Git/AppVeyor:

AppVayor
--------

.. todo:: List AppVayor variables.



.. _TEMPLATES/Git/GitHub:

GitHub
------

.. todo:: List GitHub variables.



.. _TEMPLATES/Git/GitLab:

GitLab
------

.. todo:: List GitLab variables.



.. _TEMPLATES/Git/TravisCI:

Travis-CI
---------

.. todo:: List Travis-CI variables.

