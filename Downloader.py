import pytube
import os
import subprocess

class Downloader:

    # constructor
    def __init__(self):
        self.__yt = None
        self.__choice = 0
        self.__mp3_mode = False
        self.__directory = self.get_download_path()
        self.__vids = None

    # sets the video to download by its url
    def set_url(self, url):
        self.__yt = pytube.YouTube(url)

    # sets a custom download directory
    def set_download_directory(self, directory):
        self.__directory = directory

    #sets if the just downlaod mp3
    def mp3_mode_on(self, value):
        self.__mp3_mode = value

    # dipplasy download choices
    def display_download_choices(self):
        self.__vids = self.__yt.streams.all()
        choice_list = [None] * len(self.__vids)
        for i in range(len(self.__vids)):
            choice_list[i] = str(print(i, '. ', self.__vids[i]))
        return list

    # sets the video choices
    def set_video_choice(self, choice):
        self.__choice = choice


    # checks if the url is set
    def all_set(self):
        return self.__yt is not None

    # Returns the default downloads path for linux or windows
    def get_download_path(self):
        if os.name == 'nt':
            import winreg
            sub_key = r'SOFTWARE\Microsoft\Windows\CurrentVersion\Explorer\Shell Folders'
            downloads_guid = '{374DE290-123F-4565-9164-39C4925E467B}'
            with winreg.OpenKey(winreg.HKEY_CURRENT_USER, sub_key) as key:
                location = winreg.QueryValueEx(key, downloads_guid)[0]
            return location
        else:
            return os.path.join(os.path.expanduser('~'), 'downloads')

    # last step, download
    def download(self):
        if not self.all_set():
            print("\nneed to set url")
            return False
        self.__vids[self.__choice].download(self.__directory)

        # this converts the mp4 video tp mp3 then delete the mp4 if the mp3 mode is on
        if self.__mp3_mode is True:
            downloaded_file_name = self.__vids[self.__choice].default_filename
            new_filename = downloaded_file_name[:-4] + '.mp3'
            subprocess.run(['ffmpeg', '-i',  # or subprocess.run (Python 3.5+)
                            os.path.join(self.__directory, downloaded_file_name),
                            os.path.join(self.__directory, new_filename)
                            ])
            subprocess.run(['rm', os.path.join(self.__directory, downloaded_file_name)])
        return True





if __name__ == '__main__':
 downloader = Downloader()
 downloader.set_url('https://www.youtube.com/watch?v=9tzyJEwO9Os&index=3&list=PLoYCgNOIyGAB_8_iq1cL8MVeun7cB6eNc')
 downloader.mp3_mode_on(False)
 print(downloader.display_download_choices())
 downloader.set_video_choice(0)
 downloader.download()
