__author__ = 'peter'

import copy
import sys
import warnings
from collections import OrderedDict

from PySide2 import QtCore, QtGui, QtWidgets

from AudioTagger.classDialog2 import Ui_Dialog

# from AudioTagger.classdialog_ui import Ui_Dialog


class ClassDialog(QtWidgets.QDialog, Ui_Dialog):
    settingsSig = QtCore.Signal(list)

    def __init__(self, parent, labels):
        super(ClassDialog, self).__init__(parent)
        self.setupUi(self)

        self.connectSignals()

        self.tag_count = 0
        self.labels = labels
        self.creatingNewLabelSet = False

        for tag in labels.tags.values():
            self.create_label_form(tag)
        # self.create_label_form()

    def getSettings(self):
        self.show()

    def connectSignals(self):
        self.buttonBox.accepted.connect(self.sendSettings)
        self.btn_add.clicked.connect(self.create_label_form)
        applyButton = self.buttonBox.button(
            QtWidgets.QDialogButtonBox.Apply)
        applyButton.clicked.connect(self.sendSettings)

    def setLabelColor(self, label, color):
        colourStyle = "background-color: {0}".format(color.name())
        label.setStyleSheet(colourStyle)

    def create_label_form(self, label=None):
        self.creatingNewLabelSet = True
        self.tag_count += 1

        color = QtGui.QColor()
        if not label:
            idx = self.labels.next_id
            name = ""
            color.setRgb(255, 0, 127)
            keyseq = ""  # int(QtCore.Qt.Key_0) + self.label_count + 1
            self.labels.add(name, color.rgb(), keyseq)
        else:
            idx = label.id
            name = label.name
            color = color.fromRgb(int(label.color))
            keyseq = label.keyseq

        label_id = str(idx)

        # Tag name input
        name_input = QtWidgets.QLineEdit(self)
        name_input.setObjectName("input_name_" + label_id)
        name_input.setText(name)

        # Color selection button
        color_btn = QtWidgets.QPushButton(self)
        pal = color_btn.palette()
        pal.setColor(QtGui.QPalette.Button, color)
        color_btn.setPalette(pal)
        color_btn.setAutoFillBackground(True)
        color_btn.setText("")
        color_btn.setObjectName("btn_color_" + label_id)

        # klabel = QtWidgets.QLabel("Keyboard shortcut: ", self)
        # klabel.setObjectName("lbl_keyseq_" + label_id)

        # Shortcut input
        keySeq = QtGui.QKeySequence(keyseq)
        key_input = KeySequenceEdit(keySeq, self)
        key_input.setObjectName("input_keyseq_" + label_id)

        # Delete button
        delete_btn = QtWidgets.QPushButton(self)
        sizePolicy = QtWidgets.QSizePolicy(
            QtWidgets.QSizePolicy.Maximum, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(
            delete_btn.sizePolicy().hasHeightForWidth())
        delete_btn.setSizePolicy(sizePolicy)
        delete_btn.setText("")
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap(":/icons/delete"),
                       QtGui.QIcon.Normal, QtGui.QIcon.Off)
        delete_btn.setIcon(icon)
        delete_btn.setFlat(True)
        delete_btn.setObjectName("delete_btn_" + label_id)

        # self.ui.gridLayout.addWidget(label, self.label_count + 1, 0, 1, 1)
        self.gridLayout.addWidget(name_input, self.tag_count, 0, 1, 1)
        self.gridLayout.addWidget(color_btn, self.tag_count, 1, 1, 1)
        # self.ui.gridLayout.addWidget(klabel, self.label_count + 1, 2, 1, 1)
        self.gridLayout.addWidget(key_input, self.tag_count, 3, 1, 1)
        self.gridLayout.addWidget(delete_btn, self.tag_count, 4, 1, 1)

        # Add connections for each specific button

        def new_name():
            return self.lineEditFinished(idx, "name")
        name_input.editingFinished.connect(new_name)

        def color_clicked():
            return self.select_color(idx)
        color_btn.clicked.connect(color_clicked)

        def new_keyseq():
            return self.lineEditFinished(idx, "keyseq")
        key_input.editingFinished.connect(new_keyseq)

        def delete_clicked():
            return self.delete_tag(idx)
        delete_btn.clicked.connect(delete_clicked)

        self.creatingNewLabelSet = False

        if name:
            listItem = QtWidgets.QListWidgetItem()
            listItem.setText(name)
            self.selection_list.list_src.addItem(listItem)

        # self.ui.scrollArea.viewport().updateGeometry()
        # self.ui.scrollArea.viewport().update()
        # self.ui.scrollArea.updateGeometry()

    def delete_tag(self, idx):
        pass

    def select_color(self, idx):
        color = QtWidgets.QColorDialog.getColor()
        color_btn = self.findChild(
            QtWidgets.QPushButton, "btn_color_" + str(idx))
        pal = color_btn.palette()
        pal.setColor(QtGui.QPalette.Button, color)
        color_btn.setPalette(pal)
        self.labels[idx].color = color.rgb()

    def lineEditFinished(self, idx, input):
        value = self.findChild(
            QtWidgets.QLineEdit, "input_" + input + "_" + str(idx)).text()

        # self.labels[idx].getattr(input) = value
        setattr(self.labels[idx], input, value)

        # if input == "name":
        #     if idx < self.label_count - 1:
        #         return
        #
        #     if value != "":
        #         if not self.creatingNewLabelSet:
        #             self.create_label_form()

    def sendSettings(self):
        self.labels.remove_empty()
        # labels = [label for label in self.labels if label["name"]]
        self.settingsSig.emit(self.labels)


class KeySequenceEdit(QtWidgets.QLineEdit):
    """
    This class is mainly inspired by
    http://stackoverflow.com/a/6665017

    """

    def __init__(self, keySequence, *args):
        super(KeySequenceEdit, self).__init__(*args)

        self.keySequence = keySequence
        self.setKeySequence(keySequence)

    def setKeySequence(self, keySequence):
        self.keySequence = keySequence
        self.setText(self.keySequence.toString(QtGui.QKeySequence.NativeText))

    def keyPressEvent(self, e):
        if e.type() == QtCore.QEvent.KeyPress:
            key = e.key()

            if key == QtCore.Qt.Key_unknown:
                warnings.warn("Unknown key from a macro probably")
                return

            # the user have clicked just and only the special keys Ctrl, Shift, Alt, Meta.
            if(key == QtCore.Qt.Key_Control
               or key == QtCore.Qt.Key_Shift
               or key == QtCore.Qt.Key_Alt
               or key == QtCore.Qt.Key_Meta):
                print("Single click of special key: Ctrl, Shift, Alt or Meta")
                print("New KeySequence:", QtGui.QKeySequence(
                    key).toString(QtGui.QKeySequence.NativeText))
                return

            # check for a combination of user clicks
            modifiers = e.modifiers()
            keyText = e.text()
            # if the keyText is empty than it's a special key like F1, F5, ...
            print("Pressed Key:", keyText)

            if modifiers & QtCore.Qt.ShiftModifier:
                key += QtCore.Qt.SHIFT
            if modifiers & QtCore.Qt.ControlModifier:
                key += QtCore.Qt.CTRL
            if modifiers & QtCore.Qt.AltModifier:
                key += QtCore.Qt.ALT
            if modifiers & QtCore.Qt.MetaModifier:
                key += QtCore.Qt.META

            print("New KeySequence:", QtGui.QKeySequence(
                key).toString(QtGui.QKeySequence.NativeText))

            self.setKeySequence(QtGui.QKeySequence(key))


if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)

    w = ClassDialog(None)

    sys.exit(app.exec_())
