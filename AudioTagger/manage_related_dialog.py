
from PySide2 import QtCore, QtWidgets

from AudioTagger.manage_related_dialog_ui import Ui_ManageRelatedDialog


class ManageRelatedDialog(QtWidgets.QDialog, Ui_ManageRelatedDialog):
    update_related = QtCore.Signal(list)

    def __init__(self, parent, all_tags, current):
        super().__init__(parent)
        self.setupUi(self)

        self.tags = all_tags
        self.current = current

        # Get only first level relatives
        self.related = current.get_related(max_level=1)

        # Get list of all tags as source
        src = self.tags.get_names()
        # Remove current tag from list
        src.remove(current.name)

        # Fill selection lists
        self.selection_widget.init_lists(src, self.related)

        # Disable all related tags
        all_related = current.get_related(min_level=1)
        self.selection_widget.disable_items(
            self.selection_widget.list_src, all_related)

        self.connectSignals()

    def connectSignals(self):
        self.buttonBox.accepted.connect(self.send_tags)
        self.selection_widget.items_added.connect(self.add_related)
        self.selection_widget.items_removed.connect(self.remove_related)

    def send_tags(self):
        selected = self.selection_widget.get_dest_text()
        print(selected)
        self.update_related.emit(selected)

    def add_related(self, added):
        for tag in added:
            to_add = self.tags[tag]
            self.current.add_related(to_add)
            related = to_add.get_related()
            if related:
                print(related)
                existing = self.selection_widget.get_dest_text()
                print(existing)
            print(tag)

    def remove_related(self, removed):
        print(removed)
