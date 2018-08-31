#!/usr/bin/python
import pytube
import os
import subprocess

class Downloader:


    def __init__(self, url = None):
        if url is not None:
            self.yt = pytube.YouTube(url)

    def set_url(self, url):
        self.yt = pytube.YouTube(url)

    def set_download_directory(self, directory):
        self.directory = directory

    def mp3_mode_on(self, value):
        self.mp3_mode = value

    def display_download_choices(self):
        self.vids = self.yt.streams.all()
        choice_list = [None] * len(self.vids)
        for i in range(len(self.vids)):
            choice_list[i] = str(print(i, '. ', self.vids[i]))
        return list

    def set_video_choice(self, choice):
        self.choice = choice

    def download(self):
        self.vids[self.choice].download(self.directory)
        downloaded_file_name = self.vids[self.choice].default_filename
        if self.mp3_mode is True:
            new_filename = downloaded_file_name[:-4] + '.mp3'
            subprocess.run(['ffmpeg', '-i',  # or subprocess.run (Python 3.5+)
                os.path.join(self.directory, downloaded_file_name),
                os.path.join(self.directory, new_filename)
            ])
            subprocess.run(['rm', os.path.join(self.directory, downloaded_file_name)])












        # yt = pytube.YouTube("https://www.youtube.com/watch?v=9bZkp7q19f0")
#
# vids = yt.streams.all()
# for i in range(len(vids)):
#     print(i,'. ',vids[i])
#
# choice_number = int(input("Enter video number you wished to download: "))
# downloaded_dir = '/home/xgao/Downloads/'
# vids[choice_number].download(downloaded_dir)
# downloaded_file_name = vids[choice_number].default_filename  # get default name using pytube API
#
# new_filename = input("Enter your new file name for conversion, including the extension\n")  # e.g. new_filename.mp3
#
# original_downloaded_file_name = vids[choice_number].default_filename  # get default name using pytube API
# subprocess.call(['ffmpeg', '-i',                # or subprocess.run (Python 3.5+)
#     os.path.join(downloaded_dir, original_downloaded_file_name),
#     os.path.join(downloaded_dir, new_filename)
# ])
#
# print('done')


downloader = Downloader('https://www.youtube.com/watch?v=9bZkp7q19f0')
downloader.set_download_directory('/home/xgao/Downloads/')
downloader.mp3_mode_on(True)
print(downloader.display_download_choices())
downloader.set_video_choice(0)
downloader.download()

