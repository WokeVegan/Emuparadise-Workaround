#!/usr/bin/env python3

import os
import json
import argparse

with open(os.path.join(os.path.dirname(os.path.abspath(__file__)), 'database', 'emuparadise.json'), 'r') as f:
    database = json.load(f)
    f.close()

parser = argparse.ArgumentParser()
parser.add_argument("title", help="search term")
parser.add_argument("platform", help="valid platforms: all %s" % ' '.join(x for x in database.keys()))
args = parser.parse_args()

if not any([args.platform in database, args.platform == 'all']):
    print(parser.print_help())
    raise SystemExit

if args.platform in database:
    for title, url in database.get(args.platform).items():
        if args.title.lower() in title.lower():
            print("%s\n%s\n" % (title, url))

elif args.platform == 'all':
    for platform, game_list in database.items():
        for title, url in game_list.items():
            if args.title.lower() in title.lower():
                print("(%s) %s\n%s\n" % (platform, title, url))
