#!/usr/bin/env python3

import os
import shutil
import urllib.parse
import time
import requests
import json
import bs4
import re
from src import path

try:
    import libarchive.public
    IMPORTED_LIBARCHIVE = True
except ModuleNotFoundError:
    IMPORTED_LIBARCHIVE = False


if os.name == 'nt':
    _OCCUPIED_SPACE = 39
else:
    _OCCUPIED_SPACE = 38

_BAD_FILENAME = "get-download.php?gid=%s&test=true"
_GAME_LINK = "https://www.emuparadise.me/roms/get-download.php?gid=%s&test=true"
_SIZES = {1000000000: "{:1.2f}GB", 1000000: "{0:02.2f}MB", 1000: "{:02.2f}KB", 0: "{:02d}B"}
_EMUPARADISE_URL = "https://www.emuparadise.me"
_STYLE_SETTINGS = None
_DEFAULT_COLOR = None
_PLATFORM_COLOR = None
_GAME_ID_COLOR = None
_INITIALIZED = False


def format_gid(gid):
    """ formats ids by removing leading 0s. """
    return str(int(gid))


def initialize():
    global _STYLE_SETTINGS, _DEFAULT_COLOR, _PLATFORM_COLOR, _GAME_ID_COLOR, _INITIALIZED
    path.create_settings_template()
    _STYLE_SETTINGS = path.get_style_settings()
    _DEFAULT_COLOR = _STYLE_SETTINGS.get('default_color')
    _PLATFORM_COLOR = _STYLE_SETTINGS.get('platform_color')
    _GAME_ID_COLOR = _STYLE_SETTINGS.get('game_id_color')
    _INITIALIZED = True


def unpack(filename, directory):
    """ unpacks archive files """
    file_path = os.path.join(directory, filename)
    folder_path = os.path.join(directory, os.path.splitext(filename)[0])

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


def get_platforms():
    platforms = []
    for platform in os.listdir(path.DATABASE_PATH):
        platforms.append(os.path.splitext(platform)[0])
    return platforms


def get_dreamcast_link(url):
    """ this is a temporary workaround to get dreamcast links. """
    links = []
    html = requests.get(url).text
    soup = bs4.BeautifulSoup(html, "html.parser")

    for file in soup.find_all("div", class_="download-link"):
        for x in file.find_all('p'):
            title = x.find('a')['title']
            filename = re.search("Download (.+?) ISO", title)
            filename = filename.group(1)
            link = "http://50.7.92.186/happyxhJ1ACmlTrxJQpol71nBc/Dreamcast/" + filename
            links.append(link)
    return links


def check_bad_id(filename, gid):
    """ exit if download link is bad """
    if filename == _BAD_FILENAME % format_gid(gid):
        print("Failed to download due to bad ID.")
        raise SystemExit


def get_platform_by_gid(gid):
    """ search for gid in database and return the platform it's contained in """
    for filename in os.listdir(path.DATABASE_PATH):
        with open(os.path.join(path.DATABASE_PATH, filename), encoding='utf-8') as f:
            database = json.load(f)
        f.close()

        name, extension = os.path.splitext(filename)
        current_platform = name.lower()
        for key in database.keys():
            if str(format_gid(gid)) == key:
                return current_platform
    return None


def get_name_by_gid(gid):
    """ search for gid in database and return the platform it's contained in """
    for filename in os.listdir(path.DATABASE_PATH):
        with open(os.path.join(path.DATABASE_PATH, filename), encoding='utf-8') as f:
            database = json.load(f)
        f.close()

        for key, value in database.items():
            if str(format_gid(gid)) == key:
                return value
    return


def download(gid, directory=None, extract=False, chunk_size=1024**2):
    """ attempt to download rom """

    _check_if_initialized()

    gid = format_gid(gid)

    if not directory:
        directory = path.get_default_directory(get_platform_by_gid(gid))

    game_links = []
    platform = get_platform_by_gid(gid)
    if platform.lower() == 'dreamcast':
        with open(os.path.join(path.DATABASE_PATH, 'Dreamcast.json'), encoding='utf-8') as f:
            database = json.load(f)
            for key, value in database.items():
                if str(gid) == key:
                    game_link = get_dreamcast_link(value['link'])
                    for x in game_link:
                        game_links.append([x, {"referer": x}])
    else:
        game_links.append([_GAME_LINK % gid, {"referer": _GAME_LINK % gid}])

    for game_link in game_links:
        response = requests.get(game_link[0], headers=game_link[1], stream=True)
        decoded_url = urllib.parse.unquote(response.url)
        filename = decoded_url.split('/')[-1]
        download_path = os.path.join(directory, filename)
        check_bad_id(filename, gid)

        if os.path.exists(download_path):
            question = f"'{os.path.abspath(download_path)}' already exists.\nOverwrite the file? [y/n] "
            overwrite = input(question)
            if overwrite.lower() != 'y':
                return

        if not os.path.isdir(directory):
            question = f"'{directory}' doesnt exists yet.\nCreate the directory? [y/n] "
            create_dir = input(question)
            if create_dir.lower() == 'y':
                os.makedirs(directory)
            else:
                return

        print("\nDownloading '%s'." % filename)
        start_time = time.time()
        total_size = int(response.headers.get('content-length'))
        current_size = 0

        with open(download_path, 'wb') as f:
            for block in response.iter_content(chunk_size):
                f.write(block)
                current_size += len(block)
                progress_bar = get_progress_bar(current_size, total_size, start_time)
                print(progress_bar, end="")
            f.close()
            print("\nFile saved to '%s'." % os.path.abspath(download_path))

        if extract:
            unpack(download_path, directory)


def _check_if_initialized():
    assert _INITIALIZED is True, "tools have not been initialized yet. try calling tools.initialize()"


def search(keywords, show_platform=False):
    """ prints all matching games """
    _check_if_initialized()

    matches = []

    for filename in os.listdir(path.DATABASE_PATH):
        with open(os.path.join(path.DATABASE_PATH, filename), encoding='utf-8') as f:
            for key, value in json.load(f).items():
                if filename == "Dreamcast.json":
                    string = f"{os.path.splitext(filename)[0]};{key};{value['title']}"
                    if all([keyword.lower() in string.lower() for keyword in keywords]):
                        matches.append(string)
                else:
                    string = f"{os.path.splitext(filename)[0]};{key};{value}"
                    if all([keyword.lower() in string.lower() for keyword in keywords]):
                        matches.append(string)
        f.close()

    print(f"\n{len(matches)} results found...\n")

    for game in sorted(matches):
        platform, gid, title = game.split(';')
        gid = format_gid(gid)

        if os.name == 'nt':
            gid = f"{' ' * (6 - len(gid))}{gid} "

        else:
            gid = f"{_GAME_ID_COLOR}{' ' * (6 - len(gid))}{gid}{_DEFAULT_COLOR}"
            platform = f"{_PLATFORM_COLOR}{platform}{_DEFAULT_COLOR}"

        if show_platform:
            print(f"{gid}[{platform}] {title}")
        else:
            print(f"{gid} {title}")
