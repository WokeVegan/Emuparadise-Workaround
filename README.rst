emu_workaround
====

emu_workaround is a command-line tool written in python3 that allows you to search and download roms from emuparadise.

Example
-------

searching...
.. code-block:: text

    $ python emuw.py -s "emu_workaround"
    https://github.com/WokeVegan/emu_workaround
    https://github.com/WokeVegan/emu_workaround
    https://github.com/WokeVegan/emu_workaround

downloading
.. code-block:: text

    $ python emuw.py -d "https://github.com/WokeVegan/emu_workaround"
    120.00MB / 120.00MB    100%
    file saved to 'emu_workaround.rar'
    $ python emuw.py -d "https://github.com/WokeVegan/emu_workaround"
    'emu_workaround.rar' already exists

