from PyQt5 import QtCore
from PyQt5 import QtWidgets

from emuw import path
from emuw import tools


class DirectorySettings(QtWidgets.QDialog):

    def __init__(self, parent=None, *args, **kwargs):
        super(DirectorySettings, self).__init__(parent, *args, **kwargs)

        self.setWindowTitle("Directory Settings")
        self.setEnabled(True)
        self.resize(355, 130)
        self.setFixedSize(self.size())

        self.platform_list = QtWidgets.QComboBox(self)
        self.platform_list.currentTextChanged.connect(self.on_combo_change)

        self.directory_label = QtWidgets.QLineEdit(self)
        self.directory_label.setReadOnly(True)

        self.open_directory_button = QtWidgets.QToolButton(self)
        self.open_directory_button.setText("...")
        self.open_directory_button.clicked.connect(self.choose_path)

        self.okay_cancel_buttons = QtWidgets.QDialogButtonBox(self)
        self.okay_cancel_buttons.setStandardButtons(QtWidgets.QDialogButtonBox.Cancel | QtWidgets.QDialogButtonBox.Ok)
        self.okay_cancel_buttons.accepted.connect(self.on_accept)
        self.okay_cancel_buttons.rejected.connect(self.on_reject)

        self.rpi_config = QtWidgets.QCheckBox("RPI Mode", self)
        self.rpi_config.stateChanged.connect(self.on_rpi_config_change)

        self.rpi_ip = QtWidgets.QLineEdit(self)
        self.rpi_ip.setPlaceholderText("RPI IP Address")
        self.rpi_ip.setFixedWidth(100)
        self.rpi_ip.setDisabled(True)

        self.grid_layout = QtWidgets.QGridLayout(self)
        self.grid_layout.addWidget(self.platform_list, 0, 0, 1, 2)
        self.grid_layout.addWidget(self.directory_label, 1, 0, 1, 1)
        self.grid_layout.addWidget(self.open_directory_button, 1, 1, 1, 1)
        self.grid_layout.addWidget(self.okay_cancel_buttons, 3, 0, 1, 2)
        self.grid_layout.addWidget(self.rpi_config, 2, 0, 1, 1)
        self.grid_layout.addWidget(self.rpi_ip, 3, 0, 1, 1)
        self.changed_directories = {}
        self.initialize()

    def initialize(self):
        self.platform_list.addItem('Default')
        for platform in tools.get_platforms():
            self.platform_list.addItem(platform)

        config = path.get_config()
        ip_address = config['RPI']['IPAddress']
        is_enabled = bool(int(config['RPI']['enabled']))
        self.rpi_ip.setText(ip_address)

        if is_enabled:
            self.rpi_config.setChecked(True)
            self.rpi_ip.setDisabled(False)
            self.open_directory_button.setDisabled(True)
        else:
            self.rpi_config.setChecked(False)
            self.rpi_ip.setDisabled(True)
            self.open_directory_button.setDisabled(False)

        self.on_combo_change()

    def on_rpi_config_change(self):
        if self.rpi_config.isChecked():
            self.rpi_ip.setDisabled(False)
            self.open_directory_button.setDisabled(True)
        elif not self.rpi_config.isChecked():
            self.rpi_ip.setDisabled(True)
            self.open_directory_button.setDisabled(False)
        self.on_combo_change()

    def on_combo_change(self):
        if self.rpi_config.isChecked():
            self.directory_label.setText('')
            self.directory_label.setPlaceholderText(path.get_default_directory(self.platform_list.currentText(), True))
        else:
            if path.does_platform_have_path_set(self.platform_list.currentText()):
                self.directory_label.setText(path.get_default_directory(self.platform_list.currentText()))
            else:
                self.directory_label.setPlaceholderText(path.get_default_directory(self.platform_list.currentText()))
                self.directory_label.setText('')

    def on_reject(self):
        self.close()

    def on_accept(self):

        config = path.get_config()
        can_close = True
        config['RPI']['enabled'] = '0'
        if self.rpi_config.isChecked():
            if not self.rpi_ip.text():
                can_close = False
                QtWidgets.QMessageBox.about(None, "Emuparadise Workaround",
                                            "No IP Address is set and RPI config is checked..")
            else:
                config['RPI']['enabled'] = '1'
                config['RPI']['IPAddress'] = self.rpi_ip.text()
                if not self.parent().rpi_connection(self.rpi_ip.text()):
                    QtWidgets.QMessageBox.about(None, "Emuparadise Workaround", "RPI Mode is enabled, but cannot connect to IP Address.")
                    can_close = False
                if not self.parent().rpi_storage_thread.is_alive() and self.parent().rpi_connection():
                    self.parent().rpi_storage_thread.start()

        self.directory_label.setText(path.get_default_directory(self.platform_list.currentText()))
        for key, value in self.changed_directories.items():
            config['DIRECTORY'][key] = value
        path.write_config(config)
        rpi_enalbed = path.get_config().getboolean('RPI', 'enabled')
        rpi_label = f"RPI ENABLED: {rpi_enalbed}"
        if not self.parent().rpi_enabled.text() == rpi_enalbed:
            self.parent().game_list.clear()
        self.parent().rpi_enabled.setText(rpi_label)

        if can_close:
            self.close()

    def choose_path(self):
        directory = path.get_default_directory(self.platform_list.currentText())
        filename = str(QtWidgets.QFileDialog.getExistingDirectory(self, 'Select a directory', directory))

        if filename:
            self.changed_directories[self.platform_list.currentText()] = filename
            self.directory_label.setText(filename)


