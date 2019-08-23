__author__ = 'peter'

import sys
import warnings

from PySide2 import QtCore, QtGui, QtWidgets

from AudioTagger.classDialog2 import Ui_Dialog
from AudioTagger.keysequenceedit import KeySequenceEdit
from AudioTagger.tag_form import TagForm

# from AudioTagger.classdialog_ui import Ui_Dialog


class ClassDialog(QtWidgets.QDialog, Ui_Dialog):
    settingsSig = QtCore.Signal(list)

    def __init__(self, parent, labels):
        super(ClassDialog, self).__init__(parent)
        self.setupUi(self)

        self.connectSignals()

        self.labels = labels
        self.tag_forms = {}
        self.creatingNewLabelSet = False
        self.to_delete = []
        self.to_add = []

        for tag in labels.tags.values():
            self.create_tag(tag)

    def getSettings(self):
        self.show()

    def connectSignals(self):
        self.buttonBox.accepted.connect(self.sendSettings)
        self.buttonBox.rejected.connect(self.remove_pending)
        self.btn_add.clicked.connect(self.create_tag)
        applyButton = self.buttonBox.button(
            QtWidgets.QDialogButtonBox.Apply)
        applyButton.clicked.connect(self.sendSettings)

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

    # def create_label_form(self, label=None):
    #     self.creatingNewLabelSet = True
    #     self.tag_count += 1
    #
    #     color = QtGui.QColor()
    #     if not label:
    #         idx = self.labels.next_id
    #         name = ""
    #         color.setRgb(255, 0, 127)
    #         keyseq = ""  # int(QtCore.Qt.Key_0) + self.label_count + 1
    #         self.labels.add(name, color.rgb(), keyseq)
    #     else:
    #         idx = label.id
    #         name = label.name
    #         color = color.fromRgb(int(label.color))
    #         keyseq = label.keyseq
    #
    #     label_id = str(idx)
    #
    #     # Tag name input
    #     name_input = QtWidgets.QLineEdit(self)
    #     name_input.setObjectName("input_name_" + label_id)
    #     name_input.setText(name)
    #
    #     # Color selection button
    #     color_btn = QtWidgets.QPushButton(self)
    #     pal = color_btn.palette()
    #     pal.setColor(QtGui.QPalette.Button, color)
    #     color_btn.setPalette(pal)
    #     color_btn.setAutoFillBackground(True)
    #     color_btn.setText("")
    #     color_btn.setObjectName("btn_color_" + label_id)
    #
    #     # klabel = QtWidgets.QLabel("Keyboard shortcut: ", self)
    #     # klabel.setObjectName("lbl_keyseq_" + label_id)
    #
    #     # Shortcut input
    #     keySeq = QtGui.QKeySequence(keyseq)
    #     key_input = KeySequenceEdit(keySeq, self)
    #     key_input.setObjectName("input_keyseq_" + label_id)
    #
    #     # Delete button
    #     delete_btn = QtWidgets.QPushButton(self)
    #     sizePolicy = QtWidgets.QSizePolicy(
    #         QtWidgets.QSizePolicy.Maximum, QtWidgets.QSizePolicy.Fixed)
    #     sizePolicy.setHorizontalStretch(0)
    #     sizePolicy.setVerticalStretch(0)
    #     sizePolicy.setHeightForWidth(
    #         delete_btn.sizePolicy().hasHeightForWidth())
    #     delete_btn.setSizePolicy(sizePolicy)
    #     delete_btn.setText("")
    #     icon = QtGui.QIcon()
    #     icon.addPixmap(QtGui.QPixmap(":/icons/delete"),
    #                    QtGui.QIcon.Normal, QtGui.QIcon.Off)
    #     delete_btn.setIcon(icon)
    #     delete_btn.setFlat(True)
    #     delete_btn.setObjectName("delete_btn_" + label_id)
    #
    #     # self.ui.gridLayout.addWidget(label, self.label_count + 1, 0, 1, 1)
    #     self.gridLayout.addWidget(name_input, self.tag_count, 0, 1, 1)
    #     self.gridLayout.addWidget(color_btn, self.tag_count, 1, 1, 1)
    #     # self.ui.gridLayout.addWidget(klabel, self.label_count + 1, 2, 1, 1)
    #     self.gridLayout.addWidget(key_input, self.tag_count, 3, 1, 1)
    #     self.gridLayout.addWidget(delete_btn, self.tag_count, 4, 1, 1)
    #
    #     # Add connections for each specific button
    #
    #     def new_name():
    #         return self.lineEditFinished(idx, "name")
    #     name_input.editingFinished.connect(new_name)
    #
    #     def color_clicked():
    #         return self.select_color(idx)
    #     color_btn.clicked.connect(color_clicked)
    #
    #     def new_keyseq():
    #         return self.lineEditFinished(idx, "keyseq")
    #     key_input.editingFinished.connect(new_keyseq)
    #
    #     def delete_clicked():
    #         return self.delete_tag(idx)
    #     delete_btn.clicked.connect(delete_clicked)
    #
    #     self.creatingNewLabelSet = False
    #
    #     if name:
    #         listItem = QtWidgets.QListWidgetItem()
    #         listItem.setText(name)
    #         self.selection_list.list_src.addItem(listItem)
    #
    #     # self.ui.scrollArea.viewport().updateGeometry()
    #     # self.ui.scrollArea.viewport().update()
    #     # self.ui.scrollArea.updateGeometry()

    def sendSettings(self):
        print("sending settings")
        self.labels.remove_empty()
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

    w = ClassDialog(None)

    sys.exit(app.exec_())
