#!/usr/bin/env python3

import os
import argparse
import requests
import urllib.parse
import time

DOWNLOAD_RATE_SIZE = len("xxx.xx xx/s")
DOWNLOAD_SIZE = len("xxx.xx xx")
ETA_SIZE = len("ETA 00:00:00")
TIME_SIZE = len('00:00:00')


def get_progress_bar(current_download, total_download):
    """ returns progress bar"""
    actual_percentage_width = 4  # ex. 100%
    total_spaces = 6
    if os.name == "nt":
        total_spaces = 7

    terminal_width = os.get_terminal_size()[0]
    progress_bar_width = terminal_width - (actual_percentage_width + total_spaces +
                                           DOWNLOAD_RATE_SIZE + ETA_SIZE + DOWNLOAD_SIZE + TIME_SIZE)
    percentage = int(current_download / total_download * progress_bar_width)
    return f"[{'=' * percentage}{' ' * (progress_bar_width - percentage)}]"


def search():
    """ searches database for keywords """
    database_path = os.path.join(os.path.dirname(os.path.realpath(__file__)), "database")
    database = []
    for platform in os.listdir(database_path):
        with open(os.path.join(database_path, platform), encoding='utf-8') as f:
            for x in f.readlines():
                line = x.strip('\n')
                platform_string = platform.strip('.txt')
                database.append(f"{platform_string}/{line}")

    matches = sorted([x for x in database if all([key.lower() in x.lower() for key in args.keywords])])

    print(f"\n{len(matches)} results found...\n")
    for game in matches:
        platform, gid, title = game.split('/')
        if os.name == "posix":
            gid = f"\033[1;32;34m{gid}\033[0;32;37m"
            platform = f"\033[2;32;37m{platform}\033[0;32;37m"
        if args.platform:
            print(f"{gid}\t{platform} {title}")
        else:
            print(f"{gid}\t{title}")


def get_size_label(size):
    """ returns a formatted size label """
    sizes = {1000000000: "{:1.2f}GB", 1000000: "{0:02.2f}MB", 1000: "{:06.2f}KB",  0: "{:02d}B"}
    for key, value in sizes.items():
        if size >= key:
            try:
                return value.format(size / key)
            except ZeroDivisionError:
                return value.format(size)


def set_default_directory(directory):
    settings = os.path.join(os.path.dirname(os.path.realpath(__file__)), "directory.txt")
    with open(settings, 'w', encoding='utf-8') as f:
        f.write(directory)
    f.close()
    print(f"The default download directory has been set to '{directory}'.")


def get_default_directory():
    settings = os.path.join(os.path.dirname(os.path.realpath(__file__)), "directory.txt")
    if os.path.isfile(settings):
        return open(settings, encoding='utf-8').read()
    return os.getcwd()


def download():
    """ downloads rom """
    gid = args.id
    directory = get_default_directory()
    if args.directory:
        directory = args.directory

    game_link = "https://www.emuparadise.me/roms/get-download.php?gid=%s&test=true" % gid
    response = requests.get(game_link, headers={"referer": game_link}, stream=True)
    decoded_url = urllib.parse.unquote(response.url)
    filename = decoded_url.split('/')[-1]
    download_path = os.path.join(directory, filename)
    install = True

    if os.path.exists(download_path):
        overwrite = input("'%s' already exists.\nOverwrite the file? [y/n] " % os.path.abspath(download_path))
        if overwrite.lower() != 'y':
            install = False
    if not os.path.isdir(directory):
        print(directory)
        create_dir = input("'%s' doesnt exists yet.\nCreate the directory? [y/n] " % directory)
        if create_dir.lower() == 'y':
            os.mkdir(directory)
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
                eta = f"ETA {time.strftime('%H:%M:%S', time.gmtime(int(((time.time() - start_time) / download_percentage) * (100 - download_percentage))))}"
                bps = f"{get_size_label(current_size // (time.time() - start_time))}/s"
                print(f"\r{time_elapsed} {percentage}% {progress_bar} {size} {eta} "
                      f"{' ' * (DOWNLOAD_RATE_SIZE - len(bps))}{bps}", end="")
            f.close()
        print("\nFile saved to '%s'." % os.path.abspath(download_path))


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('-d', '--default-rom-directory', help='Sets the default directory ROMs will be saved to.')
    sub_parsers = parser.add_subparsers()
    search_parser = sub_parsers.add_parser('search')
    search_parser.add_argument('-k', '--keywords', nargs='+', help='Keywords to search for.', required=True)
    search_parser.add_argument('--platform', action='store_true', help='Shows the platform next to each ROM.')
    download_parser = sub_parsers.add_parser('download')
    download_parser.add_argument('-i', '--id', help='ID of the rom you wish to download.')
    download_parser.add_argument('-d', '--directory', help='Directory the rom will be saved in. This overrides the default rom directory.')
    args = parser.parse_args()

    if args.default_rom_directory:
        set_default_directory(args.default_rom_directory)

    try:
        if args.keywords:
            search()
        else:
            search_parser.print_help()
    except AttributeError:
        pass

    try:
        if args.id:
            download()
        else:
            download_parser.print_help()
    except AttributeError:
        pass
