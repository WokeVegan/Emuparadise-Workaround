import hashlib
import json
import os
import shutil
import sys
import urllib
import zipfile

import requests


def _verify_md5(filename: str, original_md5: str) -> bool:
    with open(filename, 'rb') as f:
        md5 = hashlib.md5(f.read()).hexdigest()
        f.close()
    return md5 == original_md5


def _get_bios_data(platform):
    with open(os.path.join(os.path.dirname(sys.argv[0]), "database", "bios.json")) as f:
        data = json.loads(f.read())[platform]
        f.close()
    return data


def _bios_exists(platform, rpi_ip):
    data = _get_bios_data(platform)
    target_path = f"//{rpi_ip}/System/"
    target_file = os.path.join(target_path, data['rename-to'])
    if os.path.isfile(target_file):
        return _verify_md5(target_file, data['md5'])
    return False


def install_bios(platform, rpi_ip):
    data = _get_bios_data(platform)

    if _bios_exists(platform, rpi_ip):
        return 2, data['rename-to']

    try:
        response = requests.get(data['link'], stream=True)
        decoded_url = urllib.parse.unquote(response.url)
        temp_path = os.path.realpath(os.path.join(os.path.dirname(sys.argv[0]), "temp"))
        zip_filename = os.path.join(temp_path, decoded_url.split('/')[-1])

        if not os.path.exists(temp_path):
            os.mkdir(temp_path)

        with open(zip_filename, 'wb') as f:

            for chunk in response.iter_content(1024 ** 2):
                f.write(chunk)
            f.close()

        with zipfile.ZipFile(zip_filename, 'r') as f:
            f.extractall(temp_path)

        os.remove(os.path.join(temp_path, zip_filename))
        content_name = os.path.join(temp_path, os.listdir(temp_path)[0])
        if _verify_md5(content_name, data['md5']):
            new_name = os.path.join(temp_path, data['rename-to'])
            os.rename(content_name, new_name)
        else:
            shutil.rmtree(temp_path)
            return 1, data['rename-to'], "MD5 Checksum doesn't match."

        target_path = f"//{rpi_ip}/System/"
        new_location = os.path.join(target_path, os.path.split(new_name)[-1])
        shutil.copyfile(new_name, new_location)
        shutil.rmtree(temp_path)
    except BaseException:
        return 1, data['rename-to']

    return 0, data['rename-to']


def remove_bios(platform, rpi_ip):
    target_file = _get_bios_data(platform).get('rename-to')

    if not _bios_exists(platform, rpi_ip):
        return 2, target_file
    try:
        target_path = f"//{rpi_ip}/System/{target_file}"
        os.remove(target_path)
    except BaseException as e:
        return 1, target_file, e

    return 0, target_file
