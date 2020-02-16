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


if os.name == 'nt':
    _OCCUPIED_SPACE = 39
else:
    _OCCUPIED_SPACE = 38

BAD_FILENAME = "get-download.php?gid=%s&test=true"
GAME_LINK = "https://www.emuparadise.me/roms/get-download.php?gid=%s&test=true"
_SIZES = {1000000000: "{:1.2f}GB", 1000000: "{0:02.2f}MB", 1000: "{:02.2f}KB", 0: "{:02d}B"}
_INITIALIZED = False


def format_gid(gid):
    """ formats ids by removing leading 0s. """
    return str(int(gid))


def initialize():
    global _INITIALIZED
    path.create_settings_template()
    _INITIALIZED = True


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


def check_bad_id(filename, gid):
    """ exit if download link is bad """
    if filename == BAD_FILENAME % format_gid(gid):
        return 1


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


def download(gid, directory=None):
    """ attempt to download rom """
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

                    links = []
                    html = requests.get(value['link']).text
                    soup = bs4.BeautifulSoup(html, "html.parser")

                    for file in soup.find_all("div", class_="download-link"):
                        for x in file.find_all('p'):
                            title = x.find('a')['title']
                            filename = re.search("Download (.+?) ISO", title)
                            filename = filename.group(1)
                            link = "http://50.7.92.186/happyxhJ1ACmlTrxJQpol71nBc/Dreamcast/" + filename
                            links.append(link)

                    for x in links:
                        game_links.append([x, {"referer": x}])
    else:
        game_links.append([GAME_LINK % gid, {"referer": GAME_LINK % gid}])

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
            for block in response.iter_content(1024**2):
                f.write(block)
                current_size += len(block)
                progress_bar = get_progress_bar(current_size, total_size, start_time)
                print(progress_bar, end="")
            f.close()
            print("\nFile saved to '%s'." % os.path.abspath(download_path))


def search(keywords, show_platform=False):
    """ prints all matching games """
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
        gid = f"{' ' * (6 - len(gid))}{gid} "

        if show_platform:
            print(f"{gid}[{platform}] {title}")
        else:
            print(f"{gid} {title}")
