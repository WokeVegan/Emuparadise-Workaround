emu-dl
====

emu-dl is a command-line tool that allows you to search and download roms from emuparadise.

Requirements
------------
* Python version 3.x: https://www.python.org
    * requests

Installing requests
-------------------
.. code-block:: text

    $ pip install requests

Example
-------
* searching

.. code-block:: text

    $ python emu-dl.py -s "shrek super slam"
    https://emuparadise.me//Nintendo_DS_ROMs/Shrek_-_Super_Slam_(E)(Legacy)/46252
    https://emuparadise.me//Nintendo_DS_ROMs/Shrek_-_Super_Slam_(U)(Mode_7)/46212
    https://emuparadise.me//Nintendo_Gameboy_Advance_ROMs/Shrek_SuperSlam_(E)(Rising_Sun)/45474
    https://emuparadise.me//Nintendo_Gameboy_Advance_ROMs/Shrek_SuperSlam_(U)(Trashman)/45462
    https://emuparadise.me//Nintendo_Gamecube_ISOs/DreamWorks_Shrek_-_SuperSlam_(Europe)/181769
    https://emuparadise.me//Nintendo_Gamecube_ISOs/DreamWorks_Shrek_-_SuperSlam_(Europe)_(En,Fr,Es,It)/181770
    https://emuparadise.me//Nintendo_Gamecube_ISOs/DreamWorks_Shrek_-_SuperSlam_(Germany)/181771
    https://emuparadise.me//Nintendo_Gamecube_ISOs/Shrek_SuperSlam/66350
    https://emuparadise.me//Sony_Playstation_2_ISOs/DreamWorks_Shrek_-_SuperSlam_(Europe)/153130
    https://emuparadise.me//Sony_Playstation_2_ISOs/DreamWorks_Shrek_-_SuperSlam_(Europe)_(Fr,Es,It,Nl)/153131


* downloading

.. code-block:: text

    $ python emu-dl.py -d "https://emuparadise.me//Nintendo_Gamecube_ISOs/Shrek_SuperSlam/66350"
    downloading 'Shrek SuperSlam (USA).7z'
    00:01:30 100%[==============================] 1.33GB ETA 00:00:00
    file saved to '/home/user/emu-dl/Shrek SuperSlam (USA).7z'
