#!/usr/bin/env python3

import os
import argparse
import requests
import urllib


def url_is_valid(x):
    """ checks if the url is in the database """
    if not args.force:
        return x in database
    return True


def search():
    """ searches database for specified title """
    keywords = args.search.lower().split(' ')
    matches = [x for x in database if all([key.lower() in x.lower() for key in keywords])]
    for x in matches:
        print(x)


def download():
    """ downloads specified url """
    if not url_is_valid(args.install):
        parser.error("url is not valid")
        raise SystemExit

    gid = args.install.split('/')[-1]
    game_link = "https://www.emuparadise.me/roms/get-download.php?gid=%s&test=true" % gid
    response = requests.get(game_link, headers={"referer": game_link}, stream=True)
    decoded_url = urllib.parse.unquote(response.url)
    filename = os.path.join(download_path, decoded_url.split('/')[-1])

    if os.path.exists(filename):
        print("%s already exists" % filename)

    elif not os.path.exists(filename):
        total_size = int(response.headers.get('content-length'))
        current_size = 0

        with open(filename, 'wb') as f:
            for block in response.iter_content(args.chunk):
                f.write(block)
                current_size += len(block)
                percent = '{0:3d}%'.format(int(current_size / total_size * 100))
                print("\r%.2fMB / %.2fMB\t%s" % (current_size >> 20, total_size >> 20, percent), end="")
            f.close()
        print("\nfile saved to '%s'" % filename)


if __name__ == '__main__':
    download_path = os.path.join(os.path.expanduser("~"))
    database_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'database', 'emuparadise.txt')
    database = [x.strip('\n') for x in open(database_path, 'r').readlines()]

    parser = argparse.ArgumentParser()
    parser.add_argument("-s", "--search", type=str, help="keywords to search for")
    parser.add_argument("-i", "--install", type=str, help="URL of the ROM to install")
    parser.add_argument("-c", "--chunk", type=int, default=2097152, help="read/write chunk size")
    parser.add_argument("-f", "--force", action="store_true", help="skip URL validation check")
    args = parser.parse_args()

    if args.search and not args.install:
        search()
    elif args.install and not args.search:
        download()
