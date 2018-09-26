from PyQt5.QtWidgets import QMainWindow
from Downloader import Downloader

class Downloader_Main_Window(QMainWindow):

    def __init__(self,  download_manager):
        super().__init__()
        self.setWindowTitle("PyTube Downloader")
        self.resize(800, 600)
        self.__download_manager = download_manager
        self.__init_layout()


    def __init_layout(self):
        pass