class DownloadDialog(QtWidgets.QDialog):

    def __init__(self, *args, **kwargs):
        super(DownloadDialog, self).__init__(*args, **kwargs)

        self.setWindowTitle("Download")
        self.resize(480, 124)
        self.setMinimumSize(QtCore.QSize(480, 124))
        self.setMaximumSize(QtCore.QSize(1920, 124))
        self.setBaseSize(QtCore.QSize(480, 124))

        self.filename_label = QtWidgets.QLabel(self)
        self.filename_label.setText("Filename")

        self.filename = QtWidgets.QLabel(self)

        self.platform_label = QtWidgets.QLabel(self)
        self.platform_label.setText("Platform")

        self.platform = QtWidgets.QLabel(self)
        self.size_label = QtWidgets.QLabel(self)
        self.size_label.setText("Size")
        self.size = QtWidgets.QLabel(self)
        self.directory_label = QtWidgets.QLabel(self)
        self.directory_label.setText("Directory")

        self.directory = QtWidgets.QLineEdit(self)
        self.directory.setReadOnly(True)

        self.choose_directory_button = QtWidgets.QToolButton(self)
        self.choose_directory_button.setText("...")
        self.choose_directory_button.clicked.connect(self.open)

        self.yes_no_button = QtWidgets.QDialogButtonBox(self)
        self.yes_no_button.setStandardButtons(QtWidgets.QDialogButtonBox.Cancel | QtWidgets.QDialogButtonBox.Save)
        self.yes_no_button.accepted.connect(self.accept)
        self.yes_no_button.rejected.connect(self.reject)

        self.grid_layout = QtWidgets.QGridLayout(self)
        self.grid_layout.addWidget(self.filename_label, 0, 0, 1, 1)
        self.grid_layout.addWidget(self.platform_label, 1, 0, 1, 1)
        self.grid_layout.addWidget(self.choose_directory_button, 3, 3, 1, 1)
        self.grid_layout.addWidget(self.filename, 0, 1, 1, 2)
        self.grid_layout.addWidget(self.size_label, 2, 0, 1, 1)
        self.grid_layout.addWidget(self.yes_no_button, 4, 2, 1, 2)
        self.grid_layout.addWidget(self.directory_label, 3, 0, 1, 1)
        self.grid_layout.addWidget(self.directory, 3, 1, 1, 2)
        self.grid_layout.addWidget(self.platform, 1, 1, 1, 2)
        self.grid_layout.addWidget(self.size, 2, 1, 1, 2)

    def open(self):
        directory = path.get_default_directory(self.platform.text())
        filename = str(QtWidgets.QFileDialog.getExistingDirectory(self, 'Select a directory', directory))

        if filename:
            self.directory.setText(filename)

    def setup(self, filenames, size, platform, default_directory):
        self.filename.setText(', '.join(filenames))
        self.size.setText(size)
        self.platform.setText(platform)

        if int(path.get_config()['RPI']['enabled']):
            self.directory.setPlaceholderText(path.get_default_directory(self.platform.text(), True))
            self.directory.setText('')
            self.choose_directory_button.setDisabled(True)
        else:
            self.directory.setPlaceholderText(default_directory)
