from PySide2 import QtCore, QtWidgets


class AutoCompleteLineEdit(QtWidgets.QLineEdit):
    def __init__(self, *args, **kwargs):
        super(AutoCompleteLineEdit, self).__init__(*args, **kwargs)
        self.comp = QtWidgets.QCompleter([""], self)
        self.comp.setCaseSensitivity(QtCore.Qt.CaseInsensitive)
        self.setCompleter(self.comp)
        self.setModel(["hallo", "world", "we", "are"])

    def setModel(self, strList):
        self.comp.model().setStringList(strList)


class ContextLineEdit(QtWidgets.QWidget):
    def __init__(self, action, *args, **kwargs):
        super(ContextLineEdit, self).__init__(*args, **kwargs)
        self.action = action

        self.label = QtWidgets.QLabel(self)
        self.label.setText("change label to ")
        self.autoCompeleteLineEdit = AutoCompleteLineEdit(self)

        self.layout = QtWidgets.QHBoxLayout()
        self.layout.addWidget(self.label)
        self.layout.addWidget(self.autoCompeleteLineEdit)

        self.setLayout(self.layout)

        self.autoCompeleteLineEdit.returnPressed.connect(action.trigger)

    def text(self):
        return self.autoCompeleteLineEdit.text()

    def setModel(self, strList):
        self.autoCompeleteLineEdit.setModel(strList)
