from PyQt5.QtWidgets import QMainWindow
from PyQt5.QtWidgets import QWidget
from PyQt5.QtWidgets import QVBoxLayout
from PyQt5.QtWidgets import QHBoxLayout
from PyQt5.QtWidgets import QLineEdit
from PyQt5.QtWidgets import QPushButton
from PyQt5.QtWidgets import QCheckBox
from Downloader import Downloader
from PyQt5.QtWidgets import QLabel

class DownloaderMainWindow(QMainWindow):

    def __init__(self,   download_manager=Downloader()):
        super().__init__()
        self.setWindowTitle("PyTube Downloader")
        self.__download_manager = download_manager
        self.__ui = self.UI(self)

        # makes sure the downloaded directory can't not be manually edited. This ensures the user chooses a valid path with browse button
        self.__ui.dir_line_edit.setText(self.__download_manager.get_download_directory())
        self.__ui.dir_line_edit.setReadOnly(True)
        self.setCentralWidget(self.__ui)
        # this autoresizes
        # self.resize(self.layout().sizeHint())


    class UI(QWidget):

        def __init__(self, parent):
            super().__init__(parent)
            self.layout = QVBoxLayout()
            self.init_gui()
            self.setLayout(self.layout)


        def init_gui(self):
            self.h_box1 = QHBoxLayout()
            self.paste_label = QLabel('Paste Web page here: ')
            self.url_line_edit = QLineEdit()
            self.url_line_edit.setMaximumWidth(300);
            self.url_line_edit.setFixedWidth(310);
            self.h_box1.addWidget(self.paste_label)
            self.h_box1.addWidget(self.url_line_edit)
            self.layout.addLayout(self.h_box1)

            self.h_box2 = QHBoxLayout()
            self.dir_line_edit = QLineEdit()
            self.browse_button = QPushButton('Browse')
            self.h_box2.addWidget(self.browse_button)
            self.h_box2.addWidget(self.dir_line_edit)
            self.layout.addLayout(self.h_box2)

            self.h_box3 = QHBoxLayout()
            self.checkbox = QCheckBox('mp3 only')
            self.download_button = QPushButton('Download')
            self.h_box3.addStretch(1);
            self.h_box3.addWidget(self.checkbox)
            self.h_box3.addWidget(self.download_button)
            self.layout.addLayout(self.h_box3)
