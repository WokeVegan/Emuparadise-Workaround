Emuparadise Workaround
====

Emuparadise Workaround is a command-line tool that allows you to search and download roms from emuparadise.

Requirements
------------
* Python version 3.x: https://www.python.org
    * argparse

Installing argparse
-------------------
.. code-block:: text

    $ pip install argparse

Example
-------
* searching

.. code-block:: text

    $ python emuw.py -s "shrek super slam"
    https://emuparadise.me//Nintendo_Gamecube_ISOs/DreamWorks_Shrek_-_SuperSlam_(Europe)/181769
    https://emuparadise.me//Nintendo_Gamecube_ISOs/DreamWorks_Shrek_-_SuperSlam_(Europe)_(En,Fr,Es,It)/181770
    https://emuparadise.me//Nintendo_Gamecube_ISOs/DreamWorks_Shrek_-_SuperSlam_(Germany)/181771
    https://emuparadise.me//Nintendo_Gamecube_ISOs/Shrek_SuperSlam/66350
    https://emuparadise.me//Sony_Playstation_2_ISOs/DreamWorks_Shrek_-_SuperSlam_(Europe)/153130
    https://emuparadise.me//Sony_Playstation_2_ISOs/DreamWorks_Shrek_-_SuperSlam_(Europe)_(Fr,Es,It,Nl)/153131
    https://emuparadise.me//Nintendo_DS_ROMs/Shrek_-_Super_Slam_(E)(Legacy)/46252
    https://emuparadise.me//Nintendo_DS_ROMs/Shrek_-_Super_Slam_(U)(Mode_7)/46212
    https://emuparadise.me//Nintendo_Gameboy_Advance_ROMs/Shrek_SuperSlam_(E)(Rising_Sun)/45474
    https://emuparadise.me//Nintendo_Gameboy_Advance_ROMs/Shrek_SuperSlam_(U)(Trashman)/45462

* downloading

.. code-block:: text

    $ python emuw -d "https://emuparadise.me//Nintendo_Gamecube_ISOs/Shrek_SuperSlam/66350"
    1267.00MB / 1267.00MB    100%
    file saved to 'Shrek SuperSlam (USA).7z'
