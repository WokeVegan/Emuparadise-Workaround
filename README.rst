======================
Emuparadise Workaround
======================

Emuparadise Workaround is a command-line tool written in Python that allows you to install games from Emuparadise.

Requirements
************
- Python 3.6+

- Python Packages

    - Required

        - **requests**
        - **bs4**

    - Optional

        - **libarchive** - Allows you to extract .7z files.

Commands
********

- Setting the default download directory.

    .. code-block:: text
        
        python emuw.py -d /some/path optional_platform

    Whenever you download a ROM it will be saved to this path. If you provide a specific platform after the path, all games for that platform will be saved in that directory.

- Searching for games.

    .. code-block:: text

        python emuw.py search [-p] [keywords ...]


    **Positional Arguments**

    -keywords  A list of keywords to search for.

    **Optional Arguments**

    -p, --platform  Display the platform next to each game.

    This will list all matches found in the database with their IDs. If you use -p, their platforms will be listed as well.


- Downloading Games

    .. code-block:: text

        python emuw.py download [-d] [-e] [-s] [id ...]


    **Positional Arguments**

    -id  ID of the ROM/ROMs provided from the search command.

    **Optional Arguments**

    -d, --directory  The ROMs save directory. (overrides default directory)

    -e, --extract  Attempt to extract the contents after downloading.

    -c, --chunk-size  Changes chunk size for downloads. (default: 1048576)

    This downloads the specified game. You can choose to install it in a specific directory or extract the files.


- Queue

    This allows you to add games to a queue then download them all at once.

    **Optional Arguments**

    -a, --append  Adds all the IDs listed to the queue. This won't add duplicate entries or IDs of games that don't
        exist.

    -r, --remove  Removes the listed IDs from the queue.

    -c, --clear  Clears the queue.

    -l, --list  Lists all the titles in the queue.

    -d, --download  Starts downloading all the games in the queue. This will automatically remove it from the queue
        after the download is finished.
