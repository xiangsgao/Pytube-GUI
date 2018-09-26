import Downloader
from DownloaderGUI import Downloader_Main_Window
from PyQt5 import QtWidgets
import sys

def main():
    app = QtWidgets.QApplication(sys.argv)
    downloader_manager = Downloader.Downloader()
    window = Downloader_Main_Window(downloader_manager)
    window.show()
    sys.exit(app.exec())




if __name__ == '__main__':
    main()