import pytube
import os

class Downloader:

    # constructor
    def __init__(self):
        self.__yt = None
        self.__choice = 0
        self.__mp3_mode = False
        self.__directory = self.__get_default_download_path()
        self.__vids = None

    # sets the video to download by its url
    def set_url(self, url):
        self.__yt = pytube.YouTube(url)

    # sets a custom download directory
    def set_download_directory(self, directory):
        self.__directory = directory

    # sets if the just download mp3
    def mp3_mode_on(self, value):
        self.__mp3_mode = value

    # displays download choices
    def display_download_choices(self):
        if not self.yt_set():
            print('need to set url first\n')
            return

        self.__vids = self.__yt.streams.all()
        choice_list = [None] * len(self.__vids)
        for i in range(len(self.__vids)):
            choice_list[i] = str(print(i, '. ', self.__vids[i]))
        return list

    # sets the video choices
    def set_video_choice(self, choice):
        self.__choice = choice

    def get_download_directory(self):
        return self.__directory

    # checks if the url is set
    def yt_set(self):
        return self.__yt is not None

    # Returns the default downloads path for linux or windows
    def __get_default_download_path(self):
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
        if not self.yt_set():
            print("\nneed to set url")
            return False

        self.__vids[self.__choice].download(self.__directory)
        self.__vids = self.__yt.streams.all()
        # this converts the mp4 video tp mp3 then delete the mp4 if the mp3 mode is on
        if self.__mp3_mode is True:
            downloaded_file = os.path.join(self.__directory, self.__vids[self.__choice].default_filename)
            mp3_file = downloaded_file[:-4] + '.mp3'
            print(downloaded_file)
            print(mp3_file)
            os.rename(downloaded_file, mp3_file)
            # below is for removing the original mp4, doesn't need becuase we are just gonna rename the file to mp3 instead of actually converting
            # subprocess.run(['rm', os.path.join(self.__directory, downloaded_file)])
        return True





if __name__ == '__main__':
    downloader = Downloader()
    downloader.set_url('https://www.youtube.com/watch?v=gqJG2QFbgfg')
    downloader.mp3_mode_on(True)
    print(downloader.display_download_choices())
    downloader.set_video_choice(0)
    downloader.download()
