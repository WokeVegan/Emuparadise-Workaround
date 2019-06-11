#!/usr/bin/env python3

import requests


with open('demo/database.txt', 'wb') as f:
    response = requests.get("https://raw.githubusercontent.com/WokeVegan/emu-dl/master/database.txt", stream=True)
    print('downloading database.txt...')
    for block in response.iter_content(1024**2):
        f.write(block)
    f.close()

with open('demo/emu-dl.py', 'wb') as f:
    response = requests.get("https://raw.githubusercontent.com/WokeVegan/emu-dl/master/emu-dl.py", stream=True)
    print('downloading emu-dl.py...')
    for block in response.iter_content(1024**2):
        f.write(block)
    f.close()
