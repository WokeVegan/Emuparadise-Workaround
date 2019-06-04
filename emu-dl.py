#!/usr/bin/env python3

import os
import argparse
import requests
import urllib.parse
import time


def search():
    """ searches database for specified title """
    relative_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "database.txt")
    xdg_path = os.path.join(os.path.expanduser("~"), ".local", "share", "emu-dl", "database.txt")

    if os.name == "nt" or not os.path.exists(xdg_path):
        database_path = relative_path
    else:
        database_path = xdg_path

    database = [x.strip('\n') for x in open(database_path, encoding='utf-8').readlines()]
    keywords = args.search.lower().split(' ')
    matches = sorted([x for x in database if all([key.lower() in x.lower() for key in keywords])])

    for x in matches:
        print(x)


def get_size_label(total):
    if total >= 1000000000:
        return "%.2fGB" % (int(total) / 1000000000)
    if total >= 1000000:
        return "%.2fMB" % (int(total) / 1000000)
    elif total >= 1000:
        return "%.2fdKB" % (int(total) / 1000)
    return "%dB" % total


def download():
    """ downloads specified url """
    gid = args.download.split('/')[-1]
    game_link = "https://www.emuparadise.me/roms/get-download.php?gid=%s&test=true" % gid
    response = requests.get(game_link, headers={"referer": game_link}, stream=True)
    decoded_url = urllib.parse.unquote(response.url)
    filename = decoded_url.split('/')[-1]
    install = True

    if os.path.exists(filename):
        overwrite = input("'%s' already exists.\nOverwrite the file? [y/n] " % os.path.abspath(filename))
        if overwrite.lower() != 'y':
            install = False

    if install:
        print("downloading '%s'" % filename)
        start_time = time.time()
        total_size = int(response.headers.get('content-length'))
        current_size = 0
        bar_width = 30

        with open(os.path.join(filename), 'wb') as f:
            for block in response.iter_content(2097152):
                f.write(block)
                current_size += len(block)
                download_percent = current_size / total_size * 100
                bar_percent = "=" * int(current_size / total_size * bar_width)
                bar_difference = " " * (bar_width - int(current_size / total_size * bar_width))
                time_label = time.strftime("%H:%M:%S", time.gmtime(time.time() - start_time))
                size_label = get_size_label(total_size)
                remaining_time = int(((time.time() - start_time) / download_percent) * (100 - download_percent))
                time_estimate = time.strftime("%H:%M:%S", time.gmtime(remaining_time))
                print("\r%s %03d%%[%s%s] %s ETA %s" % (time_label, int(download_percent), bar_percent, bar_difference, size_label, time_estimate), end="")
            f.close()

        print("\nfile saved to '%s'" % os.path.abspath(filename))


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument("-s", "--search", type=str, help="keywords to search")
    parser.add_argument("-d", "--download", type=str, help="link to download")
    args = parser.parse_args()

    if args.search and not args.download:
        search()
    elif args.download and not args.search:
        download()
