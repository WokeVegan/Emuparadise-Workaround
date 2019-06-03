#!/usr/bin/env python3

import os
import argparse
import requests
import urllib.parse


def search():
    """ searches database for specified title """
    relative_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'database', 'emuparadise.txt')
    xdg_path = os.path.join(os.path.expanduser("~"), ".local", "share", "emuw", "database", "emuparadise.txt")

    if os.name == "nt" or not os.path.exists(xdg_path):
        database_path = relative_path
    else:
        database_path = xdg_path

    database = [x.strip('\n') for x in open(database_path, encoding='utf-8').readlines()]

    keywords = args.search.lower().split(' ')
    matches = [x for x in database if all([key.lower() in x.lower() for key in keywords])]
    for x in matches:
        print(x)


def download():
    """ downloads specified url """
    gid = args.download.split('/')[-1]
    game_link = "https://www.emuparadise.me/roms/get-download.php?gid=%s&test=true" % gid
    response = requests.get(game_link, headers={"referer": game_link}, stream=True)
    decoded_url = urllib.parse.unquote(response.url)
    filename = decoded_url.split('/')[-1]

    if os.path.exists(filename):
        print("%s already exists" % filename)
    elif not os.path.exists(filename):
        total_size = int(response.headers.get('content-length'))
        current_size = 0

        with open(filename, 'wb') as f:
            for block in response.iter_content(2097152):
                f.write(block)
                current_size += len(block)
                percent = '{0:3d}%'.format(int(current_size / total_size * 100))
                print("\r%.2fMB / %.2fMB\t%s" % (current_size >> 20, total_size >> 20, percent), end="")
            f.close()
        print("\nfile saved to '%s'" % filename)


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument("-s", "--search", type=str, help="keywords to search")
    parser.add_argument("-d", "--download", type=str, help="link to download")
    args = parser.parse_args()

    if args.search and not args.download:
        search()
    elif args.download and not args.search:
        download()
