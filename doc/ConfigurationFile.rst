.. _CONFIG:

Configuration File
##################

:file:`.pyVersioning.yaml`

.. card:: .pyVersioning.yaml

   .. code-block:: YAML

      version: 1

      project:
        name:     Test Project
        variant:  A2
        version:  v2.1.6

      build:
        compiler:
          name:           gcc
          version:        10.2.0
          configuration:  Release
          options:        -g -O3
