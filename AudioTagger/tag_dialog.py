__author__ = 'peter'

import sys

from PySide2 import QtCore, QtGui, QtWidgets

from AudioTagger.manage_related_dialog import ManageRelatedDialog
from AudioTagger.tag_dialog_ui import Ui_TagDialog


class TagListModel(QtGui.QStandardItemModel):

    def __init__(self, parent, tags):
        super().__init__(0, 0, parent)
        print(tags)
        self.tags = tags
        self.create_model()

    def create_model(self):
        print(self.tags.tags)
        for tag in self.tags.tags.values():
            self.add_item(tag)

    def add_item(self, tag):
        item = QtGui.QStandardItem(tag.name)
        item.setData(tag.id)
        self.appendRow(item)
        return item


class TagDialog(QtWidgets.QDialog, Ui_TagDialog):
    settingsSig = QtCore.Signal(list)

    def __init__(self, parent, tag_list):
        super().__init__(parent)
        self.setupUi(self)

        self.tags = tag_list
        self.current_tag = None

        self.init_list()
        self.connectSignals()
        self.tag_list.setCurrentRow(0)

    def init_list(self):
        self.tag_list.addItems(self.tags.get_names())

    def getSettings(self):
        self.show()

    def connectSignals(self):
        self.buttonBox.accepted.connect(self.sendSettings)
        self.btn_add.clicked.connect(self.add_tag)
        applyButton = self.buttonBox.button(
            QtWidgets.QDialogButtonBox.Apply)
        applyButton.clicked.connect(self.sendSettings)
        self.tag_list.selectionModel().selectionChanged.connect(self.update_details)
        self.tag_list.currentRowChanged.connect(self.update_details)

        # Tag form link_signals
        self.input_name.editingFinished.connect(self.new_name)
        self.input_keyseq.editingFinished.connect(self.new_keyseq)
        self.btn_color.clicked.connect(self.color_clicked)
        self.btn_delete.clicked.connect(self.delete_tag)
        self.btn_edit_related.clicked.connect(self.edit_related)

    def add_tag(self, tag=None):
        if not tag:
            # TODO check if exists
            name = "<New Tag>"
            color = QtGui.QColor()
            color.setRgb(255, 0, 127)
            keyseq = ""  # int(QtCore.Qt.Key_0) + self.label_count + 1
            tag = self.tags.add(name, color.rgb(), keyseq)
        self.tag_list.addItem(name)
        self.tag_list.setCurrentRow(self.tag_list.count() - 1)

    def update_details(self, row):
        self.current_tag = self.tags[self.tag_list.currentItem().text()]
        self.show_tag_details()

    def show_tag_details(self):
        tag = self.current_tag
        # Name
        self.input_name.setText(tag.name)

        # Color
        color = QtGui.QColor()
        color = color.fromRgb(int(tag.color))
        pal = self.btn_color.palette()
        pal.setColor(QtGui.QPalette.Button, color)
        self.btn_color.setPalette(pal)

        # Key Sequence
        print(tag.keyseq)
        self.input_keyseq.setKeySequence(tag.keyseq)

        # Related tags
        self.lbl_related_tags.setText(str(tag.get_related()))

    def select_color(self):
        color = QtWidgets.QColorDialog.getColor()
        pal = self.btn_color.palette()
        pal.setColor(QtGui.QPalette.Button, color)
        self.btn_color.setPalette(pal)
        self.current_tag.color = color.rgb()

    def lineEditFinished(self, input_name):
        return getattr(self, "input_" + input_name).text()

    def new_name(self):
        new = self.lineEditFinished("name")
        self.tags.update_name(self.current_tag.name, new)
        self.tag_list.currentItem().setText(self.current_tag.name)

    def color_clicked(self):
        self.select_color()

    def new_keyseq(self):
        new = self.lineEditFinished("keyseq")
        self.current_tag.keyseq = new

    @QtCore.Slot()
    def delete_tag(self):
        print("deleting tag")
        self.tags.delete(self.current_tag.name)
        self.tag_list.takeItem(self.tag_list.currentRow())

    def edit_related(self):
        print("editing related tags")
        dialog = ManageRelatedDialog(self, self.tags, self.current_tag)
        dialog.show()

    def sendSettings(self):
        print("sending settings")
        self.tags.remove_empty()
        self.settingsSig.emit(self.tags)


if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)

    w = TagDialog(None)

    sys.exit(app.exec_())
