from PySide2 import QtWidgets

from AudioTagger.selection_list_ui import Ui_SelectionList


class SelectionListWidget(QtWidgets.QWidget, Ui_SelectionList):

    def __init__(self, parent=None, src=None, dest=None):
        super().__init__(parent)
        self.setupUi(self)
        self.link_signals()

    def link_signals(self):
        self.btn_add.clicked.connect(self.add)
        self.btn_remove.clicked.connect(self.remove)

    def add(self):
        self.moveItems(self.list_src, self.list_dest)

    def remove(self):
        self.moveItems(self.list_dest, self.list_src)

    def moveItems(self, src, dest):
        for item in src.selectedItems():
            row = src.row(item)
            src.takeItem(row)
            dest.addItem(item)
