======================
Emuparadise Workaround
======================

Emuparadise Workaround is a command-line tool written in Python that allows you to install games from Emuparadise.

Requirements
************
- Python 3.6+
- See requirements.txt for required python packages
- 7zip (optional); if you have 7zip installed, you can extract .7z files with -e

Commands
********

- Setting the default download directory.

    .. code-block:: text
        
        python emuw.py -d /some/path optional_platform

    Whenever you download a ROM it will be saved to this path. If you provide a specific platform after the path, all games for that platform will be saved in that directory.

- Searching for games.

    .. code-block:: text

        python emuw.py search [-p] keywords [...]


    **Positional Arguments**

    -keywords  A list of keywords to search for.

    **Optional Arguments**

    -p, --platform  Display the platform next to each game.


- Downloading Games

    .. code-block:: text

        python emuw.py download [-d] [-e] [-s] id


    **Positional Arguments**

    -id  ID of the ROM provided from the search command.

    **Optional Arguments**

    -d, --directory  The ROMs save directory. (overrides default directory)

    -e, --extract  Attempt to extract the contents after downloading.

    -s, --scrap  Scrap user uploaded images of game.
