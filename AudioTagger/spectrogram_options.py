
from PySide2 import QtCore, QtGui, QtWidgets

from AudioTagger.gui.spectrogram_options_ui import Ui_SpectrogramOptions


class SpectrogramOptions(QtWidgets.QWidget, Ui_SpectrogramOptions):

    def __init__(self, parent):
        super().__init__(parent)
        self.setupUi(self)

    def follow(self):
        return self.cb_followSound.isChecked()

    def contrast(self):
        return self.slider_contrast.value()
