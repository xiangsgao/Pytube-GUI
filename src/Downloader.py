import threading
import pytube
import os
import math
import enlighten

class Downloader:
    # constructor
    def __init__(self):
        self.__yt = None
        self.__choice = 0
        self.__mp3_mode = False
        self.__directory = self.__get_default_download_path()
        self.__vids = {} # list of videos to download
        self.__thread_pool = []
        self.__parallel_download = False
        self.__manager = enlighten.get_manager()
        self.__ticks = {}

    # add a video to download by its url, returns the name of the video from the given url
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
            return os.path.join(os.path.expanduser('~'), 'Downloads')

    def get_number_of_downloads_in_progress(self):
        return len(self.__thread_pool)


    # displays download choices
    def display_download_choices(self):
        for key, value in self.__vids.items():
            print("\n" + "<------------------------------------------" + key + "------------------------------------------>")
            for i in range(len(value)):
                print(str(i), '. ', value[i])

    # sets the video choices
    def set_video_choice(self, choice):
        self.__choice = choice


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
            self.__ticks[value[self.__choice].title] = self.__manager.counter(total=value[self.__choice].filesize, desc=value[self.__choice].title, unit="ticks", color="red")
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
            self.__ticks[value[self.__choice].title] = self.__manager.counter(total=value[self.__choice].filesize, desc=value[self.__choice].title, unit="ticks", color="red")
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




    # Print iterations progress
    def printProgressBar (self, iteration, total, prefix = '', suffix = '', decimals = 1, length = 100, fill = '█', printEnd = "\r"):

        """
        Call in a loop to create terminal progress bar
        @params:
            iteration   - Required  : current iteration (Int)
            total       - Required  : total iterations (Int)
            prefix      - Optional  : prefix string (Str)
            suffix      - Optional  : suffix string (Str)
            decimals    - Optional  : positive number of decimals in percent complete (Int)
            length      - Optional  : character length of bar (Int)
            fill        - Optional  : bar fill character (Str)
            printEnd    - Optional  : end character (e.g. "\r", "\r\n") (Str)
        """
        percent = ("{0:." + str(decimals) + "f}").format(100 * (iteration / float(total)))
        filledLength = int(length * iteration // total)
        bar = fill * filledLength + '-' * (length - filledLength)
        print(f'\r{prefix} |{bar}| {percent}% {suffix}', end = printEnd)
        # Print New Line on Complete
        if iteration == total:
            print()


    # this function will update the downloading progress
    def progress_function(self, stream, chunk, bytes_remaining):
        tick = self.__ticks[stream.title]
        current_pos = tick.count
        bytes_downloaded = stream.filesize - bytes_remaining
        to_increment = bytes_downloaded - current_pos
        tick.update(to_increment)
        # self.printProgressBar(bytes_downloaded, total_bytes, prefix = 'Progress:', suffix = 'Complete', length = 50)




if __name__ == '__main__':
    # example usage of the downloader class
    downloader = Downloader()
    downloader.add_video('https://www.youtube.com/watch?v=K1QICrgxTjA')
    downloader.add_video('https://www.youtube.com/watch?v=Og847HVwRSI')
    downloader.add_video('https://www.youtube.com/watch?v=STXXtuoohXE')
    downloader.mp3_mode_on(False)
    downloader.set_video_choice(0)
    downloader.use_multithreading(False)
    downloader.download()

    # import time
    # import enlighten

    # manager = enlighten.get_manager()
    # ticks = manager.counter(total=100, desc="Ticks", unit="ticks", color="red")
    # tocks = manager.counter(total=20, desc="Tocks", unit="tocks", color="blue")
    #
    # for num in range(100):
    #     time.sleep(0.1)  # Simulate work
    #     print("The quick brown fox jumps over the lazy dog. {}".format(num))
    #     ticks.update()
    #     if not num % 5:
    #         tocks.update()









