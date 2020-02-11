import configparser
from src import tools
from src import path


def add_to_queue(ids):
    config = configparser.ConfigParser()
    config.read(path.CONFIG_PATH, encoding='utf-8')
    queue = config['QUEUE']['ids'].split(';')
    for gid in config['QUEUE']['ids'].split(';') + ids:
        if gid not in queue:
            name = tools.get_name_by_gid(gid)
            if gid in ids and name:
                print(f"Added {name} to queue.")
                tools.get_name_by_gid(gid)
            queue.append(gid)
    config['QUEUE']['ids'] = ';'.join(queue)
    with open(path.CONFIG_PATH, 'w', encoding='utf-8') as f:
        config.write(f)


def clear_queue():
    config = configparser.ConfigParser()
    config.read(path.CONFIG_PATH, encoding='utf-8')
    config['QUEUE']['ids'] = ''
    print('Download queue was cleared.')
    with open(path.CONFIG_PATH, 'w', encoding='utf-8') as f:
        config.write(f)


def remove_from_queue(ids):
    config = configparser.ConfigParser()
    config.read(path.CONFIG_PATH, encoding='utf-8')
    queue = []
    for gid in config['QUEUE']['ids'].split(';'):
        if gid not in ids:
            queue.append(gid)
        else:
            if tools.get_name_by_gid(gid):
                print(f"Removed {tools.get_name_by_gid(gid)} from the queue.")
    config['QUEUE']['ids'] = ';'.join(queue)
    with open(path.CONFIG_PATH, 'w', encoding='utf-8') as f:
        config.write(f)


def download_queue():
    config = configparser.ConfigParser()
    config.read(path.CONFIG_PATH, encoding='utf-8')
    for gid in config['QUEUE']['ids'].split(';'):
        if gid:
            tools.download(int(gid))
            remove_from_queue(gid)


def list_queue():
    config = configparser.ConfigParser()
    config.read(path.CONFIG_PATH, encoding='utf-8')
    for gid in config['QUEUE']['ids'].split(';'):
        if gid:
            print(tools.get_name_by_gid(gid))
