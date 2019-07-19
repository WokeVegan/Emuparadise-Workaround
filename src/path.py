import os
import configparser


_DIRECTORY_PATH = os.path.join(os.path.dirname(os.path.realpath(__file__)), "..",  "settings.cfg")


def get_list_platforms():
    database_path = os.path.join(os.path.dirname(os.path.realpath(__file__)), "..", "database")
    platforms = []
    for platform in os.listdir(database_path):
        platforms.append(os.path.splitext(platform)[0])
    return platforms


def create_settings_template():
    config = configparser.ConfigParser()
    config.add_section('DIRECTORY')
    for platform in get_list_platforms():
        config['DIRECTORY']['DEFAULT'] = str()
        config['DIRECTORY'][str(platform)] = str()
    with open(_DIRECTORY_PATH, 'w', encoding='utf-8') as f:
        config.write(f)
    f.close()


def set_default_directory(directory, platform=None):
    """ changes the default download directory. """
    if not os.path.exists(_DIRECTORY_PATH):
        create_settings_template()
    config = configparser.ConfigParser()
    config.read(_DIRECTORY_PATH)
    if platform is None:
        platform = 'default'
    config['DIRECTORY'][platform] = directory
    with open(_DIRECTORY_PATH, 'w', encoding='utf-8') as f:
        config.write(f)
    f.close()

    print(f"The default download directory has been set to '{directory}'.")


def get_default_directory(platform=None):
    """ returns the default download directory. """
    if not os.path.exists(_DIRECTORY_PATH):
        create_settings_template()
    elif os.path.isfile(_DIRECTORY_PATH):
        config = configparser.ConfigParser()
        config.read(_DIRECTORY_PATH, encoding='utf-8')
        if platform is None:
            platform = 'default'
        if config.get('DIRECTORY', platform):
            return config.get('DIRECTORY', platform)
        elif config.get('DIRECTORY', 'default'):
            return config.get('DIRECTORY', 'default')
    return os.getcwd()
