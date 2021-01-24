from aqt import mw
# import the "show info" tool from utils.py

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

        decks = ['Magie', 'Tricksqueue', 'Import']

        for deck_name in decks:
            deck_id = deck_name.lower()

            urls_file = f'data/urls_{deck_id}.txt'

            # read archive
            urls_in_archive = ArchiveReader().read(
                working_directory=working_directory, 
                deck_name=deck_name)
            
            archived_urls = set()
            for url in urls_in_archive:
                cleaned = url.replace("\n", "")
                Logger.info(f'-->archive -->{cleaned}<--')
                archived_urls.add(cleaned)

            urls = self._fetch_urls_from_deck(deck_name, archived_urls)
            Logger.info(f'Found {len(urls)} urls in deck {deck_name}')
            self._save_urls(
                filename=f'{working_directory}/{urls_file}', urls=urls)
            Logger.info(f'Wrote urls to {working_directory}/{urls_file}')

            self._download_videos(
                working_directory=working_directory, filename=urls_file, deck_id=deck_id)

        Logger.close()

    def _fetch_urls_from_deck(self, deck_name, archived_urls):
        return UrlFinder().find(deck_name,archived_urls)

    def _save_urls(self, filename, urls):
        UrlListWriter().write(filename, urls)

    def _download_videos(self, working_directory, filename, deck_id):

        Logger.info(f'filename {filename} deck_id {deck_id}')

        subprocess.run(['python',
                        './youtube-dl.py',
                        filename, deck_id],
                       cwd=working_directory)


class UrlListWriter():

    def write(self, filename, urls):
        writer = open(
            filename, "w+")

        for url in urls:
            writer.write(f'{url}\n')

        writer.close()

# https: // www.reddit.com/r/Anki/comments/a6u2he/adding_background_image/


class ArchiveReader():

    def read(self, working_directory, deck_name):
        urls = []
        deck_id = deck_name.lower()
        filename = f'{working_directory}/data/archive_{deck_id}.txt'
        
        file = open(filename, 'r')
        lines = file.readlines()

        # Strips the newline character
        for line in lines:
            youtube_id = line.split(' ')[1]
            print(youtube_id)
            urls.append(youtube_id)
            # print("Line{}: {}".format(count, line.strip()))

        return urls

class UrlFinder():
    def __init__(self):
        pass

    def find(self, deck_name, archived_urls):

        all_urls = set()  # []

        deckfilter = ""
        deckfilter = f"deck:{deck_name}"
        note_ids = mw.col.findNotes(deckfilter)
        
        for (index, note_id) in enumerate(note_ids):
            note = mw.col.getNote(note_id)

            items = note.items()

            for item in items:

                if item[0] == 'YoutubeUrls':
                    urls = self._extract_urls_from_youtubeurls(item[1])
                    if urls:
                        for url in urls:
                            url = url.split('?')[0] # strip url parameters
                            youtube_url = f'https://youtu.be/{url}'
                            
                            if url in archived_urls:
                                Logger.info(f'Skipping {youtube_url}, already downloaded')
                            elif youtube_url in all_urls:
                                Logger.info(f'Skipping {youtube_url}, duplicate entry')  
                            else:
                                all_urls.add(youtube_url)
                                Logger.info(f'Added {youtube_url}')
                                

                            # all_urls.append()

                else:
                    tag_content = item[1]

                    soup = BeautifulSoup(tag_content, 'html.parser')

                    for link in soup.find_all('a'):
                        url = link.get('href')

                        if url not in all_urls:
                            all_urls.add(url)
                        # all_urls.append(link.get('href'))

        return all_urls

    def _extract_urls_from_youtubeurls(self, content):

        if content:
            urls = []
            cleaned = content.replace("\n", " ")
            entries = cleaned.split('|')

            for entry in entries:
                values = entry.split(';')
                urls.append(values[0])

            return urls

        return None
'''
class UrlListChecker():

    def check(deck_id):
        # read archive file

        # read url list
        urls_file = f'data/urls_{deck_id}.txt'
        urls = UrlListReader().read(urls_file)
        urls_set = set
        # put all youtube ids in a set
'''
        

