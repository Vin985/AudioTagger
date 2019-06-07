# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'classDialog2.ui',
# licensing of 'classDialog2.ui' applies.
#
# Created: Thu Jun  6 15:04:12 2019
#      by: pyside2-uic  running on PySide2 5.12.2
#
# WARNING! All changes made in this file will be lost!

from PySide2 import QtCore, QtGui, QtWidgets

class Ui_Dialog(object):
    def setupUi(self, Dialog):
        Dialog.setObjectName("Dialog")
        Dialog.resize(841, 257)
        self.verticalLayout = QtWidgets.QVBoxLayout(Dialog)
        self.verticalLayout.setObjectName("verticalLayout")
        self.gridLayout = QtWidgets.QGridLayout()
        self.gridLayout.setObjectName("gridLayout")
        self.label_5 = QtWidgets.QLabel(Dialog)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Maximum, QtWidgets.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.label_5.sizePolicy().hasHeightForWidth())
        self.label_5.setSizePolicy(sizePolicy)
        self.label_5.setText("")
        self.label_5.setObjectName("label_5")
        self.gridLayout.addWidget(self.label_5, 0, 4, 1, 1)
        self.label = QtWidgets.QLabel(Dialog)
        self.label.setStyleSheet("font-weight: bold")
        self.label.setTextFormat(QtCore.Qt.PlainText)
        self.label.setObjectName("label")
        self.gridLayout.addWidget(self.label, 0, 0, 1, 1)
        self.label_2 = QtWidgets.QLabel(Dialog)
        self.label_2.setStyleSheet("font-weight: bold")
        self.label_2.setObjectName("label_2")
        self.gridLayout.addWidget(self.label_2, 0, 1, 1, 1)
        self.label_4 = QtWidgets.QLabel(Dialog)
        self.label_4.setStyleSheet("font-weight: bold")
        self.label_4.setObjectName("label_4")
        self.gridLayout.addWidget(self.label_4, 0, 3, 1, 1)
        self.label_3 = QtWidgets.QLabel(Dialog)
        self.label_3.setStyleSheet("font-weight: bold")
        self.label_3.setObjectName("label_3")
        self.gridLayout.addWidget(self.label_3, 0, 2, 1, 1)
        self.verticalLayout.addLayout(self.gridLayout)
        spacerItem = QtWidgets.QSpacerItem(20, 40, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding)
        self.verticalLayout.addItem(spacerItem)
        self.comboBox = QtWidgets.QComboBox(Dialog)
        self.comboBox.setObjectName("comboBox")
        self.comboBox.addItem("")
        self.comboBox.addItem("")
        self.comboBox.addItem("")
        self.verticalLayout.addWidget(self.comboBox)
        self.horizontalLayout = QtWidgets.QHBoxLayout()
        self.horizontalLayout.setContentsMargins(-1, 15, -1, 15)
        self.horizontalLayout.setObjectName("horizontalLayout")
        spacerItem1 = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout.addItem(spacerItem1)
        self.btn_add = QtWidgets.QPushButton(Dialog)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Maximum, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.btn_add.sizePolicy().hasHeightForWidth())
        self.btn_add.setSizePolicy(sizePolicy)
        self.btn_add.setStyleSheet("font-weight:bold")
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap(":/icons/add"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.btn_add.setIcon(icon)
        self.btn_add.setIconSize(QtCore.QSize(16, 16))
        self.btn_add.setFlat(False)
        self.btn_add.setObjectName("btn_add")
        self.horizontalLayout.addWidget(self.btn_add)
        self.verticalLayout.addLayout(self.horizontalLayout)
        self.selection_list = SelectionListWidget(Dialog)
        self.selection_list.setObjectName("selection_list")
        self.verticalLayout.addWidget(self.selection_list)
        self.buttonBox = QtWidgets.QDialogButtonBox(Dialog)
        self.buttonBox.setOrientation(QtCore.Qt.Horizontal)
        self.buttonBox.setStandardButtons(QtWidgets.QDialogButtonBox.Apply|QtWidgets.QDialogButtonBox.Cancel|QtWidgets.QDialogButtonBox.Ok)
        self.buttonBox.setObjectName("buttonBox")
        self.verticalLayout.addWidget(self.buttonBox)

        self.retranslateUi(Dialog)
        QtCore.QObject.connect(self.buttonBox, QtCore.SIGNAL("accepted()"), Dialog.accept)
        QtCore.QObject.connect(self.buttonBox, QtCore.SIGNAL("rejected()"), Dialog.reject)
        QtCore.QMetaObject.connectSlotsByName(Dialog)

    def retranslateUi(self, Dialog):
        Dialog.setWindowTitle(QtWidgets.QApplication.translate("Dialog", "Dialog", None, -1))
        self.label.setText(QtWidgets.QApplication.translate("Dialog", "Tag name", None, -1))
        self.label_2.setText(QtWidgets.QApplication.translate("Dialog", "Color", None, -1))
        self.label_4.setText(QtWidgets.QApplication.translate("Dialog", "Shortcut", None, -1))
        self.label_3.setText(QtWidgets.QApplication.translate("Dialog", "Related tags", None, -1))
        self.comboBox.setItemText(0, QtWidgets.QApplication.translate("Dialog", "New Item", None, -1))
        self.comboBox.setItemText(1, QtWidgets.QApplication.translate("Dialog", "New Item", None, -1))
        self.comboBox.setItemText(2, QtWidgets.QApplication.translate("Dialog", "New Item", None, -1))
        self.btn_add.setText(QtWidgets.QApplication.translate("Dialog", "  Add new tag", None, -1))

from AudioTagger.selectionListWidget import SelectionListWidget
import resources_rc
