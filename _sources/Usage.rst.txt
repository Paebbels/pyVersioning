.. _USAGE:

Usage
#####

pyVersioning collects various information from the build environment and provides the collected information as
structured field. These fields can be queried individually or can be used with a template to fillout and generate a
source file. This source file can then be used in a normal build flow by the compiler.

.. rubric:: Collected Information

* Platform
* Environment variables
* Version Control System information (e.g. commit hash, branch, tag)
* Static data from configuration file
* Static data from command line arguments



.. _USAGE/variables:

List all variables
******************

.. code-block:: bash

   pyVersioning variables


.. _USAGE/field:

Get single field
****************

.. code-block:: bash

   pyVersioning field git.commit.date


.. _USAGE/fillout:

Fillout a template
******************

.. code-block:: bash

   pyVersioning fillout versioning.c.template versioning.c


.. _USAGE/yaml:

Write all collected data as YAML
********************************

.. code-block:: bash

   pyVersioning yaml


.. _USAGE/json:

Write all collected data as JSON
********************************

.. code-block:: bash

   pyVersioning json
