# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'spectrogram_options.ui',
# licensing of 'spectrogram_options.ui' applies.
#
# Created: Mon Jan 27 16:40:35 2020
#      by: pyside2-uic  running on PySide2 5.12.2
#
# WARNING! All changes made in this file will be lost!

from PySide2 import QtCore, QtGui, QtWidgets

class Ui_SpectrogramOptions(object):
    def setupUi(self, SpectrogramOptions):
        SpectrogramOptions.setObjectName("SpectrogramOptions")
        SpectrogramOptions.resize(351, 225)
        self.horizontalLayout_2 = QtWidgets.QHBoxLayout(SpectrogramOptions)
        self.horizontalLayout_2.setObjectName("horizontalLayout_2")
        self.groupBox = QtWidgets.QGroupBox(SpectrogramOptions)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Maximum, QtWidgets.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(2)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.groupBox.sizePolicy().hasHeightForWidth())
        self.groupBox.setSizePolicy(sizePolicy)
        self.groupBox.setObjectName("groupBox")
        self.verticalLayout_3 = QtWidgets.QVBoxLayout(self.groupBox)
        self.verticalLayout_3.setContentsMargins(0, -1, -1, -1)
        self.verticalLayout_3.setObjectName("verticalLayout_3")
        self.horizontalLayout_15 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_15.setObjectName("horizontalLayout_15")
        self.cb_followSound = QtWidgets.QCheckBox(self.groupBox)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Maximum, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.cb_followSound.sizePolicy().hasHeightForWidth())
        self.cb_followSound.setSizePolicy(sizePolicy)
        self.cb_followSound.setObjectName("cb_followSound")
        self.horizontalLayout_15.addWidget(self.cb_followSound)
        spacerItem = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout_15.addItem(spacerItem)
        self.verticalLayout_3.addLayout(self.horizontalLayout_15)
        self.horizontalLayout = QtWidgets.QHBoxLayout()
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.label_2 = QtWidgets.QLabel(self.groupBox)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.label_2.sizePolicy().hasHeightForWidth())
        self.label_2.setSizePolicy(sizePolicy)
        self.label_2.setAlignment(QtCore.Qt.AlignLeading|QtCore.Qt.AlignLeft|QtCore.Qt.AlignVCenter)
        self.label_2.setObjectName("label_2")
        self.horizontalLayout.addWidget(self.label_2)
        self.cb_specType = QtWidgets.QComboBox(self.groupBox)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.cb_specType.sizePolicy().hasHeightForWidth())
        self.cb_specType.setSizePolicy(sizePolicy)
        self.cb_specType.setObjectName("cb_specType")
        self.cb_specType.addItem("")
        self.cb_specType.addItem("")
        self.horizontalLayout.addWidget(self.cb_specType)
        spacerItem1 = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout.addItem(spacerItem1)
        self.verticalLayout_3.addLayout(self.horizontalLayout)
        self.horizontalLayout_6 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_6.setObjectName("horizontalLayout_6")
        self.label_8 = QtWidgets.QLabel(self.groupBox)
        self.label_8.setObjectName("label_8")
        self.horizontalLayout_6.addWidget(self.label_8)
        self.slider_contrast = QtWidgets.QSlider(self.groupBox)
        self.slider_contrast.setMinimum(10)
        self.slider_contrast.setMaximum(26)
        self.slider_contrast.setSliderPosition(18)
        self.slider_contrast.setOrientation(QtCore.Qt.Horizontal)
        self.slider_contrast.setObjectName("slider_contrast")
        self.horizontalLayout_6.addWidget(self.slider_contrast)
        self.verticalLayout_3.addLayout(self.horizontalLayout_6)
        spacerItem2 = QtWidgets.QSpacerItem(20, 40, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding)
        self.verticalLayout_3.addItem(spacerItem2)
        self.horizontalLayout_2.addWidget(self.groupBox)

        self.retranslateUi(SpectrogramOptions)
        QtCore.QMetaObject.connectSlotsByName(SpectrogramOptions)

    def retranslateUi(self, SpectrogramOptions):
        SpectrogramOptions.setWindowTitle(QtWidgets.QApplication.translate("SpectrogramOptions", "Form", None, -1))
        self.groupBox.setTitle(QtWidgets.QApplication.translate("SpectrogramOptions", "Spectrogram options", None, -1))
        self.cb_followSound.setText(QtWidgets.QApplication.translate("SpectrogramOptions", "follow sound", None, -1))
        self.label_2.setText(QtWidgets.QApplication.translate("SpectrogramOptions", "spectrogram type:", None, -1))
        self.cb_specType.setItemText(0, QtWidgets.QApplication.translate("SpectrogramOptions", "audible range", None, -1))
        self.cb_specType.setItemText(1, QtWidgets.QApplication.translate("SpectrogramOptions", "ultra sonic range", None, -1))
        self.label_8.setText(QtWidgets.QApplication.translate("SpectrogramOptions", "Color contrast", None, -1))

