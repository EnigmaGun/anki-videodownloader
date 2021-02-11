from aqt import mw
# import the "show info" tool from utils.py

import os
import re
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
        #decks = ['Magie']
        #decks = ['Import']

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

class UrlsList():

    def __init__(self, archived_urls):
        self._all_urls = set()  # []
        self._archived_urls = archived_urls

    def add_youtube_id(self,  id, items):
        youtube_url = f'https://youtu.be/{id}'
                            
        if url in self._archived_urls:
            Logger.info(f'Skipping {youtube_url}, already downloaded')
        elif youtube_url in self._all_urls:
            Logger.info(f'Skipping {youtube_url}, duplicate entry')  
        else:
            self._all_urls.add(youtube_url)
            Logger.info(f'Added {youtube_url} NoteId {items[0][1]}')
    
    def get_urls(self):
        return self._all_urls

class UrlFinder():
    def __init__(self):
        pass

    def find(self, deck_name, archived_urls):

        new_video_urls = set()  # []

        #all_urls_list = UrlsList(archived_urls)

        deckfilter = ""
        deckfilter = f"deck:{deck_name}"
        note_ids = mw.col.findNotes(deckfilter)

        def should_download(video_id):
            if video_id in archived_urls:
                Logger.info(f'Skipping {video_id}, already downloaded')
                return False
            elif video_id in new_video_urls:
                Logger.info(f'Skipping {video_id}, duplicate entry')  
                return False
        
            return True

        
        for (index, note_id) in enumerate(note_ids):
            note = mw.col.getNote(note_id)
            
            items = note.items()

            for item in items:

                if item[0] == 'YoutubeUrls':
                    urls = self._extract_urls_from_youtubeurls(item[1])
                    if urls:
                        for url in urls:
                            video_id = url.split('?')[0] # strip url parameters
                            #all_urls_list.add_youtube_id(id, items)
                            
                            if should_download(video_id):
                                youtube_url = f'https://youtu.be/{video_id}'    
                                new_video_urls.add(youtube_url)
                                Logger.info(f'Added {youtube_url} NoteId {items[0][1]}')
                            '''
                            youtube_url = f'https://youtu.be/{video_id}'
                            
                            if video_id in archived_urls:
                                Logger.info(f'Skipping {youtube_url}, already downloaded')
                            elif youtube_url in all_urls:
                                Logger.info(f'Skipping {youtube_url}, duplicate entry')  
                            else:
                                all_urls.add(youtube_url)
                                Logger.info(f'Added {youtube_url} NoteId {items[0][1]}')
                                
                            '''
                            # all_urls.append()
                            

                else:
                    tag_content = item[1]
                    youtube_ids = self._get_youtube_ids_from_string(tag_content)

                    for video_id in youtube_ids:
                        #all_urls_list.add_youtube_id(id, items)
                        
                        youtube_url = f'https://youtu.be/{video_id}'
                            
                        if video_id in archived_urls:
                            Logger.info(f'Skipping {youtube_url}, already downloaded')
                        elif youtube_url in new_video_urls:
                            Logger.info(f'Skipping {youtube_url}, duplicate entry')  
                        else:
                            new_video_urls.add(youtube_url)
                            Logger.info(f'Added {youtube_url} NoteId {items[0][1]}')
                        
                    
                    '''
                    soup = BeautifulSoup(tag_content, 'html.parser')

                    for link in soup.find_all('a'):
                        url = link.get('href')

                        if url not in all_urls:
                            all_urls.add(url)
                        # all_urls.append(link.get('href'))
                    '''

        return new_video_urls #all_urls_list.get_urls() # 

    def _extract_urls_from_youtubeurls(self, content):

        if content:
            urls = []

            cleanr = re.compile('<.*?>')
            cleaned = re.sub(cleanr, '', content)
            cleaned = cleaned.replace("\n", "")
            entries = cleaned.split('|')

            for entry in entries:
                values = entry.split(';')
                urls.append(values[0])

            return urls

        return None
    
    def _get_youtube_ids_from_string(self, string):
        
        urls = self._get_urls_from_string(string)
        
        youtube_ids = []
        
        for url in urls:
            if url.startswith('https://youtu.be/'):
                youtube_ids.append(url.replace('https://youtu.be/','')) 

        return youtube_ids

    def _get_urls_from_string(self, string): 
        # findall() has been used  
        # with valid conditions for urls in string 
        regex = r"(?i)\b((?:https?://|www\d{0,3}[.]|[a-z0-9.\-]+[.][a-z]{2,4}/)(?:[^\s()<>]+|\(([^\s()<>]+|(\([^\s()<>]+\)))*\))+(?:\(([^\s()<>]+|(\([^\s()<>]+\)))*\)|[^\s`!()\[\]{};:'\".,<>?«»“”‘’]))"
        urls = re.findall(regex,string)       
        
        return [x[0] for x in urls] 

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
        

