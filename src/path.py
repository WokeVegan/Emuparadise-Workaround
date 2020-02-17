import configparser
import os
import sys

from src import tools

CONFIG_PATH = os.path.join(os.path.dirname(sys.argv[0]), "emuw.cfg")
DATABASE_PATH = os.path.join(os.path.dirname(sys.argv[0]), "database")


def get_config():
    config = configparser.ConfigParser()
    config.read(CONFIG_PATH, encoding='utf-8')
    return config


def write_config(config):
    with open(CONFIG_PATH, 'w', encoding='utf-8') as f:
        config.write(f)
    f.close()


def create_settings_template():
    if not os.path.exists(CONFIG_PATH):
        config = get_config()
        config.add_section('DIRECTORY')

        for platform in tools.get_platforms():
            config['DIRECTORY']['DEFAULT'] = ''
            config['DIRECTORY'][str(platform)] = ''

        config.add_section('QUEUE')
        config['QUEUE']['ids'] = ''
        write_config(config)


def get_default_directory(platform=None):
    """ returns the default download directory. """
    config = get_config()

    if platform is None:
        platform = 'default'

    if config.get('DIRECTORY', platform):
        return config.get('DIRECTORY', platform)
    elif config.get('DIRECTORY', 'default'):
        return config.get('DIRECTORY', 'default')

    return os.getcwd()


def does_platform_have_path_set(platform=None):
    config = get_config()

    if platform is None:
        platform = 'default'

    if config.get('DIRECTORY', platform):
        return True

    return False
