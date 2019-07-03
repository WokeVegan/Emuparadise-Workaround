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
    The default download directory has been set to '/path/to/directory'.


* Searching for games
A list of games and their [game id's] will be listed while searching.

.. code-block:: text

    $ python emu-dl.py search -k shrek super slam
    
    10 results found...

    [46252] Shrek - Super Slam (E)(Legacy)
    [46212] Shrek - Super Slam (U)(Mode 7)
    [45474] Shrek SuperSlam (E)(Rising Sun)
    [45462] Shrek SuperSlam (U)(Trashman)
    [181770] DreamWorks Shrek - SuperSlam (Europe) (En,Fr,Es,It)
    [181769] DreamWorks Shrek - SuperSlam (Europe)
    [181771] DreamWorks Shrek - SuperSlam (Germany)
    [66350] Shrek SuperSlam
    [153131] DreamWorks Shrek - SuperSlam (Europe) (Fr,Es,It,Nl)
    [153130] DreamWorks Shrek - SuperSlam (Europe)


You can type the following while searching to find closer matches.

.. code-block:: text

    $ python emu-dl.py search -k shrek super slam --strict

    2 results found...

    [46212] Shrek - Super Slam (U)(Mode 7)
    [46252] Shrek - Super Slam (E)(Legacy)


You can also display the games platform.

.. code-block:: text

    $ python emu-dl.py search -k shrek super slam --strict --platform

    2 results found...

    [46212][Nintendo DS] Shrek - Super Slam (U)(Mode 7)
    [46252][Nintendo DS] Shrek - Super Slam (E)(Legacy)



* Downloading
To download games, simply use the download command and paste the game id in the brackets provided from the search function.

.. code-block:: text

    $ python emu-dl.py download -i 66350
    Downloading 'Shrek SuperSlam (USA).7z'.
    00:01:30 100% [==============================] 1.33GB ETA 00:00:00   14.69MB/s
    File saved to '/path/to/directory/Shrek SuperSlam (USA).7z'.


You can type the following command to override the default download path.

  
.. code-block:: text    

    $ python emu-dl.py download -i xxx -d /some/other/path




