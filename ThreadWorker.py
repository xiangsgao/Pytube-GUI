from PyQt5.QtCore import QObject, pyqtSignal
import threading

class ParserWorker(QObject):
    finished = pyqtSignal()

    # app in this case is the DownloaderGUI.MainWindow and arg1 is the QListWidgetItem, and the arg2 is the url passed from the url line edit
    def __init__(self, arg1, arg2, app):
        super().__init__()
        self.__arg1 = arg1
        self.__arg2 = arg2
        self.__app = app

    def run(self):
        thread_name = threading.current_thread().name
        print('\nCreating the thread ' + thread_name + ' for a ' + 'parser worker working on url ' + self.__arg2)
        print('Running the url parser worker....')
        try:
            video_name = self.__app.parse_Url_Function(self.__arg1, self.__arg2)
            self.__app.PARSE_URL_SIGNAL.emit(self.__arg1, video_name)
        except Exception as e:
            print('Encountered error while parsing url: ' + str(e))
            self.__app.PARSE_URL_SIGNAL.emit(self.__arg1 ,'Invalid or duplicated Url: ' + self.__arg2)
        finally:
            print('Terminating the url parser worker')


