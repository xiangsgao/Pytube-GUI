from PyQt5 import QtCore
from PyQt5.QtCore import QObject


class CustomThread(QObject):

    RUN_URL_PARSE_WORKER_SIGNAL = 'PARSE_WORKER'
    URL_PARSE_WORKER_ERROR_MESSAGE = 'Invalid url or the url is already added'

    def __init__(self):
        super().__init__()

    def run(self):
        pass

