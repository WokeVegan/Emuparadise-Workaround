#!/usr/bin/env python3

import os
import shutil
import urllib.parse
import time
import requests

from src import path

try:
    import libarchive.public
    IMPORTED_LIBARCHIVE = True
except ModuleNotFoundError:
    IMPORTED_LIBARCHIVE = False


_DEFAULT_COLOR = "\033[0;32;37m"
_GREY = "\033[2;32;37m"
_BLUE = "\033[1;32;34m"
_OCCUPIED_SPACE = 38
_BAD_FILENAME = "get-download.php?gid=%s&test=true"
_GAME_LINK = "https://www.emuparadise.me/roms/get-download.php?gid=%s&test=true"
_SIZES = {1000000000: "{:1.2f}GB", 1000000: "{0:02.2f}MB", 1000: "{:06.2f}KB", 0: "{:02d}B"}
_IMAGE_DATABASE_URL = "https://r.mprd.se/media/images"
_EMUPARADISE_URL = "https://www.emuparadise.me"
_PLATFORM_NAMES = {
    'abandonware': 'Abandonware_Games',
    'acorn archimedes': 'Acorn_Archimedes_ROMs',
    'acorn bbc micro': 'Acorn_BBC_Micro_ROMs',
    'acorn electron': 'Acorn_Electron_ROMs',
    'amiga cd': 'Amiga_CD_ISOs',
    'amiga cd32': 'Amiga_CD32_ISOs',
    'amstrad cpc': 'Amstrad_CPC_ROMs',
    'apple ii': 'Apple_][_ROMs',
    'atari 2600': 'Atari_2600_ROMs',
    'atari 5200': 'Atari_5200_ROMs',
    'atari 7800': 'Atari_7800_ROMs',
    'atari 8-bit family': 'Atari_8-bit_Family_ROMs',
    'atari jaguar': 'Atari_Jaguar_ROMs',
    'atari lynx': 'Atari_Lynx_ROMs',
    'bandai playdia': 'Bandai_Playdia_ISOs',
    'bandai wonderswan': 'Bandai_Wonderswan_ROMs',
    'bandai wonderswan color': 'Bandai_Wonderswan_Color_ROMs',
    'capcom play system 1': 'Capcom_Play_System_1_ROMs',
    'capcom play system 2': 'Capcom_Play_System_2_ROMs',
    'capcom play system 3': 'Capcom_Play_System_3_ROMs',
    'commodore 64 (tapes)': 'Commodore_64_(Tapes)_ROMs',
    'commodore 64 preservation project': 'Commodore_64_Preservation_Project_ROMs',
    'game boy': 'Nintendo_Game_Boy_ROMs',
    'game boy advance': 'Nintendo_Gameboy_Advance_ROMs',
    'game boy color': 'Nintendo_Game_Boy_Color_ROMs',
    'nintendo entertainment system': 'Nintendo_Entertainment_System_ROMs',
    'neo geo': 'Neo_Geo_ROMs',
    'neo geo pocket - neo geo pocket color (ngpx)': 'Neo_Geo_Pocket_-_Neo_Geo_Pocket_Color_(NGPx)_ROMs',
    'nintendo 64': 'Nintendo_64_ROMs',
    'nintendo ds': 'Nintendo_DS_ROMs',
    'nintendo famicom disk system': 'Nintendo_Famicom_Disk_System_ROMs',
    'gamecube': 'Nintendo_Gamecube_ISOs',
    'nokia n-gage': 'Nokia_N-Gage_ROMs',
    'pc engine - turbografx16': 'PC_Engine_-_TurboGrafx16_ROMs',
    'pc engine cd - turbo duo - turbografx cd': 'PC_Engine_CD_-_Turbo_Duo_-_TurboGrafx_CD_ISOs',
    'pc-fx': 'PC-FX_ISOs',
    'psx on psp': 'PSX_on_PSP_ISOs',
    'panasonic 3do (3do interactive multiplayer)': 'Panasonic_3DO_(3DO_Interactive_Multiplayer)_ISOs',
    'philips cd-i': 'Philips_CD-i_ISOs',
    'snes': 'Super_Nintendo_Entertainment_System_(SNES)_ROMs',
    'scummvm': 'ScummVM_Games',
    'sega 32x': 'Sega_32X_ROMs',
    'sega cd': 'Sega_CD_ISOs',
    'sega game gear': 'Sega_Game_Gear_ROMs',
    'sega genesis - sega megadrive': 'Sega_Genesis_-_Sega_Megadrive_ROMs',
    'sega master system': 'Sega_Master_System_ROMs',
    'sega naomi': 'Sega_NAOMI_ROMs',
    'sega saturn': 'Sega_Saturn_ISOs',
    'sharp x68000': 'Sharp_X68000_ROMs',
    'sony playstation': 'Sony_Playstation_ISOs',
    'sony playstation - demos': 'Sony_Playstation_-_Demos_ISOs',
    'sony playstation 2': 'Sony_Playstation_2_ISOs',
    'sony pocketstation': 'Sony_PocketStation_ROMs',
    'sony psp': 'PSP_ISOs',
    'virtual boy': 'Nintendo_Virtual_Boy_ROMs',
    'zx spectrum (tapes)': 'ZX_Spectrum_(Tapes)_ROMs',
    'zx spectrum (z80)': 'X_Spectrum_(Z80)_ROMs'
}


