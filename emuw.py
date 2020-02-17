import os
import threading
import urllib

import requests
from PyQt5 import QtCore
from PyQt5 import QtWidgets

from src import path
from src import tools
from src import widgets


class EWMainWindow(QtWidgets.QMainWindow):
    updated = QtCore.pyqtSignal()
    set_progress = QtCore.pyqtSignal(int)

    def __init__(self, *args, **kwargs):
        QtWidgets.QMainWindow.__init__(self)
        self.setWindowTitle("Emuparadise Workaround")
        self.resize(705, 452)
        self.setBaseSize(QtCore.QSize(480, 400))
        self.setAutoFillBackground(False)
        self.setIconSize(QtCore.QSize(24, 24))
        self.statusBar = QtWidgets.QStatusBar(self)
        self.setStatusBar(self.statusBar)

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

        self.result_count = QtWidgets.QLabel(self.central_widget)

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
        self.platform_search.addItems([platform for platform in tools.get_platforms()])

        self.grid_layout = QtWidgets.QGridLayout(self.central_widget)
        self.grid_layout.setContentsMargins(9, -1, -1, -1)
        self.grid_layout.addWidget(self.download_button, 2, 0, 1, 1)
        self.grid_layout.addWidget(self.cancel_button, 2, 0, 1, 1)
        self.grid_layout.addWidget(self.result_count, 2, 2, 1, 1)
        self.grid_layout.addWidget(self.progressBar, 3, 0, 1, 7)
        self.grid_layout.addWidget(self.game_list, 1, 0, 1, 6)
        self.grid_layout.addWidget(self.search_box, 0, 0, 1, 1)
        self.grid_layout.addWidget(self.search_button, 0, 3, 1, 1)
        self.grid_layout.addWidget(self.platform_search, 0, 1, 1, 2)
        self.grid_layout.setColumnStretch(0, 1)

        self.setCentralWidget(self.central_widget)

        self.menu_bar = QtWidgets.QMenuBar(self)
        self.menu_bar.setGeometry(QtCore.QRect(0, 0, 705, 21))
        self.menu_settings = QtWidgets.QMenu(self.menu_bar)
        self.menu_settings.setTitle("Settings")
        self.menu_help = QtWidgets.QMenu(self.menu_bar)
        self.setMenuBar(self.menu_bar)
        self.action_directory = QtWidgets.QAction(self)
        self.action_directory.triggered.connect(self.open_settings)
        self.action_directory.setText("Directory")
        self.menu_settings.addAction(self.action_directory)
        self.menu_bar.addAction(self.menu_settings.menuAction())
        self.menu_bar.addAction(self.menu_help.menuAction())

        self.setting_window = widgets.DirectorySettings(self)

        self.kill_thread = False
        self.download_was_canceled = 0

        self.updated.connect(self.download_complete)
        self.set_progress.connect(self.set_progress_x)

    def open_settings(self):
        self.setting_window.setModal(True)
        self.setting_window.show()

    def on_cancel_download(self):
        self.kill_thread = True

    def on_download(self):
        if not self.game_list.currentItem():
            return

        gid = tools.format_gid(int(self.game_list.currentItem().text().split('\t')[0][1:-1]))
        directory = path.get_default_directory(tools.get_platform_by_gid(gid))
        game_link = tools.GAME_LINK % gid, {"referer": tools.GAME_LINK % gid}
        response = requests.get(game_link[0], headers=game_link[1], stream=True)
        decoded_url = urllib.parse.unquote(response.url)
        filename = decoded_url.split('/')[-1]
        download_path = os.path.join(directory, filename)

        if tools.check_bad_id(filename, gid):
            return

        size = tools.get_size_label(int(response.headers.get('content-length')))
        download_widget = widgets.DownloadDialog()
        download_widget.setup(filename, size, tools.get_platform_by_gid(gid), download_path)
        answer = download_widget.exec_()

        if answer == 0:
            return

        if download_widget.directory.text():
            download_path = os.path.join(download_widget.directory.text(), filename)
        else:
            download_path = download_widget.directory.placeholderText()

        if os.path.exists(download_path):
            msg = QtWidgets.QMessageBox()
            msg.setIcon(QtWidgets.QMessageBox.Information)
            msg.setText(f"'{os.path.abspath(download_path)}' already exists.\nOverwrite the file?")
            msg.setWindowTitle("Emuparadise Workaround")
            msg.setStandardButtons(QtWidgets.QMessageBox.Yes | QtWidgets.QMessageBox.No)
            choice = msg.exec_()
            if choice == QtWidgets.QMessageBox.No:
                return

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
                return

        self.setEnabled(False)
        self.cancel_button.setVisible(True)
        self.download_button.setVisible(False)
        thread = threading.Thread(target=self.download_thread, args=(response, download_path))
        thread.start()

        self.setEnabled(True)

    def download_complete(self):
        if self.download_was_canceled:
            QtWidgets.QMessageBox.about(None, "Emuparadise Workaround", "The download has been canceled.")
            self.cancel_button.setVisible(False)
            self.download_button.setVisible(True)
        else:
            QtWidgets.QMessageBox.about(None, "Emuparadise Workaround", "The download is complete.")
            self.cancel_button.setVisible(False)
            self.download_button.setVisible(True)

        self.download_was_canceled = 0

    def download_thread(self, response, download_path):
        total_size = response.headers.get('content-length')
        self.download_button.setDisabled(True)
        self.search_box.setDisabled(True)
        self.search_button.setDisabled(True)
        current_size = 0

        with open(download_path, 'wb') as f:
            for block in response.iter_content(1024 ** 2):
                f.write(block)
                current_size += len(block)
                self.set_progress.emit(int(current_size / int(total_size) * 100))

                if self.kill_thread:
                    f.close()
                    os.remove(download_path)
                    self.kill_thread = False
                    self.download_was_canceled = 1
                    break

            if not f.closed:
                f.close()

        self.download_button.setDisabled(False)
        self.search_box.setDisabled(False)
        self.search_button.setDisabled(False)
        self.set_progress.emit(0)
        self.updated.emit()

    def set_progress_x(self, x):
        self.progressBar.setValue(x)

    def on_search(self):
        self.game_list.clear()
        platform = self.platform_search.currentText()
        keywords = self.search_box.text()
        items = []

        for result in tools.get_search_results(keywords.split(' '), platform):
            plat, gid, name = result.split(';')

            if platform == 'All':
                items.append(f'[{gid}]\t{plat} - {name}')
            else:
                items.append(f"[{gid}]\t{name}")

        self.result_count.setText(f"{len(items)} Results")
        self.game_list.addItems(items)


if __name__ == '__main__':
    import sys

    path.create_settings_template()
    app = QtWidgets.QApplication(sys.argv)
    main_window = EWMainWindow()
    main_window.show()
    app.exec_()
