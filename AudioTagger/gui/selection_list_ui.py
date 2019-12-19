# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'selection_list.ui',
# licensing of 'selection_list.ui' applies.
#
# Created: Wed Aug 28 13:43:08 2019
#      by: pyside2-uic  running on PySide2 5.12.2
#
# WARNING! All changes made in this file will be lost!

from PySide2 import QtCore, QtGui, QtWidgets

class Ui_SelectionList(object):
    def setupUi(self, SelectionList):
        SelectionList.setObjectName("SelectionList")
        SelectionList.resize(548, 444)
        self.horizontalLayout = QtWidgets.QHBoxLayout(SelectionList)
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.list_src = QtWidgets.QListWidget(SelectionList)
        self.list_src.setObjectName("list_src")
        self.horizontalLayout.addWidget(self.list_src)
        self.verticalLayout = QtWidgets.QVBoxLayout()
        self.verticalLayout.setContentsMargins(20, -1, 20, -1)
        self.verticalLayout.setObjectName("verticalLayout")
        spacerItem = QtWidgets.QSpacerItem(20, 40, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding)
        self.verticalLayout.addItem(spacerItem)
        self.btn_add = QtWidgets.QPushButton(SelectionList)
        self.btn_add.setText("")
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap(":/icons/right"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.btn_add.setIcon(icon)
        self.btn_add.setFlat(True)
        self.btn_add.setObjectName("btn_add")
        self.verticalLayout.addWidget(self.btn_add)
        self.btn_remove = QtWidgets.QPushButton(SelectionList)
        self.btn_remove.setText("")
        icon1 = QtGui.QIcon()
        icon1.addPixmap(QtGui.QPixmap(":/icons/left"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.btn_remove.setIcon(icon1)
        self.btn_remove.setFlat(True)
        self.btn_remove.setObjectName("btn_remove")
        self.verticalLayout.addWidget(self.btn_remove)
        spacerItem1 = QtWidgets.QSpacerItem(20, 40, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding)
        self.verticalLayout.addItem(spacerItem1)
        self.horizontalLayout.addLayout(self.verticalLayout)
        self.list_dest = QtWidgets.QListWidget(SelectionList)
        self.list_dest.setObjectName("list_dest")
        self.horizontalLayout.addWidget(self.list_dest)

        self.retranslateUi(SelectionList)
        QtCore.QMetaObject.connectSlotsByName(SelectionList)

    def retranslateUi(self, SelectionList):
        SelectionList.setWindowTitle(QtWidgets.QApplication.translate("SelectionList", "Form", None, -1))
        self.list_src.setSortingEnabled(True)
        self.list_dest.setSortingEnabled(True)

import resources_rc
