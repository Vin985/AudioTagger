# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'tag_form.ui',
# licensing of 'tag_form.ui' applies.
#
# Created: Fri Jun  7 16:42:19 2019
#      by: pyside2-uic  running on PySide2 5.12.2
#
# WARNING! All changes made in this file will be lost!

from PySide2 import QtCore, QtGui, QtWidgets

class Ui_TagForm(object):
    def setupUi(self, TagForm):
        TagForm.setObjectName("TagForm")
        TagForm.resize(719, 55)
        self.horizontalLayout = QtWidgets.QHBoxLayout(TagForm)
        self.horizontalLayout.setContentsMargins(0, 0, 0, 0)
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.input_name = QtWidgets.QLineEdit(TagForm)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.input_name.sizePolicy().hasHeightForWidth())
        self.input_name.setSizePolicy(sizePolicy)
        self.input_name.setObjectName("input_name")
        self.horizontalLayout.addWidget(self.input_name)
        self.btn_color = QtWidgets.QPushButton(TagForm)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.btn_color.sizePolicy().hasHeightForWidth())
        self.btn_color.setSizePolicy(sizePolicy)
        self.btn_color.setAutoFillBackground(True)
        self.btn_color.setText("")
        self.btn_color.setObjectName("btn_color")
        self.horizontalLayout.addWidget(self.btn_color)
        self.lbl_related = QtWidgets.QLabel(TagForm)
        self.lbl_related.setObjectName("lbl_related")
        self.horizontalLayout.addWidget(self.lbl_related)
        self.btn_add_related = QtWidgets.QPushButton(TagForm)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Maximum, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.btn_add_related.sizePolicy().hasHeightForWidth())
        self.btn_add_related.setSizePolicy(sizePolicy)
        self.btn_add_related.setText("")
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap(":/icons/add"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.btn_add_related.setIcon(icon)
        self.btn_add_related.setFlat(True)
        self.btn_add_related.setObjectName("btn_add_related")
        self.horizontalLayout.addWidget(self.btn_add_related)
        self.input_keyseq = KeySequenceEdit(TagForm)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Maximum, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.input_keyseq.sizePolicy().hasHeightForWidth())
        self.input_keyseq.setSizePolicy(sizePolicy)
        self.input_keyseq.setObjectName("input_keyseq")
        self.horizontalLayout.addWidget(self.input_keyseq)
        self.btn_delete = QtWidgets.QPushButton(TagForm)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Maximum, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.btn_delete.sizePolicy().hasHeightForWidth())
        self.btn_delete.setSizePolicy(sizePolicy)
        self.btn_delete.setText("")
        icon1 = QtGui.QIcon()
        icon1.addPixmap(QtGui.QPixmap(":/icons/delete"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.btn_delete.setIcon(icon1)
        self.btn_delete.setFlat(True)
        self.btn_delete.setObjectName("btn_delete")
        self.horizontalLayout.addWidget(self.btn_delete)

        self.retranslateUi(TagForm)
        QtCore.QMetaObject.connectSlotsByName(TagForm)

    def retranslateUi(self, TagForm):
        TagForm.setWindowTitle(QtWidgets.QApplication.translate("TagForm", "Form", None, -1))
        self.input_name.setPlaceholderText(QtWidgets.QApplication.translate("TagForm", "Tag name", None, -1))
        self.lbl_related.setText(QtWidgets.QApplication.translate("TagForm", "No related tags found", None, -1))
        self.btn_add_related.setToolTip(QtWidgets.QApplication.translate("TagForm", "Add related tag", None, -1))
        self.input_keyseq.setPlaceholderText(QtWidgets.QApplication.translate("TagForm", "Key shortcut", None, -1))
        self.btn_delete.setToolTip(QtWidgets.QApplication.translate("TagForm", "Delete tag", None, -1))

from AudioTagger.keysequenceedit import KeySequenceEdit
import resources_rc
