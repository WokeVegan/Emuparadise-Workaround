#!/usr/bin/env python3

import os
import requests
import shutil
import urllib.parse
import time
from src import path


def get_progress_bar(current_download, total_download):
    """ returns progress bar based on terminal width """
    terminal_width = os.get_terminal_size()[0]
    download_size = 9
    eta_size = 12
    time_size = 8
    percentage_width = 4
    total_spaces = 5

    if os.name == "nt":
        total_spaces += 1

    progress_bar_width = terminal_width - (percentage_width + total_spaces + eta_size + download_size + time_size)
    percentage = int(current_download / total_download * progress_bar_width)

    return f"[{'=' * percentage}{' ' * (progress_bar_width - percentage)}]"


def get_size_label(size):
    """ returns a prettier size label """
    sizes = {1000000000: "{:1.2f}GB", 1000000: "{0:02.2f}MB", 1000: "{:06.2f}KB",  0: "{:02d}B"}
    for key, value in sizes.items():
        if size >= key:
            try:
                return value.format(size / key)
            except ZeroDivisionError:
                return value.format(size)


def check_bad_id(filename, gid):
    """ exit if download link is bad """
    bad_filename = f"get-download.php?gid={gid}&test=true"
    if filename == bad_filename:
        print("Failed to download due to bad ID.")
        raise SystemExit


def download(gid, directory=None, extract=False):
    """ attempt to download rom """

    if directory:
        directory = directory
    else:
        directory = path.get_default_directory()

    game_link = f"https://www.emuparadise.me/roms/get-download.php?gid={gid}&test=true"
    response = requests.get(game_link, headers={"referer": game_link}, stream=True)
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
            print("Unpacking archive...")
            try:
                shutil.unpack_archive(download_path, directory)
                print("Successfully extracted archive.")
            except shutil.ReadError:
                extension = os.path.splitext(download_path)[1]
                print(f"Cannot extract '{extension}' files.")


def search(keywords, show_platform=False):
    """ prints all matching games """
    database_path = os.path.join(os.path.dirname(os.path.realpath(__file__)), "..", "database")
    database = []
    for platform in os.listdir(database_path):
        with open(os.path.join(database_path, platform), encoding='utf-8') as f:
            for x in f.readlines():
                line = x.strip('\n')
                platform_string = platform.strip('.txt')
                database.append(f"{platform_string}/{line}")

    matches = sorted([x for x in database if all([key.lower() in x.lower() for key in keywords])])

    print(f"\n{len(matches)} results found...\n")

    for game in matches:
        platform, gid, title = game.split('/')

        if os.name == "posix":
            underline = "\033[4;32;37m"
            default_color = "\033[0;32;37m"
            gid = f"\033[1;32;34m{gid}{default_color}"
            platform = f"\033[2;32;37m{platform}{default_color}"
            colorized_title = []
            for word in title.split(" "):
                if word.lower() in [x.lower() for x in keywords]:
                    colorized_title.append(f"{underline}{word}{default_color}")
                else:
                    colorized_title.append(word)
            title = " ".join(colorized_title)

        if show_platform:
            print(f"{gid}\t[{platform}] {title}")
        else:
            print(f"{gid}\t{title}")
