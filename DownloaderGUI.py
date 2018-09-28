from PyQt5.QtWidgets import QMainWindow
from PyQt5.QtWidgets import QWidget
from PyQt5.QtWidgets import QVBoxLayout
from PyQt5.QtWidgets import QHBoxLayout
from PyQt5.QtWidgets import QLineEdit
from PyQt5.QtWidgets import QPushButton
from PyQt5.QtWidgets import QCheckBox
from Downloader import Downloader
from PyQt5.QtWidgets import QLabel

class Downloader_Main_Window(QMainWindow):

    def __init__(self,   download_manager=Downloader):
        super().__init__()
        self.setWindowTitle("PyTube Downloader")
        self.__download_manager = download_manager
        self.__ui = self.UI(self)
        self.setCentralWidget(self.__ui)
        # this autoresizes
        #self.resize(self.layout().sizeHint())


    class UI(QWidget):

        def __init__(self, parent):
            super().__init__(parent)
            self.layout = QVBoxLayout()
            self.init_gui()
            self.setLayout(self.layout)


        def init_gui(self):
            self.Hbox1 = QHBoxLayout()
            self.pasteLabel = QLabel('Paste Web page here: ')
            self.urlLineEdit = QLineEdit()
            self.urlLineEdit.setMaximumWidth(300);
            self.urlLineEdit.setFixedWidth(310);
            self.Hbox1.addWidget(self.pasteLabel)
            self.Hbox1.addWidget(self.urlLineEdit)
            self.layout.addLayout(self.Hbox1)
            self.Hbox2 = QHBoxLayout()
            self.dirLineEdit = QLineEdit()
            self.browseButton = QPushButton('Browse')
            self.Hbox2.addWidget(self.dirLineEdit)
            self.Hbox2.addWidget(self.browseButton)
            self.layout.addLayout(self.Hbox2)
            self.Hbox3 = QHBoxLayout()
            self.checkbox = QCheckBox('mp3 only')
            self.downloadButton = QPushButton('Download')
            self.Hbox3.addStretch(1);
            self.Hbox3.addWidget(self.checkbox)
            self.Hbox3.addWidget(self.downloadButton)
            self.layout.addLayout(self.Hbox3)
