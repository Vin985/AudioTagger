
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
        self.disable_related(self.current, min_level=1)

        self.connectSignals()

    def disable_related(self, tag, min_level=0):
        related = tag.get_related(min_level=min_level)
        self.selection_widget.disable_items(
            self.selection_widget.list_src, related)

    def enable_related(self, tag):
        # Get all related tag from removed tag
        related = tag.get_related()
        # Get all related tags for current tag
        all_related = self.current.get_related()
        # Do not enable tags that are related to other tags
        to_enable = list(set(related) - set(all_related))
        self.selection_widget.enable_items(
            self.selection_widget.list_src, to_enable)

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
            self.disable_related(to_add)

    def remove_related(self, removed):
        for tag in removed:
            to_remove = self.tags[tag]
            self.current.remove_related(to_remove)
            self.enable_related(to_remove)
            if tag in self.current.get_related():
                self.selection_widget.disable_items(
                    self.selection_widget.list_src, [tag])
