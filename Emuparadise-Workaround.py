import json
import os
import re
import shutil
import socket
import threading
import time
import urllib
from functools import partial

import bs4
import requests
from PyQt5 import QtCore
from PyQt5 import QtWidgets

from emuw import bios
from emuw import path
from emuw import tools
from emuw import widgets


LAKKA_SUPPORTED_PLATFORMS = [
    "3DO", "Atari 7800", "Atari Jaguar", "Atari Lynx", "WonderSwan Color", "WonderSwan", "MAME", "TurboGrafx 16",
    "PC-FX", "Famicom Disk System", "Game Boy Advance", "Game Boy Color", "Game Boy", "Nintendo 64", "Nintendo DS",
    "Nintendo Entertainment System", "Super Nintendo Entertainment System", "Virtual Boy", "SNK - Neo Geo Pocket Color",
    "SNK - Neo Geo Pocket", "ScummVM", "Sega - 32X", "Sega - Game Gear", "Sega - Master System - Mark III",
    "Sega - Mega-CD - Sega CD", "Sega - Mega Drive - Genesis", "Sega - Saturn", "Sinclair - ZX Spectrum",
    "PlayStation Portable", "PlayStation", "PlayStation - Demos", "PSX on PSP",
    "Dreamcast", "ZX Spectrum (Z80)"
]


