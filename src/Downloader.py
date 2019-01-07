import threading

import pytube
import os
import math
class Downloader:


    # constructor
    def __init__(self):
        self.__yt = None
        self.__choice = 0
        self.__mp3_mode = False
        self.__directory = self.__get_default_download_path()
        self.__vids = {}
        self.__thread_pool = []
        self.__parallel_download = False

    # sets the video to download by its url
    def add_video(self, url):
        # pass in the call back function so it updates
        self.__yt = pytube.YouTube(url, on_progress_callback=self.progress_function)
        video = self.__yt.streams.all()
        key = video[self.__choice].default_filename
        if key in self.__vids.keys():
            raise Exception("Already contains the video")
            return
        self.__vids[key] = video
        return key

    def use_multithreading(self, value):
        self.__parallel_download = value

    def remove_video(self, video):
        self.__vids.pop(video, None)

    # sets a custom download directory
    def set_download_directory(self, directory):
        self.__directory = directory

    # sets if the just download mp3
    def mp3_mode_on(self, value):
        self.__mp3_mode = value

    # displays download choices
    def display_download_choices(self):
        for key, value in self.__vids.items():
            print("\n" + "<------------------------------------------" + key + "------------------------------------------>")
            for i in range(len(value)):
                print(str(i), '. ', value[i])

    # sets the video choices
    def set_video_choice(self, choice):
        self.__choice = choice

    def get_download_directory(self):
        return self.__directory

    # checks if the url is set
    def videos_empty(self):
        return not any(self.__vids)

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


    # a facade function to narrow the downloading interfaces
    def download(self):
        if self.__parallel_download == True:
            self.__download_in_parallel()
        else:
            self.__download_in_serial()


    # last step, download serially, one at a time which is slow but little room for bugs
    def __download_in_serial(self):
        if self.videos_empty():
            print("\nneed to add url")
            raise Exception("No videos in the list")

        # update number of downloads, since it is serial, it will just add a place holder for thread pool
        self.__thread_pool.append('place holder')
        for key, value in self.__vids.items():
            downloaded_file = os.path.join(self.__directory, value[self.__choice].default_filename)
            mp3_file = downloaded_file[:-4] + '.mp3'
            print('Downloading ' + downloaded_file + '....')
            value[self.__choice].download(self.__directory)
            # this converts the mp4 video tp mp3 then delete the mp4 if the mp3 mode is on
            if self.__mp3_mode is True:
                print('\nconverting ' + downloaded_file + ' to mp3....')
                if os.path.exists(mp3_file):
                    os.remove(mp3_file)
                os.rename(downloaded_file, mp3_file)
                # below is for removing the original mp4, doesn't need becuase we are just gonna rename the file to mp3 instead of actually converting
                # subprocess.run(['rm', os.path.join(self.__directory, downloaded_file)])
            print('Finished downloading ' + key)
        # update he number of downloads still in progress
        self.__thread_pool.pop()

    # last step, downloading using threads, faster but error and bug prone.
    def __download_in_parallel(self):
        if self.videos_empty():
            print("\nneed to add url")
            raise Exception("No videos in the list")
        for key, value in self.__vids.items():
            thread = threading.Thread(target=self.__parallel_download_thread_function, name='Parallel download thread', args=(key, value))
            # this keeps rack how much threads are currently downloading
            self.__thread_pool.append(thread)
            thread.start()


    def __parallel_download_thread_function(self, file_name, video):
        downloaded_file = os.path.join(self.__directory, video[self.__choice].default_filename)
        mp3_file = downloaded_file[:-4] + '.mp3'
        print('Downloading ' + downloaded_file + '....')
        video[self.__choice].download(self.__directory)
        # this converts the mp4 video tp mp3 then delete the mp4 if the mp3 mode is on
        if self.__mp3_mode is True:
            print('\nconverting ' + downloaded_file + ' to mp3....')
            if os.path.exists(mp3_file):
                os.remove(mp3_file)
            os.rename(downloaded_file, mp3_file)
            # below is for removing the original mp4, doesn't need becuase we are just gonna rename the file to mp3 instead of actually converting
            # subprocess.run(['rm', os.path.join(self.__directory, downloaded_file)])
        print('Finished downloading ' + file_name)
        # this updates the number of downloads still in progress
        self.__thread_pool.pop()

    def get_number_of_downloads_in_progress(self):
        return len(self.__thread_pool)




    # this function will update the downloading progress
    def progress_function(self,stream, chunk,file_handle, bytes_remaining):
        bytes_downloaded = file_handle.tell()
        total_bytes = bytes_remaining + bytes_downloaded
        percent_downloaded = math.floor((bytes_downloaded / total_bytes) * 100)
        print(stream.default_filename + ": " + str(percent_downloaded) + '%')




if __name__ == '__main__':
    # example usage of the downloader class
    downloader = Downloader()
    downloader.add_video('https://www.youtube.com/watch?v=T47VZVwYxKg')
    downloader.mp3_mode_on(True)
    downloader.display_download_choices()
    downloader.set_video_choice(0)
    downloader.use_multithreading(False)
    downloader.download()
