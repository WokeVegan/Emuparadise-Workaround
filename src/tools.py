#!/usr/bin/env python3

import os
import requests
import shutil
import urllib.parse
import time
import subprocess
import bs4

from src import path

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
    'nes': 'Nintendo_Entertainment_System_ROMs',
    'neo geo': 'Neo_Geo_ROMs',
    'neo geo pocket - neo geo pocket color (ngpx)': 'Neo_Geo_Pocket_-_Neo_Geo_Pocket_Color_(NGPx)_ROMs',
    'nintendo 64': 'Nintendo_64_ROMs',
    'nintendo ds': 'Nintendo_DS_ROMs',
    'nintendo famicom disk system': 'Nintendo_Famicom_Disk_System_ROMs',
    'nintendo gamecube': 'Nintendo_Gamecube_ISOs',
    'nokia n-gage': 'Nokia_N-Gage_ROMs',
    'pc engine - turbografx16': 'PC_Engine_-_TurboGrafx16_ROMs',
    'pc engine cd - turbo duo - turbografx cd': 'PC_Engine_CD_-_Turbo_Duo_-_TurboGrafx_CD_ISOs',
    'pc-fx': 'PC-FX_ISOs',
    'psp': 'PSP_ISOs',
    'psx on psp': 'PSX_on_PSP_ISOs',
    'panasonic 3do (3do interactive multiplayer)': 'Panasonic_3DO_(3DO_Interactive_Multiplayer)_ISOs',
    'philips cd-i': 'Philips_CD-i_ISOs',
    'playstation': 'Sony_Playstation_ISOs',
    'playstation 2': 'Sony_Playstation_2_ISOs',
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
    'sony playstation - demos': 'Sony_Playstation_-_Demos_ISOs',
    'sony pocketstation': 'Sony_PocketStation_ROMs',
    'virtual boy': 'Nintendo_Virtual_Boy_ROMs',
    'zx spectrum (tapes)': 'ZX_Spectrum_(Tapes)_ROMs',
    'zx spectrum (z80)': 'X_Spectrum_(Z80)_ROMs'
}


def unpack(filename, directory):
    """ unpacks archive files """
    print("Attempting to unpack...")
    try:
        shutil.unpack_archive(filename, directory)
        print("Successfully extracted files.")
    except shutil.ReadError:
        if shutil.which('7z'):
            process = subprocess.Popen(["7z", "x", os.path.join(directory, filename),
                                        f"-o{directory}"], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
            _, error = process.communicate()
            if error:
                print('Failed to extract.')
        else:
            extension = os.path.splitext(filename)[1]
            if extension == "7z":
                print("Cannot extract .7z files. Install 7zip and try again.")
            else:
                print(f"Cannot extract '{extension}' files.")


def get_progress_bar(current_download, total_download):
    """ returns progress bar based on terminal width """
    terminal_width = os.get_terminal_size()[0]
    progress_bar_width = terminal_width - _OCCUPIED_SPACE
    percentage = int(current_download / total_download * progress_bar_width)
    return f"[{'=' * percentage}{' ' * (progress_bar_width - percentage)}]"


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


def download_images(gid, directory):
    platform = _PLATFORM_NAMES[get_platform_by_gid(gid)]
    title = get_title_by_gid(gid).replace(" ", "_").strip('\n')
    url = f"{_EMUPARADISE_URL}/{platform}/{title}/{gid}"
    response = requests.get(url)
    soup = bs4.BeautifulSoup(response.text, "html.parser")
    abc = soup.find(id='slider')

    try:
        for x in abc.find_all('li'):
            d = x.find('a', href=True)

            if _IMAGE_DATABASE_URL.replace('https://', '') in d['href']:
                filename = d['href'].split('/')[-1]
                img_url = f"{_IMAGE_DATABASE_URL}/{filename}"
                print('downloading %s' % filename)
                response = requests.get(img_url)
                with open(os.path.join(directory, filename), 'wb') as f:
                    for chunk in response.iter_content(1024**2):
                        f.write(chunk)
                    f.close()
    except BaseException:
        print("Failed to scrap images...")


def download(gid, directory=None, extract=False, scrap_images=False):
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
        print("Downloading '%s'." % filename)
        start_time = time.time()
        total_size = int(response.headers.get('content-length'))
        current_size = 0

        with open(download_path, 'wb') as f:
            for block in response.iter_content(1024**2):
                f.write(block)
                current_size += len(block)
                download_percentage = current_size / total_size * 100
                time_elapsed = time.strftime("%H:%M:%S", time.gmtime(time.time() - start_time))
                percentage = "%03d" % int(download_percentage)
                progress_bar = get_progress_bar(current_size, total_size)
                size = get_size_label(total_size)
                current_time = time.gmtime(int(((time.time() - start_time) / download_percentage) *
                                               (100 - download_percentage)))
                eta = f"ETA {time.strftime('%H:%M:%S', current_time)}"
                print(f"\r{time_elapsed} {percentage}% {progress_bar} {size} {eta}", end="")
            f.close()
            print("\nFile saved to '%s'." % os.path.abspath(download_path))

        if extract:
            unpack(download_path, directory)
        if scrap_images:
            download_images(gid, directory)


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
