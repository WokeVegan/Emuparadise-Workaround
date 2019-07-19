======================
Emuparadise Workaround
======================

Emuparadise Workaround is exactly what is sounds like. It is a command-line tool written in Python that allows you to
install games from Emuparadise.

Installing Python and Requests
******************************
Before running this script you must have installed Python 3.6+ and the requests library. You can download Python at
`python.org <https://www.python.org/downloads/>`_

If you don't already have pip, make sure to install it through the Python installer.

After Python and pip are installed, you can run the following command in a terminal to install requests.

.. code-block:: text

    pip install requests

Commands
********

- Setting the default download directory.

    .. code-block:: text
        
        python emuw.py -d /some/path [optional platform]

    Whenever you download a ROM, it will be saved to this path.

- Searching for games.

    .. code-block:: text

        python emuw.py search [-p] keywords [...]


    **Positional Arguments**

    -keywords  Keywords to search for.

    **Optional Arguments**

    -p, --platform  Shows the platform next to each ROM.


- Downloading Games

    .. code-block:: text

        python emuw.py download [-d] [-e] id


    **Positional Arguments**

    -id  ID of the ROM provided from the search command.

    **Optional Arguments**

    -d, --directory  The ROMs save directory. (overrides default directory)

    -e, --extract  Attempt to extract the zip file.

