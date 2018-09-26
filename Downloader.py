#!/usr/bin/python
import pytube
import os
import subprocess

class Downloader:

    def __init__(self):
        self.__yt = None
        self.__choice = 0
        self.__mp3_mode = False
        self.__directory = None
        self.__vids = None

    def set_url(self, url):
        self.__yt = pytube.YouTube(url)

    def set_download_directory(self, directory):
        self.__directory = directory

    def mp3_mode_on(self, value):
        self.__mp3_mode = value

    def display_download_choices(self):
        self.__vids = self.yt.streams.all()
        choice_list = [None] * len(self.vids)
        for i in range(len(self.vids)):
            choice_list[i] = str(print(i, '. ', self.vids[i]))
        return list

    def set_video_choice(self, choice):
        self.__choice = choice

    def download(self):
        if not self.all_set():
            print("\nneed to set path or url")
            return False

        self.vids[self.choice].download(self.directory)
        downloaded_file_name = self.vids[self.choice].default_filename
        if self.mp3_mode is True:
            new_filename = downloaded_file_name[:-4] + '.mp3'
            subprocess.run(['ffmpeg', '-i',  # or subprocess.run (Python 3.5+)
                os.path.join(self.directory, downloaded_file_name),
                os.path.join(self.directory, new_filename)
            ])
            subprocess.run(['rm', os.path.join(self.directory, downloaded_file_name)])
            return True

    def all_set(self):
        return self.__yt is not None and self.__directory is not None






# downloader = Downloader('https://www.youtube.com/watch?v=9bZkp7q19f0')
# downloader.set_download_directory('/home/xgao/Downloads/')
# downloader.mp3_mode_on(True)
# print(downloader.display_download_choices())
# downloader.set_video_choice(0)
# downloader.download()

