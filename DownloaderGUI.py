import threading

from PyQt5 import QtCore
from PyQt5.QtCore import QObject
from PyQt5.QtWidgets import QMainWindow, QLayout, QListWidgetItem
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
from PyQt5.QtWidgets import QFileDialog
from ThreadWorker import ParserWorker
import time

class DownloaderMainWindow(QMainWindow, QObject):

    # the parameters are the type of object to be passed into the function the ui thread is going to execute, in this case just something to modify the widgets
    # because we can only do so in ui thread
    PARSE_URL_SIGNAL = QtCore.pyqtSignal(QListWidgetItem, str)

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

        # listener for the widgets
        self.__ui.add_button.clicked.connect(self.add_button_clicked)
        self.__ui.remove_button.clicked.connect(self.remove_button_clicked)
        self.__ui.browse_button.clicked.connect(self.browse_button_clicked)
        self.__ui.checkbox.clicked.connect(self.mp3_checked_clicked)
        self.__ui.download_button.clicked.connect(self.download_button_clicked)

        # hide the video list and download button because they will be empty
        self.hide_list()

        # connecting the signal with this parse_url_function so whenever it is emitted from another thread, this function will be executed in the ui thread.
        self.PARSE_URL_SIGNAL.connect(self.set_list_widget_text)
        self.__threads = []
        self.__parsing_waitlist = []






    def download_button_clicked(self):
        if len(self.__parsing_waitlist) != 0:
            print(str(len(self.__parsing_waitlist)))
            QMessageBox.about(self, "Alert", "Wait for urls to finish parsing. Also remove the invalid and duplicated links first.")
            return
        # using native python thread to spun downloads. QThread is a pain in the ass
        thread = threading.Thread(target=self.__download_button_thread_function, name='Download button clicked thread',args=())
        thread.start()

    def __download_button_thread_function(self):
        print('\nStarting download in parallel.....')
        # disables all the control until download finishes
        self.__ui.add_button.setEnabled(False)
        self.__ui.remove_button.setEnabled(False)
        self.__ui.browse_button.setEnabled(False)
        self.__ui.download_button.setEnabled(False)
        self.__ui.download_button.setText('Downloading.....')
        self.__ui.checkbox.setEnabled(False)
        # download
        self.__download_manager.download_in_parallel()
        # turn control back on once the download manager finishes downloading
        while self.__download_manager.get_number_of_downloads_in_progress() == 0:
            time.sleep(1)
        self.__ui.add_button.setEnabled(True)
        self.__ui.remove_button.setEnabled(True)
        self.__ui.browse_button.setEnabled(True)
        self.__ui.download_button.setEnabled(True)
        self.__ui.download_button.setText('Download')
        self.__ui.checkbox.setEnabled(True)
        print('\nDone!')





    def show_list(self):
        self.__ui.video_list.show()
        self.__ui.download_button.show()

    def hide_list(self):
        self.__ui.video_list.hide()
        self.__ui.download_button.hide()


    def add_button_clicked(self):
        self.__ui.video_list.addItem("Parsing url...")
        item_position =  self.__ui.video_list.count() - 1
        item = self.__ui.video_list.item(item_position)
        name = self.__ui.url_line_edit.text()
        if self.__ui.download_button.isHidden():
            self.show_list()

        # add the video to the wait list so download button knows if its url is invalid or still waiting to be parse
        self.__parsing_waitlist.append(item)

        # creating the parser worker which can emit signals for ui thead to update widgets, also need to scope it to an instance else thread will malfunction lol, fuck python
        self.worker = ParserWorker(item, name, self)
        # creating thread object
        thread = QtCore.QThread()
        # add threads to the thread list because pyqt5 will annoyingly destroy ui thread if the thread object is garbabged collected cuz these threads do not die for some reason
        self.__threads.append(thread)
        # moved worker to a thread so workers work is multithreaded
        self.worker.moveToThread(thread)
        # have thread execute worker's work whenever it is started
        thread.started.connect(self.worker.run)
        # start the worker
        thread.start()


    def parse_Url_Function(self, item, url):
        video_name = self.__download_manager.add_video(url)
        # remove the video from the wait list because its link is successfully parsed
        print('url parsing is successful!')
        self.__parsing_waitlist.remove(item)
        return video_name

    def set_list_widget_text(self, item, text):
        item.setText(text)

    def remove_button_clicked(self):
            if self.__ui.video_list.currentItem() is None:
                QMessageBox.about(self, "Alert", "You need to select an item in the video list")
                return
            selectedItem = self.__ui.video_list.currentItem()
            self.__ui.video_list.takeItem(self.__ui.video_list.row(selectedItem))
            self.__download_manager.remove_video(selectedItem.text())
            if selectedItem in self.__parsing_waitlist:
                self.__parsing_waitlist.remove(selectedItem)
            self.__ui.video_list.setCurrentItem(None)
            self.__ui.video_list.clearFocus()
            if self.__ui.video_list.count() == 0:
                self.hide_list()


    def browse_button_clicked(self):
         dir = QFileDialog.getExistingDirectory(parent=self, directory=self.__download_manager.get_download_directory(), options=QFileDialog.DontResolveSymlinks)
         if dir != "":
            self.__ui.dir_line_edit.setText(dir)
            self.__download_manager.set_download_directory(dir)

    def mp3_checked_clicked(self):
        self.__download_manager.mp3_mode_on(self.__ui.checkbox.isChecked());





    class UI(QWidget):

        def __init__(self, parent):
            super().__init__(parent)
            self.layout = QVBoxLayout()
            # fixed the size constraint
            self.layout.setSizeConstraint(QLayout.SetFixedSize);
            self.init_gui()
            self.setLayout(self.layout)
            self.layoutsize = self.size()


        def init_gui(self):
            # set up first h box items
            self.h_box1 = QHBoxLayout()
            self.paste_label = QLabel('Paste the youtube url here: ')
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

