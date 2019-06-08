from PySide2 import QtGui, QtWidgets

from AudioTagger.tag_form_ui import Ui_TagForm
from AudioTagger.tags import Tag


class TagForm(QtWidgets.QWidget, Ui_TagForm):

    def __init__(self, parent, tag=None):
        super().__init__(parent)
        self.setupUi(self)
        color = QtGui.QColor()
        if not tag:
            name = ""
            color.setRgb(255, 0, 127)
            keyseq = ""  # int(QtCore.Qt.Key_0) + self.label_count + 1
            tag = Tag(0, name, color.rgb(), keyseq)
        self.tag = tag
        self.link_signals()
        self.load_data()

    def link_signals(self):
        self.input_name.editingFinished.connect(self.new_name)
        self.input_keyseq.editingFinished.connect(self.new_keyseq)
        self.btn_color.clicked.connect(self.color_clicked)
        self.btn_delete.clicked.connect(self.delete_clicked)

    def load_data(self):
        idx = self.tag.id
        name = self.tag.name
        color = QtGui.QColor()
        color = color.fromRgb(int(self.tag.color))
        keyseq = self.tag.keyseq

        label_id = str(idx)

        # Tag name input
        self.input_name.setObjectName("input_name_" + label_id)
        self.input_name.setText(name)

        # Color selection button
        pal = self.btn_color.palette()
        pal.setColor(QtGui.QPalette.Button, color)
        self.btn_color.setPalette(pal)
        self.btn_color.setObjectName("btn_color_" + label_id)

        # Shortcut input
        self.input_keyseq.setKeySequence(keyseq)
        self.input_keyseq.setObjectName("input_keyseq_" + label_id)

        # Delete button
        self.btn_delete.setObjectName("delete_btn_" + label_id)

    def select_color(self):
        color = QtWidgets.QColorDialog.getColor()
        pal = self.btn_color.palette()
        pal.setColor(QtGui.QPalette.Button, color)
        self.btn_color.setPalette(pal)
        self.tag.color = color.rgb()

    def lineEditFinished(self, input_name):
        value = getattr(self, "input_" + input_name).text()
        setattr(self.tag, input_name, value)

    def new_name(self):
        return self.lineEditFinished("name")

    def color_clicked(self):
        return self.select_color()

    def new_keyseq(self):
        return self.lineEditFinished("keyseq")

    def delete_clicked(self):
        pass
