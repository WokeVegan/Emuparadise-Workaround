============
emu-dl
============
emu-dl is a command line tool written in python that allows you to install games from Emuparadise.

Installing Python and Requests
******************************
Before running this script you must have installed Python 3.6+ and the requests library.
`python.org <https://www.python.org/downloads/>`_

Before you can install requests, you need to install pip though the Python installer.

After Python and pip are installed, you can run the following command in a terminal to install requests.

.. code-block:: text

    $ pip install requests

Now that you've installed Python and requests, you can use the script.

Commands
********

- Setting the Default Path

    .. code-block:: text
        
        $ python emu-dl.py -d ...

    Whenever you download a ROM, it will be saved to this path.

- Searching for Games

    **Required Arguments**

    -k, --keywords  Keywords to search for.

    **Optional Arguments**

    --platform      Shows the platform next to each ROM.

    .. code-block:: text

        $ python emu-dl.py search -k ... [--platform]
   
    This will list all matching games along with their ID.

- Downloading Games
    
    **Required Arguments**

    -i, --id  ID of the ROM you wish to download.

    **Optional Arguments**

    -d, --directory  Directory the ROM will be saved to. This overrides the default download directory.

    .. code-block:: text

        $ python emu-dl.py download -i ... [--directory]

    You can get the ID from the search command.

Examples
********
- Setting the Default Path

    .. code-block:: text
        
        $ python emu-dl.py -d /path/to/directory
        The default download directory has been set to '/path/to/directory'.

- Searching

    .. code-block:: text

        $ python emu-dl.py search -k shrek super slam
    
        10 results found...

        46252   Shrek - Super Slam (E)(Legacy)
        46212   Shrek - Super Slam (U)(Mode 7)
        45474   Shrek SuperSlam (E)(Rising Sun)
        45462   Shrek SuperSlam (U)(Trashman)
        181770  DreamWorks Shrek - SuperSlam (Europe) (En,Fr,Es,It)
        181769  DreamWorks Shrek - SuperSlam (Europe)
        181771  DreamWorks Shrek - SuperSlam (Germany)
        66350   Shrek SuperSlam
        153131  DreamWorks Shrek - SuperSlam (Europe) (Fr,Es,It,Nl)
        153130  DreamWorks Shrek - SuperSlam (Europe)

    .. code-block:: text

        [$ python emu-dl.py search -k shrek super slam --platform

        10 results found...

        45462	Game Boy Advance Shrek SuperSlam (U)(Trashman)
        45474	Game Boy Advance Shrek SuperSlam (E)(Rising Sun)
        46212	Nintendo DS Shrek - Super Slam (U)(Mode 7)
        46252	Nintendo DS Shrek - Super Slam (E)(Legacy)
        181769	Nintendo Gamecube DreamWorks Shrek - SuperSlam (Europe)
        181770	Nintendo Gamecube DreamWorks Shrek - SuperSlam (Europe) (En,Fr,Es,It)
        181771	Nintendo Gamecube DreamWorks Shrek - SuperSlam (Germany)
        66350	Nintendo Gamecube Shrek SuperSlam
        153130	Sony Playstation 2 DreamWorks Shrek - SuperSlam (Europe)
        153131	Sony Playstation 2 DreamWorks Shrek - SuperSlam (Europe) (Fr,Es,It,Nl)


- Downloading

    .. code-block:: text
    
        $ python emu-dl.py download -i 66350
        Downloading 'Shrek SuperSlam (USA).7z'.
        00:01:29 100% [==============================] 1.33GB ETA 00:00:00   14.89MB/s
        File saved to '/path/to/directory/Shrek SuperSlam (USA).7z'.
 
