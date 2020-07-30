# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'manage_related_dialog.ui'
##
## Created by: Qt User Interface Compiler version 5.15.0
##
## WARNING! All changes made in this file will be lost when recompiling UI file!
################################################################################

from PySide2.QtCore import (QCoreApplication, QDate, QDateTime, QMetaObject,
    QObject, QPoint, QRect, QSize, QTime, QUrl, Qt)
from PySide2.QtGui import (QBrush, QColor, QConicalGradient, QCursor, QFont,
    QFontDatabase, QIcon, QKeySequence, QLinearGradient, QPalette, QPainter,
    QPixmap, QRadialGradient)
from PySide2.QtWidgets import *

from pyqtextra.common.selection_list import SelectionList


class Ui_ManageRelatedDialog(object):
    def setupUi(self, ManageRelatedDialog):
        if not ManageRelatedDialog.objectName():
            ManageRelatedDialog.setObjectName(u"ManageRelatedDialog")
        ManageRelatedDialog.resize(590, 473)
        self.verticalLayout = QVBoxLayout(ManageRelatedDialog)
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.label = QLabel(ManageRelatedDialog)
        self.label.setObjectName(u"label")
        font = QFont()
        font.setBold(True)
        font.setWeight(75)
        self.label.setFont(font)
        self.label.setWordWrap(True)

        self.verticalLayout.addWidget(self.label)

        self.selection_widget = SelectionList(ManageRelatedDialog)
        self.selection_widget.setObjectName(u"selection_widget")
        sizePolicy = QSizePolicy(QSizePolicy.Preferred, QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.selection_widget.sizePolicy().hasHeightForWidth())
        self.selection_widget.setSizePolicy(sizePolicy)

        self.verticalLayout.addWidget(self.selection_widget)

        self.buttonBox = QDialogButtonBox(ManageRelatedDialog)
        self.buttonBox.setObjectName(u"buttonBox")
        self.buttonBox.setOrientation(Qt.Horizontal)
        self.buttonBox.setStandardButtons(QDialogButtonBox.Cancel|QDialogButtonBox.Ok)

        self.verticalLayout.addWidget(self.buttonBox)


        self.retranslateUi(ManageRelatedDialog)
        self.buttonBox.accepted.connect(ManageRelatedDialog.accept)
        self.buttonBox.rejected.connect(ManageRelatedDialog.reject)

        QMetaObject.connectSlotsByName(ManageRelatedDialog)
    # setupUi

    def retranslateUi(self, ManageRelatedDialog):
        ManageRelatedDialog.setWindowTitle(QCoreApplication.translate("ManageRelatedDialog", u"Add or remove related tags", None))
        self.label.setText(QCoreApplication.translate("ManageRelatedDialog", u"Adding a tag will also add all its related tags. Removing a tag will remove related tags if no other tag is related to it", None))
    # retranslateUi

