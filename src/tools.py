#!/usr/bin/env python3

import os
import requests
import shutil
import urllib.parse
import time
import subprocess
from src import path

_DEFAULT_COLOR = "\033[0;32;37m"
_GREY = "\033[2;32;37m"
_BLUE = "\033[1;32;34m"
_OCCUPIED_SPACE = 38
_BAD_FILENAME = "get-download.php?gid=%s&test=true"
_GAME_LINK = "https://www.emuparadise.me/roms/get-download.php?gid=%s&test=true"
_SIZES = {1000000000: "{:1.2f}GB", 1000000: "{0:02.2f}MB", 1000: "{:06.2f}KB", 0: "{:02d}B"}


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
