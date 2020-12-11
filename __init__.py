from aqt import mw

# import all of the Qt GUI library
from aqt.qt import *
from .downloader import VideoDownloader


class SettingsDialog(QDialog):

    def __init__(self, *args, **kwargs):
        super(SettingsDialog, self).__init__(*args, **kwargs)

        self.setWindowTitle("Video Downloader")

        buttons = QDialogButtonBox.Ok | QDialogButtonBox.Cancel

        self.button_box = QDialogButtonBox(buttons)
        self.button_box.accepted.connect(self._start)
        self.button_box.rejected.connect(self.reject)

        self.layout = QVBoxLayout()

        description = QLabel('Video Downloader:')
        self.layout.addWidget(description)
        self.layout.addWidget(QLabel('All urls are gathered and downloaded'))

        output_path_label = QLabel('Output path')
        self.layout.addWidget(output_path_label)

        self._output_path = QLineEdit(self)
        self._output_path.setText("c:/temp/")
        self.layout.addWidget(self._output_path)

        self.layout.addWidget(self.button_box)
        self.setLayout(self.layout)

    def _start(self):

        downloader = VideoDownloader()
        downloader.start()

        #downloader = VideoDownloader()
        # downloader.start()

        self.accept()


class AddOnActivator():

    def __init__(self):
        action = QAction(mw)
        action.setText("Video Downloader")
        mw.form.menuTools.addAction(action)

        def start_addon():
            dlg = SettingsDialog()
            if dlg.exec_():
                print("Success!")
            else:
                print("Cancel!")

        action.triggered.connect(start_addon)


AddOnActivator()