class EWMainWindow(QtWidgets.QMainWindow):
    updated = QtCore.pyqtSignal()
    set_progress = QtCore.pyqtSignal(int)
    set_size_label = QtCore.pyqtSignal(str)
    signal_kill_rpi_storage_thread = QtCore.pyqtSignal()

    def __init__(self, *args, **kwargs):
        QtWidgets.QMainWindow.__init__(self)
        self.setWindowTitle("Emuparadise Workaround")
        self.resize(705, 452)
        self.setBaseSize(QtCore.QSize(480, 400))
        self.setAutoFillBackground(False)
        self.setIconSize(QtCore.QSize(24, 24))
        self.statusBar = QtWidgets.QStatusBar(self)

        self.central_widget = QtWidgets.QWidget(self)

        self.download_button = QtWidgets.QPushButton(self.central_widget)
        self.download_button.setMaximumWidth(200)
        self.download_button.setStatusTip("Download the selected game.")
        self.download_button.setText("Download")
        self.download_button.clicked.connect(self.on_download)

        self.cancel_button = QtWidgets.QPushButton(self.central_widget)
        self.cancel_button.setMaximumWidth(200)
        self.cancel_button.setVisible(False)
        self.cancel_button.setStatusTip("Cancel the current download.")
        self.cancel_button.setText("Cancel")
        self.cancel_button.clicked.connect(self.on_cancel_download)

        self.rpi_enabled = QtWidgets.QLabel(self.central_widget)
        self.rpi_enabled.setText(f"RPI ENABLED: {path.get_config().getboolean('RPI', 'enabled')}")
        self.rpi_storage_label = QtWidgets.QLabel(self.central_widget)

        self.progressBar = QtWidgets.QProgressBar(self.central_widget)
        self.progressBar.setEnabled(False)

        self.game_list = QtWidgets.QListWidget(self.central_widget)
        self.game_list.setTabletTracking(False)
        self.game_list.setAcceptDrops(False)
        self.game_list.setEditTriggers(QtWidgets.QAbstractItemView.NoEditTriggers)
        self.game_list.setAlternatingRowColors(True)
        self.game_list.setUniformItemSizes(False)
        self.game_list.setSelectionRectVisible(True)
        self.game_list.setStatusTip("Select a game to download.")
        self.game_list.setSortingEnabled(False)

        self.search_box = QtWidgets.QLineEdit(self.central_widget)
        self.search_box.setPlaceholderText('Keywords')
        self.search_box.setMinimumWidth(400)
        self.search_box.setStatusTip("Enter keywords in the games title to search for.")

        self.search_button = QtWidgets.QPushButton(self.central_widget)
        self.search_button.setStatusTip("Begin searching for matches in the database.")
        self.search_button.setText("Search")
        self.search_button.clicked.connect(self.on_search)

        self.platform_search = QtWidgets.QComboBox(self.central_widget)
        self.platform_search.setToolTip("Get platform specific results")
        self.platform_search.addItem('All')
        if path.get_config().getboolean('RPI', 'enabled'):
            self.platform_search.addItems(
                [platform for platform in tools.get_platforms() if platform in LAKKA_SUPPORTED_PLATFORMS])
        else:
            self.platform_search.addItems([platform for platform in tools.get_platforms()])

        self.grid_layout = QtWidgets.QGridLayout(self.central_widget)
        self.grid_layout.setContentsMargins(9, -1, -1, -1)
        self.grid_layout.addWidget(self.download_button, 2, 0, 1, 1)
        self.grid_layout.addWidget(self.cancel_button, 2, 0, 1, 1)

        self.grid_layout.addWidget(self.rpi_enabled, 2, 3, 1, 1)
        self.grid_layout.addWidget(self.rpi_storage_label, 2, 2, 1, 1)
        self.grid_layout.addWidget(self.progressBar, 3, 0, 1, 7)
        self.grid_layout.addWidget(self.game_list, 1, 0, 1, 6)
        self.grid_layout.addWidget(self.search_box, 0, 0, 1, 1)
        self.grid_layout.addWidget(self.search_button, 0, 3, 1, 1)
        self.grid_layout.addWidget(self.platform_search, 0, 1, 1, 2)
        self.grid_layout.setColumnStretch(0, 1)

        self.setCentralWidget(self.central_widget)

        self.menu_bar = QtWidgets.QMenuBar(self)
        self.menu_bar.setGeometry(QtCore.QRect(0, 0, 705, 21))

        self.action_directory = QtWidgets.QAction(self)
        self.action_directory.triggered.connect(self.open_settings)
        self.action_directory.setText("Directory")

        # BIOS INSTALL
        self.bios_install_menu = QtWidgets.QMenu('Install', self)
        self.bios_install_menu_3DO = QtWidgets.QAction('3DO', self)
        self.bios_install_menu_3DO.triggered.connect(partial(self.install_bios, '3DO'))
        self.bios_install_menu.addAction(self.bios_install_menu_3DO)
        self.bios_install_menu_atari7800 = QtWidgets.QAction('Atari 7800', self)
        self.bios_install_menu_atari7800.triggered.connect(partial(self.install_bios, 'Atari 7800'))
        self.bios_install_menu.addAction(self.bios_install_menu_atari7800)
        self.bios_install_menu_gba = QtWidgets.QAction('Game Boy Advance', self)
        self.bios_install_menu_gba.triggered.connect(partial(self.install_bios, 'Game Boy Advance'))
        self.bios_install_menu.addAction(self.bios_install_menu_gba)
        self.bios_install_menu_sega_genesis = QtWidgets.QAction('Sega Genesis', self)
        self.bios_install_menu_sega_genesis.triggered.connect(partial(self.install_bios, 'Sega Genesis'))
        self.bios_install_menu.addAction(self.bios_install_menu_sega_genesis)
        self.bios_install_menu_playstation = QtWidgets.QAction('Playstation', self)
        self.bios_install_menu_playstation.triggered.connect(partial(self.install_bios, 'Playstation'))
        self.bios_install_menu.addAction(self.bios_install_menu_playstation)

        self.bios_remove_menu = QtWidgets.QMenu('Remove', self)
        self.bios_remove_menu_3DO = QtWidgets.QAction('3DO', self)
        self.bios_remove_menu_3DO.triggered.connect(partial(self.remove_bios, '3DO'))
        self.bios_remove_menu.addAction(self.bios_remove_menu_3DO)
        self.bios_remove_menu_atari7800 = QtWidgets.QAction('Atari 7800', self)
        self.bios_remove_menu_atari7800.triggered.connect(partial(self.remove_bios, 'Atari 7800'))
        self.bios_remove_menu.addAction(self.bios_remove_menu_atari7800)
        self.bios_remove_menu_gba = QtWidgets.QAction('Game Boy Advance', self)
        self.bios_remove_menu_gba.triggered.connect(partial(self.remove_bios, 'Game Boy Advance'))
        self.bios_remove_menu.addAction(self.bios_remove_menu_gba)
        self.bios_remove_menu_sega_genesis = QtWidgets.QAction('Sega Genesis', self)
        self.bios_remove_menu_sega_genesis.triggered.connect(partial(self.remove_bios, 'Sega Genesis'))
        self.bios_remove_menu.addAction(self.bios_remove_menu_sega_genesis)
        self.bios_remove_menu_playstation = QtWidgets.QAction('Playstation', self)
        self.bios_remove_menu_playstation.triggered.connect(partial(self.remove_bios, 'Playstation'))
        self.bios_remove_menu.addAction(self.bios_remove_menu_playstation)

        self.menu_settings = QtWidgets.QMenu(self.menu_bar)
        self.menu_settings.setTitle("Settings")
        self.menu_settings.addAction(self.action_directory)
        self.menu_bar.addAction(self.menu_settings.menuAction())

        self.menu_bios = QtWidgets.QMenu(self.menu_bar)
        self.menu_bios.setTitle("Bios")
        self.menu_bios.addMenu(self.bios_install_menu)
        self.menu_bios.addMenu(self.bios_remove_menu)
        self.menu_bar.addAction(self.menu_bios.menuAction())

        self.setMenuBar(self.menu_bar)
        self.setting_window = widgets.DirectorySettings(self)

        self.kill_thread = False
        self.download_was_canceled = 0
        self.updated.connect(self.download_complete)
        self.set_progress.connect(self.set_progress_x)
        self.set_size_label.connect(self.change_rpi_storage_label)
        self.multi_link_total_size = 0
        self.multi_link_current_size = 0
        self.multi_file_count = 0
        self.files_canceled = 0
        self.kill_rpi_storage_thread = 0
        self.rpi_storage_thread = threading.Thread(target=self.update_rpi_storage)

        if path.get_config().getboolean('RPI', 'enabled') and self.rpi_connection():
            self.rpi_storage_thread.start()

        self.signal_kill_rpi_storage_thread.connect(self.kill_rpi_storage_loop)

    def kill_rpi_storage_loop(self):
        self.kill_rpi_storage_thread = 1

    def closeEvent(self, event):
        if self.rpi_storage_thread.is_alive():
            self.signal_kill_rpi_storage_thread.emit()
        self.deleteLater()

    def update_rpi_storage(self):
        while not self.kill_rpi_storage_thread:
            rpi_ip = path.get_config().get("RPI", 'IPAddress')
            if rpi_ip and self.rpi_connection():
                total, rd, free = shutil.disk_usage(f"//{rpi_ip}/ROMs/")
                self.set_size_label.emit(f"RPI Storage: {tools.get_size_label(free)}/{tools.get_size_label(total)}")
            time.sleep(1)

    def change_rpi_storage_label(self, string):
        self.rpi_storage_label.setText(string)

    def open_settings(self):
        self.setting_window.setModal(True)
        self.setting_window.show()

    def on_cancel_download(self):
        self.kill_thread = True

    @staticmethod
    def rpi_connection(custom_ip=None):
        ip_address = path.get_config().get('RPI', 'IPAddress')
        if custom_ip:
            ip_address = custom_ip
        if ip_address:
            try:
                socket.setdefaulttimeout(1)
                socket.socket(socket.AF_INET, socket.SOCK_STREAM).connect((ip_address, 22))
                return True
            except socket.error:
                pass

        return False

    def install_bios(self, platform):
        ip_address = path.get_config().get('RPI', 'IPAddress')

        if not ip_address:
            QtWidgets.QMessageBox.about(None, "Emuparadise Workaround", "RPI IP Address hasn't been set yet.")
            return
        else:
            if self.rpi_connection():
                error, bios_name, *reason = bios.install_bios(platform, ip_address)
                if error == 2:
                    QtWidgets.QMessageBox.about(None, "Emuparadise Workaround",
                                                f"Failed to install {bios_name} because the file already exists.")
                elif error == 1:
                    QtWidgets.QMessageBox.about(None, "Emuparadise Workaround",
                                                f"Failed to install {bios_name}. Reason: {reason}")
                else:
                    QtWidgets.QMessageBox.about(None, "Emuparadise Workaround", f"Successfully install {bios_name}.")
            else:
                QtWidgets.QMessageBox.about(None, "Emuparadise Workaround", "Could not connect to RPI.")


    def remove_bios(self, platform):
        ip_address = path.get_config().get('RPI', 'IPAddress')

        if not ip_address:
            QtWidgets.QMessageBox.about(None, "Emuparadise Workaround", "RPI IP Address hasn't been set yet.")
            return
        else:
            if self.rpi_connection():
                error, bios_name, *reason = bios.remove_bios(platform, ip_address)
                if error == 2:
                    QtWidgets.QMessageBox.about(None, "Emuparadise Workaround",
                                                f"Failed to removed {bios_name} because the file could not be found.")
                elif error == 1:
                    QtWidgets.QMessageBox.about(None, "Emuparadise Workaround",
                                                f"Failed to removed {bios_name}. Reason: {reason}")
                else:
                    QtWidgets.QMessageBox.about(None, "Emuparadise Workaround", f"Successfully removed {bios_name}.")
            else:
                QtWidgets.QMessageBox.about(None, "Emuparadise Workaround", "Could not connect to RPI.")

    def choose_dir(self, game_links, directory, platform):
        filenames = []
        total_size = 0

        for game_link in game_links:
            response = requests.get(game_link[0], headers=game_link[1], stream=True)
            decoded_url = urllib.parse.unquote(response.url)
            total_size += int(response.headers.get('content-length'))
            filename = decoded_url.split('/')[-1]
            filenames.append(filename)
            download_path = os.path.join(directory)

        download_widget = widgets.DownloadDialog()
        download_widget.setup(filenames, tools.get_size_label(total_size), platform, download_path)
        answer = download_widget.exec_()

        if answer == 0:
            return 0

        if download_widget.directory.text():
            download_path = os.path.join(download_widget.directory.text())
        else:
            if path.get_config().getint('RPI', 'enabled'):
                download_path = os.path.join(download_widget.directory.placeholderText())
            else:
                download_path = download_widget.directory.placeholderText()

        if not os.path.isdir(directory):
            msg = QtWidgets.QMessageBox()
            msg.setIcon(QtWidgets.QMessageBox.Information)
            msg.setText(f"'{directory}' doesnt exists yet.\nCreate the directory?")
            msg.setWindowTitle("Emuparadise Workaround")
            msg.setStandardButtons(QtWidgets.QMessageBox.Yes | QtWidgets.QMessageBox.No)
            choice = msg.exec_()

            if choice == QtWidgets.QMessageBox.Yes:
                os.makedirs(directory)
            else:
                return 0

        return download_path

    def on_download(self):
        if not self.game_list.currentItem():
            return

        if path.get_config().getboolean('RPI', 'enabled') and not self.rpi_connection():
            QtWidgets.QMessageBox.about(None, "Emuparadise Workaround",
                                        "RPI Mode is enabled, but cannot connect to IP Address.")
            return

        gid = tools.format_gid(int(self.game_list.currentItem().text().split(' ')[0][1:-1]))

        platform = tools.get_platform_by_gid(gid)
        game_links = []

        directory = path.get_default_directory(tools.get_platform_by_gid(gid),
                                               path.get_config().getboolean('RPI', 'enabled'))
        if path.get_config().getboolean('RPI', 'enabled'):
            directory = path.get_default_directory(tools.get_platform_by_gid(gid), True)

        if platform.lower() == 'dreamcast':
            with open(os.path.join(path.DATABASE_PATH, 'Dreamcast.json'), encoding='utf-8') as f:
                database = json.load(f)
                for key, value in database.items():
                    if str(gid) == key:
                        links = []
                        html = requests.get(value['link']).text
                        soup = bs4.BeautifulSoup(html, "html.parser")

                        for file in soup.find_all("div", class_="download-link"):
                            for x in file.find_all('p'):
                                title = x.find('a')['title']
                                filename = re.search("Download (.+?) ISO", title)
                                filename = filename.group(1)
                                link = "http://50.7.92.186/happyxhJ1ACmlTrxJQpol71nBc/Dreamcast/" + filename
                                links.append(link)

                        for x in links:
                            game_links.append([x, {"referer": x}, gid])
                f.close()

        else:
            game_links.append([tools.GAME_LINK % gid, {"referer": tools.GAME_LINK % gid}, gid])

        ask_for_dir = True
        if len(game_links) > 1:
            directory = self.choose_dir(game_links, directory, platform)
            ask_for_dir = False

        for game_link in game_links:
            response = requests.get(game_link[0], headers=game_link[1], stream=True)
            decoded_url = urllib.parse.unquote(response.url)
            filename = decoded_url.split('/')[-1]

            if ask_for_dir:
                directory = self.choose_dir(game_links, directory, platform)

            if directory == 0:
                pass
            else:
                download_path = os.path.join(directory, filename)

                total_size = int(response.headers.get('content-length'))

                self.setEnabled(False)
                self.cancel_button.setVisible(True)
                self.download_button.setVisible(False)
                self.multi_link_total_size += total_size
                self.multi_file_count += 1

                thread = threading.Thread(target=self.download_thread, args=(response, download_path))
                thread.start()


                self.setEnabled(True)

    def download_thread(self, response, download_path):
        self.download_button.setDisabled(True)
        self.search_box.setDisabled(True)
        self.search_button.setDisabled(True)

        with open(download_path, 'wb') as f:
            for block in response.iter_content(1024 ** 2):
                f.write(block)
                self.multi_link_current_size += len(block)
                self.set_progress.emit(int(self.multi_link_current_size / int(self.multi_link_total_size) * 100))

                if self.kill_thread:
                    f.close()
                    os.remove(download_path)
                    self.files_canceled += 1
                    self.download_was_canceled = 1
                    break

            if not f.closed:
                f.close()

        self.download_button.setDisabled(False)
        self.search_box.setDisabled(False)
        self.search_button.setDisabled(False)
        self.updated.emit()

    def download_complete(self):
        if self.multi_link_current_size == self.multi_link_total_size:
            self.search_box.setDisabled(False)
            self.search_button.setDisabled(False)
            self.set_progress.emit(0)
            self.cancel_button.setVisible(False)
            self.download_button.setVisible(True)
            self.download_was_canceled = 0
            QtWidgets.QMessageBox.about(None, "Emuparadise Workaround", "Download complete.")

        if self.kill_thread is True and self.files_canceled == self.multi_file_count:
            QtWidgets.QMessageBox.about(None, "Emuparadise Workaround", "The download has been canceled.")
            self.cancel_button.setVisible(False)
            self.download_button.setVisible(True)
            self.search_box.setDisabled(False)
            self.search_button.setDisabled(False)
            self.multi_link_total_size = 0
            self.download_was_canceled = 0
            self.multi_link_current_size = 0
            self.multi_file_count = 0
            self.files_canceled = 0
            self.set_progress.emit(0)
            self.kill_thread = False

    def set_progress_x(self, x):
        self.progressBar.setValue(x)

    def on_search(self):
        self.game_list.clear()
        platform = self.platform_search.currentText()
        keywords = self.search_box.text()
        items = []

        if path.get_config().getboolean('RPI', 'enabled'):
            for platform in LAKKA_SUPPORTED_PLATFORMS:
                for result in tools.get_search_results(keywords.split(' '), platform):
                    plat, gid, name = result.split(';')
                    items.append(f'[{gid}] {plat} - {name}')
        else:
            for result in tools.get_search_results(keywords.split(' '), platform):
                plat, gid, name = result.split(';')
                if platform == 'All':
                    items.append(f'[{gid}] {plat} - {name}')
                else:
                    items.append(f"[{gid}] {name}")

        self.game_list.addItems(items)


if __name__ == '__main__':
    import sys

    path.create_settings_template()
    app = QtWidgets.QApplication(sys.argv)
    main_window = EWMainWindow()
    main_window.show()
    app.exec_()
