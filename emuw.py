#!/usr/bin/env python3

import argparse
from src import tools
from src import path
from src import queue

if __name__ == '__main__':
    tools.initialize()
    parser = argparse.ArgumentParser(description='Allows you to search and download ROMs from Emuparadise.')
    p2 = parser.add_mutually_exclusive_group()

    p2.add_argument('-d', '--default-rom-directory', nargs='*', help='Sets the default directory games will be saved to.')
    p2.add_argument('-ld', '--list-directories', action='store_true', help='Lists custom download directories for each platform.')
    parser.set_defaults(action=None)
    p2.set_defaults(action=None)

    sub_parsers = parser.add_subparsers()

    search_parser = sub_parsers.add_parser('search')
    search_parser.add_argument('keywords', nargs='+', help='A list of keywords to search for.')
    search_parser.add_argument('--platforms', action='store_true', help='Display the platform next to each game.')
    search_parser.set_defaults(action='search')

    download_parser = sub_parsers.add_parser('download')
    download_parser.add_argument('id', nargs="+", help='ID of the ROM provided from the search command.')
    download_parser.add_argument('-d', '--directory', help='The ROMs save directory. (overrides default directory)')
    download_parser.set_defaults(action='download')

    queue_parser = sub_parsers.add_parser('queue')
    qp2 = queue_parser.add_mutually_exclusive_group()
    qp2.add_argument('--add', nargs='*', help='Add a ROM to the download queue.')
    qp2.add_argument('--remove', nargs='*', help='Remove IDs from the download queue.')
    qp2.add_argument('--clear', action='store_true', help='Removes all IDs from the queue.')
    qp2.add_argument('--list', action='store_true', help='Lists all titles in the queue.')
    qp2.add_argument('--download', action='store_true', help='Starts the download queue.')
    qp2.set_defaults(action='queue')

    args = parser.parse_args()

    if args.default_rom_directory:
        if len(args.default_rom_directory) > 1:
            path.set_default_directory(args.default_rom_directory[0], ' '.join(args.default_rom_directory[1:]).lower())
        else:
            path.set_default_directory(args.default_rom_directory[0], 'default')

    if args.list_directories:
        for key, value in path.list_directories():
            if value:
                print(key, '=', value)

    if args.action == 'search':
        if args.keywords:
            tools.search(args.keywords, args.platforms)
        else:
            search_parser.print_help()

    elif args.action == 'download':
        if args.id:
            directory = None
            if args.directory:
                directory = args.directory
            for x in args.id:
                tools.download(x, args.directory)
        else:
            download_parser.print_help()
    elif args.action == 'queue':
        if args.add:
            queue.add_to_queue(args.add)
        elif args.remove:
            queue.remove_from_queue(args.remove)
        elif args.clear:
            queue.clear_queue()
        elif args.list:
            queue.list_queue()
        elif args.download:
            queue.download_queue()
        else:
            queue_parser.print_help()
