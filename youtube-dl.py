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


def my_hook(data):
    if data['status'] == 'finished':
        print('Done downloading, now converting ...')
		
	#print(f'filename: {data['filename']})


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

"""
--format (bestvideo[ext=mp4][height<=720][fps<30]/bestvideo[ext=mp4][height<=720]/bestvideo[ext=mp4][height>=1080]/bestvideo)+(bestaudio[ext=m4a]/bestaudio)/best
--download-archive archive.txt
--output %(playlist_uploader)s-%(playlist_title)s/%(autonumber)s.%(title)s.%(id)s.%(ext)s
--merge-output-format mp4
--restrict-filenames
--ignore-errors
--write-description
https://github.com/ytdl-org/youtube-dl/blob/master/youtube_dl/YoutubeDL.py#L128-L278
"""
class VideoDownloader():
    def __init__(self):
        pass

    def start(self, urlfile):

        urls = UrlListReader().read(urlfile)
        print(f'Found {len(urls)} urls')

        ydl_opts = {
            'format': '(bestvideo[ext=mp4][height<=720][fps<30]/bestvideo[ext=mp4][height<=720]/bestvideo[ext=mp4][height>=1080]/bestvideo)+(bestaudio[ext=m4a]/bestaudio)/best',
            'merge_output_format':'mp4',
			'download_archive': './data/archive.txt',
            'logger': MyLogger(),
            'progress_hooks': [my_hook],
            'ignoreerrors': True,
            #'simulate': True,
            'outtmpl': './videos/%(uploader)s-%(title)s-%(upload_date)s-%(id)s.%(ext)s',
			'writedescription': True,
			'restrictfilenames': True,
			'quiet': True
        }
        with youtube_dl.YoutubeDL(ydl_opts) as ydl:
            ydl.download(urls)


def main():
    full_cmd_arguments = sys.argv
    args = full_cmd_arguments[1:]

    downloader = VideoDownloader()
    downloader.start(urlfile=args[0])


if __name__ == '__main__':
    main()
