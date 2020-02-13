from src import tools
from src import path


def add_to_queue(ids):
    config = path.get_config()
    queue = config['QUEUE']['ids'].split(';')
    for gid in config['QUEUE']['ids'].split(';') + ids:
        if gid not in queue:
            name = tools.get_name_by_gid(gid)
            if gid in ids and name is not None:
                print(f"Added {name} to queue.")
                tools.get_name_by_gid(gid)
                queue.append(gid)
    config['QUEUE']['ids'] = ';'.join(queue)
    path.write_config(config)


def clear_queue():
    config = path.get_config()
    config['QUEUE']['ids'] = ''
    path.write_config(config)
    print('Download queue was cleared.')


def remove_from_queue(ids):
    config = path.get_config()
    queue = []
    for gid in config['QUEUE']['ids'].split(';'):
        if gid not in ids:
            queue.append(gid)
        else:
            if tools.get_name_by_gid(gid):
                print(f"Removed {tools.get_name_by_gid(gid)} from the queue.")
    config['QUEUE']['ids'] = ';'.join(queue)
    path.write_config(config)


def download_queue():
    config = path.get_config()
    for gid in config['QUEUE']['ids'].split(';'):
        if gid:
            tools.download(int(gid))
            remove_from_queue(gid)


def list_queue():
    config = path.get_config()
    for gid in config['QUEUE']['ids'].split(';'):
        if gid:
            gid = f"{' ' * (6 - len(gid))}{gid} "
            print(gid, tools.get_name_by_gid(gid))
