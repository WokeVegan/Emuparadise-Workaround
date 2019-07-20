import os
import configparser

_ROOT = os.path.expanduser('~')
_CONFIG_PATH = os.path.join(_ROOT, '.config', 'Emuparadise-Workaround.cfg')
DATABASE_PATH = os.path.join(os.path.dirname(os.path.realpath(__file__)), "..", "database")


def get_list_platforms():
    platforms = []
    for platform in os.listdir(DATABASE_PATH):
        platforms.append(os.path.splitext(platform)[0])
    return platforms


def create_settings_template():
    config = configparser.ConfigParser()
    config.add_section('DIRECTORY')
    for platform in get_list_platforms():
        config['DIRECTORY']['DEFAULT'] = str()
        config['DIRECTORY'][str(platform)] = str()
    with open(_CONFIG_PATH, 'w', encoding='utf-8') as f:
        config.write(f)
    f.close()


def set_default_directory(directory, platform=None):
    """ changes the default download directory. """
    if not os.path.exists(_CONFIG_PATH):
        create_settings_template()
    config = configparser.ConfigParser()
    config.read(_CONFIG_PATH)
    if platform is None:
        platform = 'default'
    config['DIRECTORY'][platform] = directory
    with open(_CONFIG_PATH, 'w', encoding='utf-8') as f:
        config.write(f)
    f.close()

    print(f"The default download directory has been set to '{directory}'.")


def get_default_directory(platform=None):
    """ returns the default download directory. """
    if not os.path.exists(_CONFIG_PATH):
        create_settings_template()
    elif os.path.isfile(_CONFIG_PATH):
        config = configparser.ConfigParser()
        config.read(_CONFIG_PATH, encoding='utf-8')
        if platform is None:
            platform = 'default'
        if config.get('DIRECTORY', platform):
            return config.get('DIRECTORY', platform)
        elif config.get('DIRECTORY', 'default'):
            return config.get('DIRECTORY', 'default')
    return os.getcwd()
