from aqt import mw
# import the "show info" tool from utils.py

import json
import re
import os
import subprocess
from bs4 import BeautifulSoup

from .logger import Logger


class VideoDownloader():

    def __init__(self):
        pass

    def start(self):
        Logger.init()

        working_directory = os.path.dirname(os.path.abspath(__file__))

        if not os.path.exists(f'{working_directory}/data'):
            os.makedirs(f'{working_directory}/data')

        urls_file = 'data/urls.txt'
        urls = self._fetch_urls_from_decks()
        Logger.info(f'Found {len(urls)} urls')
        self._save_urls(
            filename=f'{working_directory}/{urls_file}', urls=urls)
        Logger.info(f'Wrote urls to {working_directory}/{urls_file}')
        # self._download_videos(
        #    working_directory=working_directory, filename=urls_file)

        Logger.close()

        # fetching all urls from the decks
        # write them to the urls list
        # start youtube-dl

        # subprocess.run(
        #    ['c:/windows/system32/Notepad.exe', 'C:/Users/berkal.XATRONIC/AppData\Roaming/Anki2/addons21/my_first_addon/urls.txt'])
        '''
        with open('C:/Users/berkal.XATRONIC/AppData/Roaming/Anki2/addons21/anki-videodownloader/out.txt', 'w+') as fout:
            with open('C:/Users/berkal.XATRONIC/AppData/Roaming/Anki2/addons21/anki-videodownloader/err.txt', 'w+') as ferr:
                out = subprocess.run(['python',
                                      './downloader.py',
                                      'urls3.txt'],
                                     cwd="C:/Users/berkal.XATRONIC/AppData/Roaming/Anki2/addons21/anki-videodownloader/",
                                     stdout=fout, stderr=ferr)
                # reset file to read from it
                fout.seek(0)
                # save output (if any) in variable
                output = fout.read()

                # reset file to read from it
                ferr.seek(0)
                # save errors (if any) in variable
                errors = ferr.read()

        '''

    def _fetch_urls_from_decks(self):
        return UrlFinder().find()

    def _save_urls(self, filename, urls):
        UrlListWriter().write(filename, urls)

    def _download_videos(self, working_directory, filename):
        subprocess.run(['python',
                        './youtube-dl.py',
                        f'{filename}'],
                       cwd=working_directory)


class UrlListWriter():

    def write(self, filename, urls):
        writer = open(
            filename, "w+")

        for url in urls:
            writer.write(f'{url}\n')

        writer.close()

# https: // www.reddit.com/r/Anki/comments/a6u2he/adding_background_image/


class UrlFinder():
    def __init__(self):
        pass

    def find(self):

        all_urls = []

        note_ids = mw.col.findNotes("")

        for (index, note_id) in enumerate(note_ids):
            note = mw.col.getNote(note_id)

            items = note.items()

            for item in items:

                if item[0] == 'YoutubeUrls':
                    urls = self._extract_urls_from_youtubeurls(item[1])
                    if urls:
                        for url in urls:
                            all_urls.append(f'https://youtu.be/{url}')

                else:
                    tag_content = item[1]

                    soup = BeautifulSoup(tag_content, 'html.parser')

                    for link in soup.find_all('a'):
                        all_urls.append(link.get('href'))

        return all_urls

    def _extract_urls_from_youtubeurls(self, content):

        if content:
            urls = []

            entries = content.split('|')

            for entry in entries:
                values = entry.split(';')
                Logger.info(f'Found {values[0]} with description')
                urls.append(values[0])

            return urls

        return None
