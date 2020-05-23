# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'shortcuts_dialog2.ui'
##
## Created by: Qt User Interface Compiler version 5.14.1
##
## WARNING! All changes made in this file will be lost when recompiling UI file!
################################################################################

from PySide2.QtCore import (QCoreApplication, QMetaObject, QObject, QPoint,
    QRect, QSize, QUrl, Qt)
from PySide2.QtGui import (QBrush, QColor, QConicalGradient, QCursor, QFont,
    QFontDatabase, QIcon, QLinearGradient, QPalette, QPainter, QPixmap,
    QRadialGradient)
from PySide2.QtWidgets import *


class Ui_ShortcutsDialog(object):
    def setupUi(self, ShortcutsDialog):
        if ShortcutsDialog.objectName():
            ShortcutsDialog.setObjectName(u"ShortcutsDialog")
        ShortcutsDialog.resize(563, 514)
        self.verticalLayout = QVBoxLayout(ShortcutsDialog)
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.gridLayout = QGridLayout()
        self.gridLayout.setObjectName(u"gridLayout")
        self.label_13 = QLabel(ShortcutsDialog)
        self.label_13.setObjectName(u"label_13")
        font = QFont()
        font.setBold(True)
        font.setWeight(75)
        self.label_13.setFont(font)
        self.label_13.setMargin(3)

        self.gridLayout.addWidget(self.label_13, 1, 0, 1, 2)

        self.label_15 = QLabel(ShortcutsDialog)
        self.label_15.setObjectName(u"label_15")
        self.label_15.setFont(font)
        self.label_15.setMargin(3)

        self.gridLayout.addWidget(self.label_15, 1, 2, 1, 2)

        self.label_3 = QLabel(ShortcutsDialog)
        self.label_3.setObjectName(u"label_3")
        font1 = QFont()
        font1.setPointSize(10)
        font1.setBold(True)
        font1.setWeight(75)
        self.label_3.setFont(font1)
        self.label_3.setMargin(5)

        self.gridLayout.addWidget(self.label_3, 0, 0, 1, 4)


        self.verticalLayout.addLayout(self.gridLayout)

        self.verticalSpacer_2 = QSpacerItem(20, 40, QSizePolicy.Minimum, QSizePolicy.Expanding)

        self.verticalLayout.addItem(self.verticalSpacer_2)

        self.horizontalLayout = QHBoxLayout()
        self.horizontalLayout.setObjectName(u"horizontalLayout")
        self.buttonBox = QDialogButtonBox(ShortcutsDialog)
        self.buttonBox.setObjectName(u"buttonBox")
        self.buttonBox.setOrientation(Qt.Horizontal)
        self.buttonBox.setStandardButtons(QDialogButtonBox.Cancel|QDialogButtonBox.Ok)

        self.horizontalLayout.addWidget(self.buttonBox)


        self.verticalLayout.addLayout(self.horizontalLayout)


        self.retranslateUi(ShortcutsDialog)
        self.buttonBox.accepted.connect(ShortcutsDialog.accept)
        self.buttonBox.rejected.connect(ShortcutsDialog.reject)

        QMetaObject.connectSlotsByName(ShortcutsDialog)
    # setupUi

    def retranslateUi(self, ShortcutsDialog):
        ShortcutsDialog.setWindowTitle(QCoreApplication.translate("ShortcutsDialog", u"Dialog", None))
        self.label_13.setText(QCoreApplication.translate("ShortcutsDialog", u"Keyboard", None))
        self.label_15.setText(QCoreApplication.translate("ShortcutsDialog", u"Mouse", None))
        self.label_3.setText(QCoreApplication.translate("ShortcutsDialog", u"List of AudioTagger shortcuts", None))
    # retranslateUi

