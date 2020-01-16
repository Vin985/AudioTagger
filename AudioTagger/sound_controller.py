
from PySide2 import QtCore, QtGui, QtWidgets

from AudioTagger.gui.sound_controller_ui import Ui_SoundController


class SoundController(QtWidgets.QWidget, Ui_SoundController):

    def __init__(self, parent):
        super().__init__(parent)
        self.setupUi(self)

    def follow(self):
        return self.cb_followSound.isChecked()

    def contrast(self):
        return self.slider_contrast.value()

    def init_playback_speeds(self, speeds, current):
        self.cb_playbackSpeed.clear()
        self.cb_playbackSpeed.insertItems(
            0, [str(x) for x in speeds])
        self.cb_playbackSpeed.setCurrentIndex(speeds.index(current))

    def update_play_tooltip(self, text):
        self.pb_play.setToolTip(text)
