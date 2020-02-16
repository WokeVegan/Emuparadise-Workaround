Requirements
************
- Python 3.6+

- Python Packages
    - **requests**
    - **bs4**


Commands
********

- Setting the default download directory.

    .. code-block:: text

        > python emuw.py -d /some/path
        Directory for 'default' has been set to '/some/path'.

        > python emuw.py -d /different/path "game boy advance"
        Directory for 'game boy advance' has been set to '/different/path'.

    This sets the default download path. If you provide a specific platform after the path,
    games for that platform will be saved in that directory.

    If you want to see all custom directories you've set, you can use the --list-directories command.

    .. code-block:: text

        > python emuw.py --list-directories
        default = /some/path
        game boy advance = /different/path

- Searching for games.

    .. code-block:: text

        > python emuw.py search shrek super slam (u) --platforms

        2 results found...

         45462 [Game Boy Advance] Shrek SuperSlam (U)(Trashman)
         46212 [Nintendo DS] Shrek - Super Slam (U)(Mode 7)

    If you add the --platforms argument, each games platform will be shown.


- Downloading Games

    .. code-block:: text

        > python emuw.py download id [option arguments ...]

    Replace id with the id of a game provided from the search command.

    **Optional Arguments**

     --directory  A directory you want to save the game to. (overrides default directory)

- Queue

    This allows you to add games to a queue then download them all at once.

    .. code-block:: text

        > python emuw.py queue --add 45462 46212
        Added Shrek SuperSlam (U)(Trashman) to queue.
        Added Shrek - Super Slam (U)(Mode 7) to queue.

        > python emuw.py queue --list
         46212  Shrek - Super Slam (U)(Mode 7)

        Downloading '2224 - Shrek SuperSlam (U)(Trashman).zip'.
        00:00:00 100% [==========================] 6.62MB ETA 00:00:00
        File saved to './2224 - Shrek SuperSlam (U)(Trashman).zip'.
        Removed Shrek SuperSlam (U)(Trashman) from the queue.

        > python emuw.py queue --download
        Downloading '0141 - Shrek - Super Slam (U)(Mode 7).7z'.
        00:00:01 100% [==========================] 12.75MB ETA 00:00:00
        File saved to 'another/path/0141 - Shrek - Super Slam (U)(Mode 7).7z'.
        Removed Shrek - Super Slam (U)(Mode 7) from the queue.


    **Optional Arguments**

    --add  Adds all the IDs listed to the queue. This won't add duplicate entries or IDs of games that don't
        exist.
    --remove  This will remove any amount of games from the queue if you provide their ID.
    --clear  Clears all games from the queue.
    --list  Lists all the titles in the queue.
    --download  Starts downloading all the games in the queue. This will automatically remove games from the queue
        after they're finished downloading.
