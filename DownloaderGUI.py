from PyQt5.QtWidgets import QMainWindow
from PyQt5.QtWidgets import QWidget
from PyQt5.QtWidgets import QVBoxLayout
from PyQt5.QtWidgets import QHBoxLayout
from PyQt5.QtWidgets import QLineEdit
from PyQt5.QtWidgets import QPushButton
from PyQt5.QtWidgets import QCheckBox
from PyQt5.QtWidgets import QListWidget
from Downloader import Downloader
from PyQt5.QtWidgets import QLabel
from PyQt5.QtWidgets import QMessageBox
from PyQt5.Qt import Qt
from PyQt5.QtWidgets import QFileDialog

class DownloaderMainWindow(QMainWindow):

    def __init__(self,   download_manager=Downloader()):
        super().__init__()
        self.setWindowTitle("PyTube Downloader")
        self.__download_manager = download_manager

        # ui contains all the widgets for the main window, just like in qt creator lol
        self.__ui = self.UI(self)

        # makes sure the downloaded directory can't not be manually edited. This ensures the user chooses a valid path with browse button
        self.__ui.dir_line_edit.setText(self.__download_manager.get_download_directory())
        self.__ui.dir_line_edit.setReadOnly(True)
        self.setCentralWidget(self.__ui)

        # listener for the buttons
        self.__ui.add_button.clicked.connect(self.add_button_clicked)
        self.__ui.remove_button.clicked.connect(self.remove_button_clicked)
        self.__ui.browse_button.clicked.connect(self.browse_button_clicked)

        # hide the video list and download button because they will be empty
        self.hide_list()


        # this autoresizes
        # self.resize(self.layout().sizeHint())


    def show_list(self):
        self.__ui.video_list.show()
        self.__ui.download_button.show()

    def hide_list(self):
        self.__ui.video_list.hide()
        self.__ui.download_button.hide()

    def add_button_clicked(self):
            if (len(self.__ui.video_list.findItems(self.__ui.url_line_edit.text(), Qt.MatchExactly))==0) and (self.__ui.url_line_edit.text() != ""):
                self.__ui.video_list.addItem(self.__ui.url_line_edit.text())
            else:
                QMessageBox.about(self, "Alert", "This link is added already or the link is invalid")
                return
            if self.__ui.download_button.isHidden():
                self.show_list()

    def remove_button_clicked(self):
            if self.__ui.video_list.currentItem() is None:
                QMessageBox.about(self, "Alert", "You need to select an item in the video list")
                return
            selectedItem = self.__ui.video_list.currentItem()
            self.__ui.video_list.takeItem(self.__ui.video_list.row(selectedItem))
            self.__ui.video_list.setCurrentItem(None)
            self.__ui.video_list.clearFocus()

    def browse_button_clicked(self):
         dir = QFileDialog.getExistingDirectory(parent=self, directory=self.__download_manager.get_download_directory(), options=QFileDialog.DontResolveSymlinks)
         if dir != "":
            self.__ui.dir_line_edit.setText(dir)
            self.__download_manager.set_download_directory(dir)




    class UI(QWidget):

        def __init__(self, parent):
            super().__init__(parent)
            self.layout = QVBoxLayout()
            self.init_gui()
            self.setLayout(self.layout)


        def init_gui(self):
            # set up first h box items
            self.h_box1 = QHBoxLayout()
            self.paste_label = QLabel('Paste Web page here: ')
            self.url_line_edit = QLineEdit()
            self.url_line_edit.setMaximumWidth(300);
            self.url_line_edit.setFixedWidth(310);
            self.h_box1.addWidget(self.paste_label)
            self.h_box1.addWidget(self.url_line_edit)
            self.layout.addLayout(self.h_box1)

            # set up 2nd h box items
            self.h_box2 = QHBoxLayout()
            self.dir_line_edit = QLineEdit()
            self.browse_button = QPushButton('Browse')
            self.h_box2.addWidget(self.browse_button)
            self.h_box2.addWidget(self.dir_line_edit)
            self.layout.addLayout(self.h_box2)

            # set up third h box items
            self.h_box3 = QHBoxLayout()
            self.checkbox = QCheckBox('mp3 only')
            self.add_button = QPushButton('Add')
            self.remove_button = QPushButton('Remove')
            self.h_box3.addStretch(1);
            self.h_box3.addWidget(self.checkbox)
            self.h_box3.addWidget(self.add_button)
            self.h_box3.addWidget(self.remove_button)
            self.layout.addLayout(self.h_box3)

            # set up added video lists and download button
            self.download_button = QPushButton('Download')
            self.video_list = QListWidget(self)
            self.layout.addWidget(self.video_list)
            self.layout.addWidget(self.download_button)

