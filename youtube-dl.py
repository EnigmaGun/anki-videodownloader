from __future__ import unicode_literals
import youtube_dl
import getopt
import sys
'''
This is basically just a wrapper for youtube-dl as it is quite hard to
use custom packages with Anki.
'''

PATH = "C:/Users/berkal.XATRONIC/AppData\Roaming/Anki2/addons21/anki-videodownloader"


class MyLogger(object):

    def debug(self, message):
        print(message)

    def warning(self, message):
        print(message)

    def error(self, message):
        print(message)


def my_hook(d):
    if d['status'] == 'finished':
        print('Done downloading, now converting ...')


class UrlListReader():

    def read(self, filename):
        urls = []
        file1 = open(filename, 'r')
        Lines = file1.readlines()

        count = 0
        # Strips the newline character
        for line in Lines:
            urls.append(line)
            # print("Line{}: {}".format(count, line.strip()))

        return urls


class VideoDownloader():
    def __init__(self):
        pass

    def start(self, urlfile):

        urls = UrlListReader().read(urlfile)
        print(f'Found {len(urls)} urls')

        ydl_opts = {
            'format': 'bestaudio/best',
            'postprocessors': [{
                'key': 'FFmpegExtractAudio',
                'preferredcodec': 'mp3',
                'preferredquality': '192',
            }],
            'logger': MyLogger(),
            'progress_hooks': [my_hook],
            'ignoreerrors': True,
            'simulate': True,
            'outtmpl': './videos/%(uploader)s/%(title)s-%(upload_date)s-%(id)s.%(ext)s'
        }
        # with youtube_dl.YoutubeDL(ydl_opts) as ydl:
        #    ydl.download(urls)


def main():
    full_cmd_arguments = sys.argv
    args = full_cmd_arguments[1:]

    downloader = VideoDownloader()
    downloader.start(urlfile=args[0])


if __name__ == '__main__':
    main()
