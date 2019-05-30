__author__ = 'peter'

import copy
import sys
import warnings
from collections import OrderedDict

from PySide2 import QtCore, QtGui, QtWidgets

from AudioTagger.classDialog_auto import Ui_Dialog


class ClassDialog(QtWidgets.QDialog):
    settingsSig = QtCore.Signal(list)

    def __init__(self, parent, labels):
        super(ClassDialog, self).__init__(parent)
        # Usual setup stuff. Set up the user interface from Designer
        self.ui = Ui_Dialog()
        self.ui.setupUi(self)

        self.connectSignals()

        # self.labelSetCnt = 0
        self.label_count = 0
        self.labels = labels
        self.creatingNewLabelSet = False
        # self.classUIs = []

        for label in labels:
            self.create_label_form(label)
        self.create_label_form()

        # self.classSettings = []
        # if classSettings is not None:
        #     classSettings = copy.copy(classSettings)
        #     while(True):
        #         try:
        #             k, c = classSettings.popitem(last=False)
        #             self.classSettings += [[k, c]]
        #             self.createNewLabelSet(k, c)
        #         except KeyError:
        #             break
        #
        # if keySequences:
        #     for i, edit in enumerate(zip(*self.classUIs)):
        #         if i < len(keySequences):
        #             edit.setKeySequence(keySequences[i])
        #         else:
        #             break

        # self.createNewLabelSet()

    def getSettings(self):
        self.show()

    def connectSignals(self):
        self.ui.buttonBox.accepted.connect(self.sendSettings)
        applyButton = self.ui.buttonBox.button(
            QtWidgets.QDialogButtonBox.Apply)
        applyButton.clicked.connect(self.sendSettings)

    def setLabelColor(self, label, color):
        colourStyle = "background-color: {0}".format(color.name())
        label.setStyleSheet(colourStyle)

    def create_label_form(self, label=None):
        self.creatingNewLabelSet = True

        color = QtGui.QColor()
        if not label:
            name = ""
            color.setRgb(255, 0, 127)
            keyseq = self.label_count
        else:
            name = label["name"]
            color = color.fromRgb(int(label["color"]))
            keyseq = label["keyseq"]

        label_id = str(self.label_count)

        label = QtWidgets.QLabel("Label {0}".format(self.label_count), self)
        label.setObjectName("lbl_name_" + label_id)

        name_input = QtWidgets.QLineEdit(self)
        name_input.setObjectName("input_name_" + label_id)
        name_input.setText(name)

        colourLbl = QtWidgets.QLabel("       ", self)
        colourLbl.setObjectName("lbl_colour_" + label_id)
        self.setLabelColor(colourLbl, color)

        button = QtWidgets.QPushButton(self)
        button.setObjectName("btn_color_" + label_id)
        button.setText("Select colour")

        klabel = QtWidgets.QLabel("Keyboard shortcut: ", self)
        klabel.setObjectName("lbl_keyseq_" + label_id)

        # TODO: looks fishy... doesnt use the loaded value
        keySeq = QtGui.QKeySequence(int(QtCore.Qt.Key_0) + self.label_count)

        keyEdit = KeySequenceEdit(keySeq, self)
        keyEdit.setObjectName("input_keyseq_" + label_id)

        self.ui.gridLayout.addWidget(label, self.label_count, 0, 1, 1)
        self.ui.gridLayout.addWidget(name_input, self.label_count, 1, 1, 1)
        self.ui.gridLayout.addWidget(colourLbl, self.label_count, 2, 1, 1)
        self.ui.gridLayout.addWidget(button, self.label_count, 3, 1, 1)
        self.ui.gridLayout.addWidget(klabel, self.label_count, 4, 1, 1)
        self.ui.gridLayout.addWidget(keyEdit, self.label_count, 5, 1, 1)

        idx = self.label_count
        def btnCon(): return self.selectColor(idx)
        button.clicked.connect(btnCon)

        def new_name(): return self.lineEditFinished(idx, "name")
        name_input.editingFinished.connect(new_name)

        def new_keyseq(): return self.lineEditFinished(idx, "keyseq")
        keyEdit.editingFinished.connect(new_keyseq)

        if len(self.labels) <= self.label_count:
            self.labels.append(
                {"name": name, "color": color.rgb(), "keyseq": keyseq})

        self.label_count += 1
        self.creatingNewLabelSet = False

        self.ui.scrollArea.viewport().updateGeometry()
        self.ui.scrollArea.viewport().update()
        self.ui.scrollArea.updateGeometry()

        # scroll->viewport()->updateGeometry();
        # scroll->viewport()->update();
        # scroll->update();

    # def createNewLabelSet(self, className=None, classColor=None, keyName=None):
    #     self.creatingNewLabelSet = True
    #     if className is None:
    #         className = ""
    #
    #     if classColor is None:
    #         classColor = QtGui.QColor()
    #         classColor.setRgb(255, 0, 127)
    #
    #     if keyName is None:
    #         keyName = self.labelSetCnt
    #
    #     label = QtWidgets.QLabel("Class {0}".format(self.labelSetCnt), self)
    #     edit = QtWidgets.QLineEdit(self)
    #     edit.setText(className)
    #
    #     colourLbl = QtWidgets.QLabel("       ".format(self.labelSetCnt), self)
    #     self.setLabelColor(colourLbl, classColor)
    #
    #     button = QtWidgets.QPushButton(self)
    #     button.setText("select colour")
    #
    #     klabel = QtWidgets.QLabel("Keyboard shortcut: ", self)
    #     keySeq = QtGui.QKeySequence(int(QtCore.Qt.Key_0) + self.labelSetCnt)
    #     keyEdit = KeySequenceEdit(keySeq, self)
    #     # edit.setText(className)
    #
    #     self.ui.gridLayout.addWidget(label, self.labelSetCnt, 0, 1, 1)
    #     self.ui.gridLayout.addWidget(edit, self.labelSetCnt, 1, 1, 1)
    #     self.ui.gridLayout.addWidget(colourLbl, self.labelSetCnt, 2, 1, 1)
    #     self.ui.gridLayout.addWidget(button, self.labelSetCnt, 3, 1, 1)
    #     self.ui.gridLayout.addWidget(klabel, self.labelSetCnt, 4, 1, 1)
    #     self.ui.gridLayout.addWidget(keyEdit, self.labelSetCnt, 5, 1, 1)
    #
    #     idx = int(self.labelSetCnt)
    #     def btnCon(): return self.selectColor(idx)
    #     button.clicked.connect(btnCon)
    #
    #     def leCon(): return self.lineEditFinished(idx)
    #     edit.editingFinished.connect(leCon)
    #
    #     self.classUIs += [[label, edit, colourLbl, button, keyEdit]]
    #
    #     if len(self.classSettings) <= self.labelSetCnt:
    #         self.classSettings += [[className, classColor]]
    #
    #     self.labelSetCnt += 1
    #     self.creatingNewLabelSet = False
    #
    #     self.ui.scrollArea.viewport().updateGeometry()
    #     self.ui.scrollArea.viewport().update()
    #     self.ui.scrollArea.updateGeometry()
    #
    #     # scroll->viewport()->updateGeometry();
    #     # scroll->viewport()->update();
    #     # scroll->update();

    def selectColor(self, idx):
        color = QtWidgets.QColorDialog.getColor()
        self.setLabelColor(self.findChild(
            QtWidgets.QLabel, "lbl_colour_" + str(idx)), color)
        self.labels[idx]["color"] = color.rgb()

    def lineEditFinished(self, idx, input):
        value = self.findChild(
            QtWidgets.QLineEdit, "input_" + input + "_" + str(idx)).text()

        self.labels[idx][input] = value

        if input == "name":
            if idx < self.label_count - 1:
                return

            if value != "":
                if not self.creatingNewLabelSet:
                    self.create_label_form()

    def sendSettings(self):
        self.settingsSig.emit(self.labels)
        # classSettings = OrderedDict()
        # for k, c in self.classSettings:
        #     if k != '':
        #         classSettings[k] = c
        #
        # keySequences = []
        # for cLbl, e, cLbl, b, keyEdit in self.classUIs:
        #     keySequences += [keyEdit.keySequence]
        #
        # # print("classSettings", classSettings)
        # # print("keySequences", keySequences)
        # self.settingsSig.emit([classSettings, keySequences])


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
