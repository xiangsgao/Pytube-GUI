from PyQt5.QtWidgets import QMainWindow
from PyQt5.QtWidgets import QWidget
from PyQt5.QtWidgets import QVBoxLayout
from Downloader import Downloader
from PyQt5.QtWidgets import QLabel

class Downloader_Main_Window(QMainWindow):

    def __init__(self,   download_manager=Downloader):
        super().__init__()
        self.setWindowTitle("PyTube Downloader")
        self.resize(800, 600)
        self.__download_manager = download_manager
        self.__ui = self.UI(self)
        self.setCentralWidget(self.__ui)


    class UI(QWidget):

        def __init__(self, parent):
            super().__init__(parent)
            self.__layout = QVBoxLayout()
            self.__label = QLabel('Hello World')
            self.__layout.addWidget(self.__label)
            self.setLayout(self.__layout)

