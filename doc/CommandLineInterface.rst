Command Line Interfaces
#######################

When installed via PIP, the command line program ``pyVersioning`` is registered in the Python installation's ``Scripts``
directory. Usually this path is listed in ``PATH``, thus this program is globally available after installation.

The program is self-describing. Use ``pyVersioning`` without parameters or ``pyVersioning help`` to see all available
common options and commands. Each command has then it's own help page for command specific options, which can be listed
by calling ``pyVersioning <cmd> -h`` or ``pyVersioning help <cmd>``. The ``pyVersioning``'s version and license
information is shown by calling ``pyVersioning version``.

.. _References:cli:

.. autoprogram:: pyVersioning.CLI:Application().MainParser
  :prog: pyVersioning
  :groups:
