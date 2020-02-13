import os
import configparser
from src import tools

if os.name == 'nt':
    _CONFIG_PATH = os.path.join(os.path.expanduser('~'), 'Emuparadise-Workaround.cfg')
else:
    _CONFIG_PATH = os.path.join(os.path.expanduser('~'), '.config', 'Emuparadise-Workaround.cfg')

DATABASE_PATH = os.path.join(os.path.dirname(os.path.realpath(__file__)), "..", "database")


def get_config():
    config = configparser.ConfigParser()
    config.read(_CONFIG_PATH, encoding='utf-8')
    return config


def write_config(config):
    with open(_CONFIG_PATH, 'w', encoding='utf-8') as f:
        config.write(f)


def create_settings_template():
    if not os.path.exists(_CONFIG_PATH):
        config = configparser.ConfigParser()
        config.add_section('DIRECTORY')
        for platform in tools.get_platforms():
            config['DIRECTORY']['DEFAULT'] = str()
            config['DIRECTORY'][str(platform)] = str()
        config.add_section('STYLE')
        config['STYLE']['default_color'] = '\033[0;32;37m'
        config['STYLE']['platform_color'] = '\033[2;32;37m'
        config['STYLE']['game_id_color'] = '\033[1;32;34m'
        config.add_section('QUEUE')
        config['QUEUE']['ids'] = ''
        with open(_CONFIG_PATH, 'w', encoding='utf-8') as f:
            config.write(f)
        f.close()


def get_style_settings():
    config = configparser.ConfigParser()
    config.read(_CONFIG_PATH, encoding='utf-8')
    return dict(config.items('STYLE'))


def list_directories():
    config = configparser.ConfigParser()
    config.read(_CONFIG_PATH, encoding='utf-8')
    for key, value in config.items('DIRECTORY'):
        if value:
            print(key, '=', value)


def set_default_directory(directory, platform=None):
    """ changes the default download directory. """
    config = configparser.ConfigParser()
    config.read(_CONFIG_PATH, encoding='utf-8')
    if platform is None:
        platform = 'default'
    config['DIRECTORY'][platform] = directory
    with open(_CONFIG_PATH, 'w', encoding='utf-8') as f:
        config.write(f)
    f.close()

    print(f"Directory for '{platform}' has been set to '{directory}'.")


def get_default_directory(platform=None):
    """ returns the default download directory. """
    config = configparser.ConfigParser()
    config.read(_CONFIG_PATH, encoding='utf-8')
    if platform is None:
        platform = 'default'
    if config.get('DIRECTORY', platform):
        return config.get('DIRECTORY', platform)
    elif config.get('DIRECTORY', 'default'):
        return config.get('DIRECTORY', 'default')
    return os.getcwd()
