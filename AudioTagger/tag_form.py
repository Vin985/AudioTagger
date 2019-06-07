from PySide2 import QtCore, QtGui, QtWidgets

from AudioTagger.tag_form_ui import Ui_TagForm


class TagForm(QtWidgets.QWidget, Ui_TagForm):

    def __init__(self, parent=None):
        super().__init__(parent)
        self.setupUi(self)