def unpack(filename, directory):
    """ unpacks archive files """
    file_path = os.path.join(directory, filename)
    folder_name = os.path.splitext(filename)[0]
    folder_path = os.path.join(directory, folder_name)

    if not os.path.exists(folder_path):
        os.mkdir(folder_path)

    if IMPORTED_LIBARCHIVE:
        with libarchive.public.file_reader(file_path) as e:
            for entry in e:
                current_size = 0
                total_size = entry.size
                filename = os.path.join(folder_path, entry.pathname)
                start_time = time.time()
                print(f"\nExtracting '{os.path.split(filename)[-1]}'.")

                with open(filename, 'wb') as f:
                    for block in entry.get_blocks():
                        f.write(block)
                        current_size += len(block)
                        progress_bar = get_progress_bar(current_size, total_size, start_time)
                        print(progress_bar, end="")
                    f.close()
            print(f"\nAll files extracted to '{folder_path}'.")
    else:
        try:
            shutil.unpack_archive(filename, directory)
        except shutil.ReadError:
            extension = os.path.splitext(file_path)[1]
            print(f"Cannot unpack '{extension}' files. Try installing libarchive.")


def get_progress_bar(current_download, total_download, start_time):
    """ returns progress bar based on terminal width """
    terminal_width = os.get_terminal_size()[0]
    download_percentage = current_download / total_download * 100
    percentage_formatted = "%03d" % int(download_percentage)
    time_elapsed = time.strftime("%H:%M:%S", time.gmtime(time.time() - start_time))
    size = get_size_label(total_download)
    current_time = time.gmtime(int(((time.time() - start_time) / download_percentage) * (100 - download_percentage)))
    eta = f"ETA {time.strftime('%H:%M:%S', current_time)}"
    progress_bar_width = terminal_width - _OCCUPIED_SPACE
    percentage = int(current_download / total_download * progress_bar_width)
    bar = f"[{'=' * percentage}{' ' * (progress_bar_width - percentage)}]"
    return f"\r{time_elapsed} {percentage_formatted}% {bar} {size} {eta}"


def get_size_label(size):
    """ returns a prettier size label """
    for key, value in _SIZES.items():
        if size >= key:
            try:
                return value.format(size / key)
            except ZeroDivisionError:
                return value.format(size)


def check_bad_id(filename, gid):
    """ exit if download link is bad """
    if filename == _BAD_FILENAME % gid:
        print("Failed to download due to bad ID.")
        raise SystemExit


def get_platform_by_gid(gid):
    """ search for gid in database and return the platform it's contained in """
    for filename in os.listdir(path.DATABASE_PATH):
        name, extension = os.path.splitext(filename)
        current_platform = name.lower()
        with open(os.path.join(path.DATABASE_PATH, filename), 'r') as f:
            for x in f.readlines():
                if int(gid) == int(x.split('/')[0]):
                    return current_platform
            f.close()
    return None


def get_title_by_gid(gid):
    """ search for gid in database and return the platform it's contained in """
    for filename in os.listdir(path.DATABASE_PATH):
        with open(os.path.join(path.DATABASE_PATH, filename), 'r') as f:
            for x in f.readlines():
                if int(gid) == int(x.split('/')[0]):
                    return x.split('/')[1]
            f.close()
    return None


def download(gid, directory=None, extract=False):
    """ attempt to download rom """
    if not directory:
        directory = path.get_default_directory(get_platform_by_gid(gid))

    response = requests.get(_GAME_LINK % gid, headers={"referer": _GAME_LINK % gid}, stream=True)
    decoded_url = urllib.parse.unquote(response.url)
    filename = decoded_url.split('/')[-1]
    download_path = os.path.join(directory, filename)
    check_bad_id(filename, gid)

    install = True

    if os.path.exists(download_path):
        question = f"'{os.path.abspath(download_path)}' already exists.\nOverwrite the file? [y/n] "
        overwrite = input(question)
        if overwrite.lower() != 'y':
            install = False

    if not os.path.isdir(directory):
        question = f"'{directory}' doesnt exists yet.\nCreate the directory? [y/n] "
        create_dir = input(question)
        if create_dir.lower() == 'y':
            os.makedirs(directory)
        else:
            install = False

    if install:
        print("\nDownloading '%s'." % filename)
        start_time = time.time()
        total_size = int(response.headers.get('content-length'))
        current_size = 0

        with open(download_path, 'wb') as f:
            for block in response.iter_content(1024**2):
                f.write(block)
                current_size += len(block)
                progress_bar = get_progress_bar(current_size, total_size, start_time)
                print(progress_bar, end="")
            f.close()
            print("\nFile saved to '%s'." % os.path.abspath(download_path))

        if extract:
            unpack(download_path, directory)


def search(keywords, show_platform=False):
    """ prints all matching games """
    database = []
    for platform in os.listdir(path.DATABASE_PATH):
        with open(os.path.join(path.DATABASE_PATH, platform), encoding='utf-8') as f:
            for x in f.readlines():
                line = x.strip('\n')
                platform_string = platform.strip('.txt')
                database.append(f"{platform_string}/{line}")

    matches = sorted([x for x in database if all([key.lower() in x.lower() for key in keywords])])

    print(f"\n{len(matches)} results found...\n")

    for game in matches:
        platform, gid, title = game.split('/')
        gid = f"{_BLUE}{' ' * (6 - len(gid))}{gid}{_DEFAULT_COLOR}"
        platform = f"{_GREY}{platform}{_DEFAULT_COLOR}"

        if show_platform:
            print(f"{gid}[{platform}] {title}")
        else:
            print(f"{gid} {title}")
