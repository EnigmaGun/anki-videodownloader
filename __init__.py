from aqt import mw
# import the "show info" tool from utils.py

# import all of the Qt GUI library
from aqt.qt import *
import json
import re
from bs4 import BeautifulSoup
import subprocess


class Logger():

    @staticmethod
    def init():

        LOG_PATH = "C:/Users/berkal.XATRONIC/AppData\Roaming/Anki2/addons21/anki-videodownloader"
        FILE_NAME = 'log.txt'

        Logger.logger = open(f"{LOG_PATH}/{FILE_NAME}", "w+")

    @staticmethod
    def info(message):
        Logger.logger.write(f'[INFO] {message}\n')

    @staticmethod
    def warn(message):
        Logger.logger.write(f'[WARN] {message}\n')

    @staticmethod
    def error(message):
        Logger.logger.write(f'[ERROR] {message}\n')

    @staticmethod
    def close():
        Logger.logger.close()


class VideoDownloader():

    def __init__(self):
        pass

    def start(self):

        # subprocess.run(
        #    ['c:/windows/system32/Notepad.exe', 'C:/Users/berkal.XATRONIC/AppData\Roaming/Anki2/addons21/my_first_addon/urls.txt'])

        with open('C:/Users/berkal.XATRONIC/AppData/Roaming/Anki2/addons21/anki-videodownloader/out.txt', 'w+') as fout:
            with open('C:/Users/berkal.XATRONIC/AppData/Roaming/Anki2/addons21/anki-videodownloader/err.txt', 'w+') as ferr:
                out = subprocess.Popen(['python',
                                        './downloader.py'],
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


class UrlListWriter():

    def write(self, filename, urls):

        FILE_NAME = filename

        writer = open(
            f"C:/Users/berkal.XATRONIC/AppData\Roaming/Anki2/addons21/anki-videodownloader/{FILE_NAME}", "w+")

        for url in urls:
            writer.write(f'{url}\n')

        writer.close()


class UrlFinder():
    def __init__(self):
        pass

    def find(self):
        Logger.init()
        Logger.info('Started')

        all_urls = []

        note_ids = mw.col.findNotes("is:review")

        for note_id in note_ids:
            note = mw.col.getNote(note_id)
            note_items = dict(note.items())

            tag_content = note_items['Lernhilfe']

            soup = BeautifulSoup(tag_content, 'html.parser')

            for link in soup.find_all('a'):
                all_urls.append(link.get('href'))

        Logger.close()

        return all_urls

    def remove_tags(self, text):
        TAG_RE = re.compile(r'<[^>]+>')
        return TAG_RE.sub('', text)


class SettingsDialog(QDialog):

    def __init__(self, *args, **kwargs):
        super(SettingsDialog, self).__init__(*args, **kwargs)

        self.setWindowTitle("Video Downloader")

        buttons = QDialogButtonBox.Ok | QDialogButtonBox.Cancel

        self.button_box = QDialogButtonBox(buttons)
        self.button_box.accepted.connect(self._start)
        self.button_box.rejected.connect(self.reject)

        self.layout = QVBoxLayout()

        output_path_label = QLabel('Output path')
        self.layout.addWidget(output_path_label)

        self._output_path = QLineEdit(self)
        self._output_path.setText("c:/temp/")
        self.layout.addWidget(self._output_path)

        self.layout.addWidget(self.button_box)
        self.setLayout(self.layout)

    def _start(self):
        urls = UrlFinder().find()
        UrlListWriter().write('urls3.txt', urls)

        downloader = VideoDownloader()
        downloader.start()

        self.accept()


class AddOnActivator():

    def __init__(self):
        action = QAction(mw)
        action.setText("Video Downloader")
        mw.form.menuTools.addAction(action)

        def start_Addon():
            dlg = SettingsDialog()
            if dlg.exec_():
                print("Success!")
            else:
                print("Cancel!")

        action.triggered.connect(start_Addon)

    def show(self):
        pass


AddOnActivator()
