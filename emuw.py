#!/usr/bin/env python3

__version__ = "07-08-2019"

import argparse
from src import tools
from src import path

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description="emu-dl - Allows you to search and download ROMs from emuparadise.")
    parser.add_argument('-d', '--default-rom-directory', help='Sets the default directory games will be saved to.')
    parser.add_argument('-v', '--version', action='version', version=__version__)
    parser.set_defaults(action=None)

    sub_parsers = parser.add_subparsers()

    search_parser = sub_parsers.add_parser('search')
    search_parser.add_argument('keywords', nargs='+', help='Keywords to search for.')
    search_parser.add_argument('-p', '--platform', action='store_true', help='Shows the platform next to each ROM.')
    search_parser.set_defaults(action='search')

    download_parser = sub_parsers.add_parser('download')
    download_parser.add_argument('id', help='ID of the ROM provided from the search command.')
    download_parser.add_argument('-d', '--directory', help='The ROMs save directory. (overrides default directory)')
    download_parser.add_argument('-e', '--extract', action="store_true", help='Attempt to extract the zip file.')
    download_parser.set_defaults(action='download')

    args = parser.parse_args()

    if args.default_rom_directory:
        path.set_default_directory(args.default_rom_directory)

    if args.action == 'search':
        if args.keywords:
            tools.search(args.keywords, args.platform)
        else:
            search_parser.print_help()

    elif args.action == 'download':
        if args.id:
            directory = None
            if args.directory:
                directory = args.directory
            tools.download(args.id, args.directory, args.extract)
        else:
            download_parser.print_help()

    else:
        parser.print_help()
