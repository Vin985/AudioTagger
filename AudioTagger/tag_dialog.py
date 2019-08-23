__author__ = 'peter'

import sys
import warnings

from PySide2 import QtCore, QtGui, QtWidgets
from PySide2.QtCore import Qt

from AudioTagger.keysequenceedit import KeySequenceEdit
from AudioTagger.tag_dialog_ui import Ui_TagDialog
from AudioTagger.tag_form import TagForm


class TagListModel(QtGui.QStandardItemModel):

    def __init__(self, parent, tags):
        super().__init__(0, 0, parent)
        print(tags)
        self.tags = tags
        self.create_model()

    def create_model(self):
        print(self.tags.tags)
        for tag in self.tags.tags.values():
            item = QtGui.QStandardItem(tag.name)
            item.setData(tag.id)
            self.appendRow(item)


class TagDialog(QtWidgets.QDialog, Ui_TagDialog):
    settingsSig = QtCore.Signal(list)

    def __init__(self, parent, tag_list):
        super().__init__(parent)
        self.setupUi(self)

        self.tags = tag_list

        self.init_list()
        self.connectSignals()
        self.tag_list.setCurrentIndex(self.tag_list.model().index(0, 0))

    def init_list(self):
        model = TagListModel(self, self.tags)
        self.tag_list.setModel(model)
        # self.tag_list.addItems(labels.get_names())

    def getSettings(self):
        self.show()

    def connectSignals(self):
        self.buttonBox.accepted.connect(self.sendSettings)
        # self.buttonBox.rejected.connect(self.remove_pending)
        self.btn_add.clicked.connect(self.create_tag)
        applyButton = self.buttonBox.button(
            QtWidgets.QDialogButtonBox.Apply)
        applyButton.clicked.connect(self.sendSettings)
        self.tag_list.selectionModel().selectionChanged.connect(self.update_details)

        # Tag form link_signals
        self.input_name.editingFinished.connect(self.new_name)
        self.input_keyseq.editingFinished.connect(self.new_keyseq)
        self.btn_color.clicked.connect(self.color_clicked)
        self.btn_delete.clicked.connect(self.delete_clicked)
        self.btn_edit_related.clicked.connect(self.edit_related)

    def update_details(self, new, old):
        index = new.indexes()[0]
        item = index.model().itemFromIndex(index)
        self.show_tag_details(self.tags[item.data()])

    def show_tag_details(self, tag):
        # Name
        self.input_name.setText(tag.name)

        # Color
        color = QtGui.QColor()
        color = color.fromRgb(int(tag.color))
        pal = self.btn_color.palette()
        pal.setColor(QtGui.QPalette.Button, color)
        self.btn_color.setPalette(pal)

        # Key Sequence
        self.input_keyseq.setKeySequence(tag.keyseq)

    def create_tag(self, tag=None):
        color = QtGui.QColor()
        if not tag:
            name = ""
            color.setRgb(255, 0, 127)
            keyseq = ""  # int(QtCore.Qt.Key_0) + self.label_count + 1
            tag = self.labels.add(name, color.rgb(), keyseq)
            #tag = self.to_add[tag.id]

        tag_form = TagForm(tag=tag, parent=self)
        self.tag_forms[tag.id] = tag_form
        tag_form.delete_tag.connect(self.delete_tag)
        self.tag_layout.addWidget(tag_form)

    def sendSettings(self):
        print("sending settings")
        self.tags.remove_empty()
        self.settingsSig.emit(self.labels)

    def remove_pending(self):
        pass

    @QtCore.Slot()
    def delete_tag(self, tag_id):
        print("deleting tag:" + str(tag_id))
        del self.tag_forms[tag_id]
        # self.to_delete.add[tag_id]
        self.labels.delete(tag_id)


if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)

    w = TagDialog(None)

    sys.exit(app.exec_())
