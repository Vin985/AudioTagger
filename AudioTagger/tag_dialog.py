import sys

from PySide2 import QtCore, QtGui, QtWidgets

from AudioTagger.gui.tag_dialog_ui import Ui_TagDialog
from AudioTagger.manage_related_dialog import ManageRelatedDialog


class TagDialog(QtWidgets.QDialog, Ui_TagDialog):
    settingsSig = QtCore.Signal(list)
    update_label_name = QtCore.Signal(str, str)

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
        self.input_keyseq.setKeySequence(tag.keyseq)

        # Related tags
        self.lbl_related_tags.setText(", ".join(tag.get_related()))

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
        old = self.current_tag.name
        if new != self.current_tag.name:
            self.update_label_name.emit(old, new)
            self.tags.update_name(old, new)
            self.tag_list.currentItem().setText(new)

    def color_clicked(self):
        self.select_color()

    def new_keyseq(self):
        new = self.lineEditFinished("keyseq")
        # Same key can be mapped only once
        # TODO: add alert if the sequence is already mapped
        old = self.tags.get_key_sequence(new)
        if old:
            old.keyseq = ""
        self.current_tag.keyseq = new

    @QtCore.Slot()
    def delete_tag(self):
        self.tags.delete(self.current_tag.name)
        self.tag_list.takeItem(self.tag_list.currentRow())

    def edit_related(self):
        dialog = ManageRelatedDialog(self, self.tags, self.current_tag)
        dialog.show()

    def sendSettings(self):
        print("sending settings")
        self.tags.remove_empty()
        self.settingsSig.emit(self.tags)
