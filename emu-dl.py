#!/usr/bin/env python3

import os
import argparse
import requests
import urllib.parse
import time


def strict_search(keywords, database):
    matches = []
    for x in database:
        if all([key.lower() in x.lower() for key in keywords]):
            x_keys = x.lower().split('/')[-2].replace('_', ' ').split(' ')
            if '-' in x_keys:
                x_keys.remove('-')
            try:
                first_index = x_keys.index(keywords[0])
                if all([key.lower() == x_keys[first_index+index].lower() for index, key in enumerate(keywords)]):
                    matches.append(x)
            except ValueError:
                pass

    return matches


def search(keywords):
    """ searches database for keywords """
    database_path = os.path.join(os.path.dirname(os.path.realpath(__file__)), "database.txt")
    database = [x.strip('\n') for x in open(database_path, encoding='utf-8').readlines()]

    try:
        if args.strict:
            matches = strict_search(keywords, database)
        else:
            matches = sorted([x for x in database if all([key.lower() in x.lower() for key in keywords])])
    except AttributeError:  # if batch downloading
        matches = sorted([x for x in database if all([key.lower() in x.lower() for key in keywords])])

    return matches


def get_size_label(size):
    """ returns a formatted size label """
    sizes = {1000000000: "{:1.2f}GB", 1000000: "{0:02.2f}MB", 1000: "{:06.2f}KB",  0: "{:02d}B"}
    for key, value in sizes.items():
        if size >= key:
            try:
                return value.format(size / key)
            except ZeroDivisionError:
                return value.format(size)


def download_batch(urls):
    if len(urls) > 0:
        index = 1
        total_size = 0
        for url in urls:
            print('\rGathering data... %03d' % int((index / len(urls)) * 100), end='')
            gid = url.split('/')[-1]
            game_link = "https://www.emuparadise.me/roms/get-download.php?gid=%s&test=true" % gid
            total_size += int(requests.get(game_link, headers={'referer': game_link}, stream=True).headers['Content-length'])
            index += 1

        answer = input("\nAre you sure you want to download all %d titles? [%s] [y/n] " % (len(urls), get_size_label(total_size)))
        if answer.lower() == 'y':
            for url in urls:

                try:
                    if args.directory:
                        download(url, args.directory)
                    else:
                        download(url)
                except TypeError:
                    print("Error downloading '%s'" % url)
    else:
        print("No results for keywords '%s'" % ' '.join(args.batch))


def download(url, directory=os.getcwd()):
    """ downloads rom """

    gid = url.split('/')[-1]
    game_link = "https://www.emuparadise.me/roms/get-download.php?gid=%s&test=true" % gid
    response = requests.get(game_link, headers={"referer": game_link}, stream=True)
    decoded_url = urllib.parse.unquote(response.url)
    filename = decoded_url.split('/')[-1]
    download_path = os.path.join(directory, filename)
    install = True

    if os.path.exists(download_path):
        overwrite = input("'%s' already exists.\nOverwrite the file? [y/n] " % os.path.abspath(filename))
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
        print("downloading '%s'" % filename)
        start_time = time.time()
        total_size = int(response.headers.get('content-length'))
        current_size = 0
        bar_width = 30

        with open(download_path, 'wb') as f:
            for block in response.iter_content(1024**2):
                f.write(block)
                current_size += len(block)
                download_percent = current_size / total_size * 100
                bar_percent = "=" * int(current_size / total_size * bar_width)
                bar_difference = " " * (bar_width - int(current_size / total_size * bar_width))
                time_label = time.strftime("%H:%M:%S", time.gmtime(time.time() - start_time))
                size_label = get_size_label(total_size)
                remaining_time = int(((time.time() - start_time) / download_percent) * (100 - download_percent))
                time_estimate = time.strftime("%H:%M:%S", time.gmtime(remaining_time))
                bps = get_size_label(current_size // (time.time() - start_time))
                print("\r%s %03d%%[%s%s] %s ETA %s %s/s" % (time_label, int(download_percent), bar_percent,
                                                            bar_difference, size_label, time_estimate, bps), end="")
            f.close()

        print("\nfile saved to '%s'" % os.path.abspath(download_path))


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    sub_parsers = parser.add_subparsers()
    search_parser = sub_parsers.add_parser('search', help='search for game')
    search_parser.add_argument('-k', '--keywords', nargs='+', help='keywords to search', required=True)
    search_parser.add_argument('-s', '--strict', action='store_true', help='uses strict search')
    download_parser = sub_parsers.add_parser('download', help='download url or batch download titles')
    download_parser.add_argument('-u', '--url', help='url of rom')
    download_parser.add_argument('-b', '--batch', nargs='+', help='batch download all match results.')
    download_parser.add_argument('-d', '--directory', help='directory rom will be saved in')
    args = parser.parse_args()

    batch_download = False

    try:
        print(*search(args.keywords), sep='\n')
    except AttributeError:
        pass

    try:
        if args.batch:
            batch_download = True
    except AttributeError:
        pass

    try:
        if batch_download:
            download_batch(search(args.batch))
        else:
            if args.directory:
                download(args.url, args.directory)
            else:
                download(args.url)
    except AttributeError:
        pass
