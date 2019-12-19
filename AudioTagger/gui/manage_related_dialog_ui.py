# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'manage_related_dialog.ui',
# licensing of 'manage_related_dialog.ui' applies.
#
# Created: Mon Aug 26 22:47:34 2019
#      by: pyside2-uic  running on PySide2 5.12.2
#
# WARNING! All changes made in this file will be lost!

from PySide2 import QtCore, QtGui, QtWidgets

class Ui_ManageRelatedDialog(object):
    def setupUi(self, ManageRelatedDialog):
        ManageRelatedDialog.setObjectName("ManageRelatedDialog")
        ManageRelatedDialog.resize(590, 473)
        self.verticalLayout = QtWidgets.QVBoxLayout(ManageRelatedDialog)
        self.verticalLayout.setObjectName("verticalLayout")
        self.label = QtWidgets.QLabel(ManageRelatedDialog)
        font = QtGui.QFont()
        font.setWeight(75)
        font.setBold(True)
        self.label.setFont(font)
        self.label.setWordWrap(True)
        self.label.setObjectName("label")
        self.verticalLayout.addWidget(self.label)
        self.selection_widget = SelectionListWidget(ManageRelatedDialog)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.selection_widget.sizePolicy().hasHeightForWidth())
        self.selection_widget.setSizePolicy(sizePolicy)
        self.selection_widget.setObjectName("selection_widget")
        self.verticalLayout.addWidget(self.selection_widget)
        self.buttonBox = QtWidgets.QDialogButtonBox(ManageRelatedDialog)
        self.buttonBox.setOrientation(QtCore.Qt.Horizontal)
        self.buttonBox.setStandardButtons(QtWidgets.QDialogButtonBox.Cancel|QtWidgets.QDialogButtonBox.Ok)
        self.buttonBox.setObjectName("buttonBox")
        self.verticalLayout.addWidget(self.buttonBox)

        self.retranslateUi(ManageRelatedDialog)
        QtCore.QObject.connect(self.buttonBox, QtCore.SIGNAL("accepted()"), ManageRelatedDialog.accept)
        QtCore.QObject.connect(self.buttonBox, QtCore.SIGNAL("rejected()"), ManageRelatedDialog.reject)
        QtCore.QMetaObject.connectSlotsByName(ManageRelatedDialog)

    def retranslateUi(self, ManageRelatedDialog):
        ManageRelatedDialog.setWindowTitle(QtWidgets.QApplication.translate("ManageRelatedDialog", "Add or remove related tags", None, -1))
        self.label.setText(QtWidgets.QApplication.translate("ManageRelatedDialog", "Adding a tag will also add all its related tags. Removing a tag will remove related tags if no other tag is related to it", None, -1))

from AudioTagger.selectionListWidget import SelectionListWidget
