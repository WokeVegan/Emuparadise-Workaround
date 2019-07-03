emu-dl
====

emu-dl is a command-line tool that allows you to search and download roms from emuparadise.

Requirements
------------
* Python version 3.6: https://www.python.org
    * requests

Installing requests
-------------------
.. code-block:: text

    $ pip install requests


Commands
----
usage: emu-dl.py [-h] [-d DEFAULT_ROM_DIRECTORY] {search,download} ...

optional arguments:
  -d, --default-rom-directory 
                        Sets the default directory ROMs will be saved to.

search arguments:
  -k, --keywords        Keywords to search for.
  --platform            Shows the platform next to each ROM.
  --strict              Search results will be more picky.

download arguments:
  -i, --id              ID of the rom you wish to download.
  -d, --directory       Directory the ROM will be saved to. This overrides the default download directory.




Examples
-------
* Setting the default download directory.

.. code-block:: text

    $ python emu-dl.py -d /path/to/directory


* Searching for games

.. code-block:: text

    $ python emu-dl.py search -k shrek super slam


You can type the following while searching to find closer matches.

.. code-block:: text

    $ python emu-dl.py search -k shrek super slam --strict


You can also display the games platform.

.. code-block:: text

    $ python emu-dl.py search -k shrek super slam --strict --platform



* Downloading
To download games, simply use the download command and paste the game id in the brackets provided from the search function.

.. code-block:: text

    $ python emu-dl.py download -i 66350


You can type the following command to override the default download path.

  
.. code-block:: text    

    $ python emu-dl.py download -i xxx -d /some/other/path

