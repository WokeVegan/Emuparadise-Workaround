import json
import os

from src import path

BAD_FILENAME = "get-download.php?gid=%s&test=true"
GAME_LINK = "https://www.emuparadise.me/roms/get-download.php?gid=%s&test=true"
_SIZES = {1000000000: "{:1.2f} GB", 1000000: "{0:02.2f} MB", 1000: "{:02.2f} KB", 0: "{:02d} B"}


def format_gid(gid):
    """ formats ids by removing leading 0s. """
    return str(int(gid))


def get_size_label(size):
    """ returns a prettier size label """
    for key, value in _SIZES.items():
        if size >= key:
            try:
                return value.format(size / key)
            except ZeroDivisionError:
                return value.format(size)


def get_platforms():
    return [os.path.splitext(platform)[0] for platform in os.listdir(path.DATABASE_PATH) if platform.endswith('json')]


def check_bad_id(filename, gid):
    """ returns true if download link is bad """
    return filename == BAD_FILENAME % format_gid(gid)


def get_platform_by_gid(gid):
    """ search for gid in database and return the platform it's contained in """
    for filename in os.listdir(path.DATABASE_PATH):
        with open(os.path.join(path.DATABASE_PATH, filename), encoding='utf-8') as f:
            database = json.load(f)
        f.close()

        name, extension = os.path.splitext(filename)
        for key in database.keys():
            if str(format_gid(gid)) == key:
                return name
    return None


def get_search_results(keywords, platform='All'):
    """ returns all matching games """
    matches = []

    if platform != 'All':
        filename = platform + '.json'
        with open(os.path.join(path.DATABASE_PATH, filename), encoding='utf-8') as f:
            for key, value in json.load(f).items():
                string = f"{os.path.splitext(filename)[0]};{key};{value}"

                if keywords:
                    if all([keyword.lower() in string.lower() for keyword in keywords]):
                        matches.append(string)
                else:
                    matches.append(string)
        f.close()
    else:
        for filename in get_platforms():
            with open(os.path.join(path.DATABASE_PATH, filename + '.json'), encoding='utf-8') as f:
                for key, value in json.load(f).items():
                    string = f"{os.path.splitext(filename)[0]};{key};{value}"
                    if keywords:
                        if all([keyword.lower() in string.lower() for keyword in keywords]):
                            matches.append(string)
                    else:
                        matches.append(string)
            f.close()

    return matches
