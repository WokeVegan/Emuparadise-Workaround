#!/usr/bin/env python3

import os
import json
import argparse
import time
import requests
import urllib
import sys

with open(os.path.join(os.path.dirname(os.path.abspath(__file__)), 'database', 'emuparadise.json'), 'r') as f:
    database = json.load(f)
f.close()

parser = argparse.ArgumentParser()
parser.add_argument("-s", "--search", help="search term")
parser.add_argument("-i", "--install", help="url of rom to install")
parser.add_argument("-p", "--platform", default='all', help="valid platforms: %s" % ' '.join(x for x in database.keys()))
args = parser.parse_args()


def url_is_valid(x):
    """ checks if the url is in the database """
    for _, game_list in database.items():
        for _, url in game_list.items():
            if url == x:
                return True
    return False


if args.search and not args.install:
    if args.platform not in database and args.platform is not 'all':
        print(parser.print_help())
        raise SystemExit

    if args.platform in database:
        for title, url in database.get(args.platform).items():
            if args.search.lower() in title.lower():
                print("%s\n%s\n" % (title, url))

    elif args.platform == 'all':
        for platform, game_list in database.items():
            for title, url in game_list.items():
                if args.search.lower() in title.lower():
                    print("(%s) %s\n%s\n" % (platform, title, url))

elif args.install and not args.search:
    if not args.install or not url_is_valid(args.install):
        parser.print_help()
        raise SystemExit

    start = time.time()
    gid = args.install.split('/')[-1]
    game_link = "https://www.emuparadise.me/roms/get-download.php?gid=%s&test=true" % gid
    response = requests.get(game_link, headers={"referer": game_link}, stream=True)
    decoded_url = urllib.parse.unquote(response.url)
    filename = decoded_url.split('/')[-1]

    with open(os.path.join(filename), 'wb') as f:
        total_length = response.headers.get('content-length')
        print("downloading", "(%s)" % filename)
        progress = 0
        total_length = int(total_length)

        for block in response.iter_content(4096):
            f.write(block)
            progress += len(block)
            done = int(50 * progress / total_length)
            percent = '{0:.2f}%'.format((progress / total_length * 100))
            string = ''
            sys.stdout.write("\r%s [%s%s] %.2fMB/%.2fMB" % (
                percent, '=' * done, ' ' * (50 - done), progress / 1000000, total_length / 1000000))
            sys.stdout.flush()
        end = time.time() - start
        f.close()
    print("\ndownload completed in %.4fs\n" % end)

else:
    parser.print_help()

