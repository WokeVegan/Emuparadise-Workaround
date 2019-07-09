import os
import configparser

_DIRECTORY_PATH = os.path.join(os.path.dirname(os.path.realpath(__file__)), "..",  "settings.cfg")


def set_default_directory(directory):
    """ changes the default download directory. """
    config = configparser.ConfigParser()
    if not config.has_section('DIRECTORY'):
        config.add_section('DIRECTORY')
    config['DIRECTORY']['DEFAULT'] = directory
    with open(_DIRECTORY_PATH, 'w', encoding='utf-8') as f:
        config.write(f)
    f.close()

    print(f"The default download directory has been set to '{directory}'.")


def get_default_directory():
    """ returns the default download directory. """
    if os.path.isfile(_DIRECTORY_PATH):
        config = configparser.ConfigParser()
        config.read(_DIRECTORY_PATH, encoding='utf-8')
        return config.get('DIRECTORY', 'default')
    return os.getcwd()
