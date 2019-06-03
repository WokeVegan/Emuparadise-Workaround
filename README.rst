Emuparadise Workaround
====

Emuparadise Workaround is a command-line tool that allows you to search and download roms from emuparadise.

Requirements
-------
* Python version 3.x: https://www.python.org
    * argparse
.. code-block:: text

    pip install argparse

Example
-------
* searching

.. code-block:: text

    $ python emuw.py -s "emu_workaround"
    https://github.com/WokeVegan/emu_workaround
    https://github.com/WokeVegan/emu_workaround/blob/master/LICENSE
    https://github.com/WokeVegan/emu_workaround/blob/master/README.rst

* downloading

.. code-block:: text

    $ python emuw.py -d "https://github.com/WokeVegan/emu_workaround/blob/master/README.rst"
    120.00MB / 120.00MB    100%
    file saved to 'README.rst'
    $ python emuw.py -d "https://github.com/WokeVegan/emu_workaround/blob/master/README.rst"
    'README.rst' already exists

