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
* Searching

.. code-block:: text

    $ python emu-dl.py search --keywords shrek super slam
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


* Downloading

.. code-block:: text

    $ python emu-dl.py download --url "https://emuparadise.me//Nintendo_Gamecube_ISOs/Shrek_SuperSlam/66350" --directory '/home/user/roms'
    downloading 'Shrek SuperSlam (USA).7z'
    00:01:30 100%[==============================] 1.33GB ETA 00:00:00 14.73MB/s
    file saved to '/home/nrp/roms/Shrek SuperSlam (USA).7z'


* Batch Downloading

.. code-block:: text

    $ python emu-dl.py download --batch shrek super slam --directory '/home/user/roms'
    downloading '0181 - Shrek - Super Slam (E)(Legacy).7z'
    00:00:00 100%[==============================] 12.74MB ETA 00:00:00 13.85MB/s
    file saved to '/home/user/roms/0181 - Shrek - Super Slam (E)(Legacy).7z'
    downloading '0141 - Shrek - Super Slam (U)(Mode 7).7z'
    00:00:00 100%[==============================] 12.75MB ETA 00:00:00 13.69MB/s
    file saved to '/home/user/roms/0141 - Shrek - Super Slam (U)(Mode 7).7z'
    downloading '2236 - Shrek SuperSlam (E)(Rising Sun).zip'
    00:00:00 100%[==============================] 6.71MB ETA 00:00:00 12.50MB/s
    file saved to '/home/user/roms/2236 - Shrek SuperSlam (E)(Rising Sun).zip'
    downloading '2224 - Shrek SuperSlam (U)(Trashman).zip'
    00:00:00 100%[==============================] 6.62MB ETA 00:00:00 12.59MB/s
    file saved to '/home/user/roms/2224 - Shrek SuperSlam (U)(Trashman).zip'
    downloading 'DreamWorks Shrek - SuperSlam (Europe).7z'
    00:00:30 033%[==========                    ] 1.33GB ETA 00:00:59 14.78MB/s
