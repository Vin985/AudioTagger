from PySide2 import QtWidgets

from AudioTagger.selectionListWidget import SelectionListWidget


class TagsSelectionList(SelectionListWidget):

    def __init__(self, parent=None, src=None, dest=None):
        super().__init__(parent, src, dest)
        self.link_signals()

    def link_signals(self):
        self.list_src.itemClicked.connect(self.check_related)

    def check_related(self):
        pass
