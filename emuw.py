#!/usr/bin/env python3

import argparse
from src import tools
from src import path
from src import queue

if __name__ == '__main__':
    path.create_settings_template()
    tools.initialize()
    parser = argparse.ArgumentParser(description='Allows you to search and download ROMs from Emuparadise.')
    parser.add_argument('-d', '--default-rom-directory', nargs='*', help='Sets the default directory games will be saved to.')
    parser.add_argument('-ld', '--list-directories', action='store_true', help='Lists custom download directories for each platform.')
    parser.set_defaults(action=None)

    sub_parsers = parser.add_subparsers()

    search_parser = sub_parsers.add_parser('search')
    search_parser.add_argument('keywords', nargs='+', help='A list of keywords to search for.')
    search_parser.add_argument('-p', '--platform', action='store_true', help='Display the platform next to each game.')
    search_parser.set_defaults(action='search')

    download_parser = sub_parsers.add_parser('download')
    download_parser.add_argument('id', nargs="+", help='ID of the ROM provided from the search command.')
    download_parser.add_argument('-d', '--directory', help='The ROMs save directory. (overrides default directory)')
    download_parser.add_argument('-e', '--extract', action='store_true', help='Attempt to extract the contents after downloading.')
    download_parser.add_argument('-c', '--chunk-size', type=int, help='Changes download chunk size.')
    download_parser.set_defaults(action='download')

    queue_parser = sub_parsers.add_parser('queue')
    queue_parser.add_argument('-a', '--append', nargs='*', help='Add a ROM to the download queue.')
    queue_parser.add_argument('-r', '--remove', nargs='*', help='Remove IDs from the download queue.')
    queue_parser.add_argument('-c', '--clear', action='store_true', help='Removes all IDs from the queue.')
    queue_parser.add_argument('-l', '--list', action='store_true', help='Lists all titles in the queue.')
    queue_parser.add_argument('-d', '--download', action='store_true', help='Starts the download queue.')
    queue_parser.set_defaults(action='queue')

    args = parser.parse_args()

    if args.default_rom_directory:
        if len(args.default_rom_directory) > 1:
            path.set_default_directory(args.default_rom_directory[0], ' '.join(args.default_rom_directory[1:]).lower())
        else:
            path.set_default_directory(args.default_rom_directory[0], 'default')

    if args.list_directories:
        path.list_directories()

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
            for x in args.id:
                if args.chunk_size:
                    chunk_size = args.chunk_size
                else:
                    chunk_size = 1024**2
                tools.download(x, args.directory, args.extract, chunk_size=chunk_size)
        else:
            download_parser.print_help()
    elif args.action == 'queue':
        if args.append:
            queue.add_to_queue(args.append)
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
