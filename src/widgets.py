from PyQt5 import QtCore
from PyQt5 import QtWidgets

from src import path
from src import tools


class DirectorySettings(QtWidgets.QDialog):

    def __init__(self, parent=None, *args, **kwargs):
        super(DirectorySettings, self).__init__(parent, *args, **kwargs)

        self.setWindowTitle("Directory Settings")
        self.setEnabled(True)
        self.resize(355, 114)
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

        self.grid_layout = QtWidgets.QGridLayout(self)
        self.grid_layout.addWidget(self.platform_list, 0, 0, 1, 2)
        self.grid_layout.addWidget(self.directory_label, 1, 0, 1, 1)
        self.grid_layout.addWidget(self.open_directory_button, 1, 1, 1, 1)
        self.grid_layout.addWidget(self.okay_cancel_buttons, 2, 0, 1, 2)

        self.platform_list.addItem('Default')

        for platform in tools.get_platforms():
            self.platform_list.addItem(platform)

        self.changed_directories = {}

        self.on_combo_change()  # Updates the directory text

    def on_combo_change(self):
        if path.does_platform_have_path_set(self.platform_list.currentText()):
            self.directory_label.setText(path.get_default_directory(self.platform_list.currentText()))
        else:
            self.directory_label.setPlaceholderText(path.get_default_directory(self.platform_list.currentText()))
            self.directory_label.setText('')

    def on_reject(self):
        self.close()

    def on_accept(self):
        path.get_config()
        self.directory_label.setText(path.get_default_directory(self.platform_list.currentText()))
        config = path.get_config()

        for key, value in self.changed_directories.items():
            config['DIRECTORY'][key] = value

        path.write_config(config)
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
        path.get_default_directory()
        directory = path.get_default_directory(self.platform.text())
        filename = str(QtWidgets.QFileDialog.getExistingDirectory(self, 'Select a directory', directory))

        if filename:
            self.directory.setText(filename)

    def setup(self, filename, size, platform, default_directory):
        self.filename.setText(filename)
        self.size.setText(size)
        self.platform.setText(platform)
        self.directory.setPlaceholderText(default_directory)
