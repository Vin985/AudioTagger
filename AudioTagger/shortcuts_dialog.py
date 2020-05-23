from AudioTagger.gui.shortcuts_dialog_ui import Ui_ShortcutsDialog
from PySide2 import QtWidgets, QtGui


class ShortcutsDialog(QtWidgets.QDialog, Ui_ShortcutsDialog):

    KEYBOARD_SHORTCUTS = {
        "Left": "Previous tag",
        "Right": "Next tag"}

    MOUSE_SHORTCUTS = {
        "Double click": "Select tag"
    }

    DEFAULT_CELL_MARGIN = 3

    def __init__(self, parent):
        super().__init__(parent)
        self.setupUi(self)
        self.bold_font = QtGui.QFont()
        self.bold_font.setBold(True)
        self.bold_font.setWeight(75)

        self.keyboard_shortcuts = {}
        self.mouse_shortcuts = {}
        self.create_texts()

        self.populate()

    def create_texts(self):
        self.keyboard_shortcuts = {
            # "": [self.tr(""), self.tr("")],
            "left": [self.tr("Left"), self.tr("Previous tag")],
            "right": [self.tr("Right"), self.tr("Next tag")],
            "ctrl_left": [self.tr("Ctrl + Left"), self.tr("Load previous file")],
            "ctrl_right": [self.tr("Ctrl + Right"), self.tr("Load next tag")],
            "space": [self.tr("Space"), self.tr("Play/pause audio")],
            "esc": [self.tr("Esc"), self.tr("Deselect tag/Cancel edit")],
            "del": [self.tr("Del"), self.tr("Delete tag")],
            "tab": [self.tr("Tab"), self.tr("Next tag")],
            "shift": [self.tr("Shift (held)"), self.tr("Edit mode")],
            "b": [self.tr("B"), self.tr("Set in background")],
            "s": [self.tr("S"), self.tr("Seek audio position")],
            "r": [self.tr("R"), self.tr("Add rain")],
            "w": [self.tr("W"), self.tr("Add wind")],
            "ctrl_s": [self.tr("Ctrl + S"), self.tr("Save file")]
        }
        self.mouse_shortcuts = {
            # "": [self.tr(""), self.tr("")],
            "left_click": [self.tr("Left click (held)"), self.tr("Draw tag bounding box")],
            "double_click": [self.tr("Double click"), self.tr("Select tag")],
            "middle_click": [self.tr("Middle click"), self.tr("Play audio from position")],
            "ctrl_wheel": [self.tr("Ctrl + wheel"), self.tr("Zoom in/Zoom out")],
        }

    def populate(self):
        for i, (k, v) in enumerate(self.keyboard_shortcuts.items()):
            self.add_shortcut(i, 0, v[0], v[1])
        for i, (k, v) in enumerate(self.mouse_shortcuts.items()):
            self.add_shortcut(i, 2, v[0], v[1])

    def add_shortcut(self, row, column, key, desc):
        self.add_label(row, column, key, key=True)
        self.add_label(row, column + 1, desc, key=False)

    # def add_key(self, idx, key):
    #     label = QtWidgets.QLabel(self)
    #     label.setObjectName(u"key_" + str(idx))
    #     label.setFont(self.bold_font)
    #     label.setMargin(3)
    #     self.gridLayout.addWidget(label, idx + 2, 0, 1, 1)

    # def add_description(self, idx, desc):
    #     label = QtWidgets.QLabel(self)
    #     label.setObjectName(u"desc_" + str(idx))
    #     label.setMargin(3)
    #     self.gridLayout.addWidget(label, idx + 2, 1, 1, 1)

    def add_label(self, row, column, text, key=False):
        label = QtWidgets.QLabel(self)
        name = "desc_"
        if key:
            label.setFont(self.bold_font)
            name = "key_"
        label.setObjectName(name + str(row))
        label.setMargin(3)
        label.setText(text)
        self.gridLayout.addWidget(label, row + 2, column, 1, 1)
