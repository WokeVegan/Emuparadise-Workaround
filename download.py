# !/usr/bin/env python3

import os
import sys
import time
import urllib
import argparse
import requests

parser = argparse.ArgumentParser()
parser.add_argument('url', help="url of rom provided from search.py")
args = parser.parse_args()

if not args.url:
    print(parser.print_help())
    raise SystemExit

start = time.time()
gid = args.url.split('/')[-1]
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

    print("\ndownload completed in %.4fs\n" % end)
    f.close()
