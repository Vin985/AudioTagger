import warnings

from PySide2 import QtCore, QtGui, QtWidgets


class KeySequenceEdit(QtWidgets.QLineEdit):
    """
    This class is mainly inspired by
    http://stackoverflow.com/a/6665017

    """

    def __init__(self, *args, keySequence=""):
        super().__init__(*args)
        self.setKeySequence(keySequence)

    def setKeySequence(self, keySequence):
        keySeq = QtGui.QKeySequence(keySequence)
        self.keySequence = keySeq
        self.setText(self.keySequence.toString(QtGui.QKeySequence.NativeText))

    def keyPressEvent(self, e):
        if e.type() == QtCore.QEvent.KeyPress:
            key = e.key()

            if key in (QtCore.Qt.Key_Delete, QtCore.Qt.Key_Backspace):
                self.setKeySequence("")
                return

            if key == QtCore.Qt.Key_unknown:
                warnings.warn("Unknown key from a macro probably")
                return

            # the user have clicked just and only the special keys Ctrl, Shift, Alt, Meta.
            if key in (QtCore.Qt.Key_Control, QtCore.Qt.Key_Shift,
                       QtCore.Qt.Key_Alt, QtCore.Qt.Key_Meta):
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
