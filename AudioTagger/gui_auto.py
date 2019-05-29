# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'gui.ui',
# licensing of 'gui.ui' applies.
#
# Created: Tue Feb 19 17:34:26 2019
#      by: pyside2-uic  running on PySide2 5.12.0
#
# WARNING! All changes made in this file will be lost!

from PySide2 import QtCore, QtGui, QtWidgets


class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(876, 584)
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.verticalLayout_2 = QtWidgets.QVBoxLayout(self.centralwidget)
        self.verticalLayout_2.setObjectName("verticalLayout_2")
        self.verticalLayout = QtWidgets.QVBoxLayout()
        self.verticalLayout.setObjectName("verticalLayout")
        self.horizontalLayout_2 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_2.setSizeConstraint(
            QtWidgets.QLayout.SetMinimumSize)
        self.horizontalLayout_2.setObjectName("horizontalLayout_2")
        self.gw_overview = QtWidgets.QGraphicsView(self.centralwidget)
        sizePolicy = QtWidgets.QSizePolicy(
            QtWidgets.QSizePolicy.Ignored, QtWidgets.QSizePolicy.Ignored)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(
            self.gw_overview.sizePolicy().hasHeightForWidth())
        self.gw_overview.setSizePolicy(sizePolicy)
        self.gw_overview.setObjectName("gw_overview")
        self.horizontalLayout_2.addWidget(self.gw_overview)
        self.verticalLayout.addLayout(self.horizontalLayout_2)
        self.horizontalLayout_3 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_3.setSizeConstraint(
            QtWidgets.QLayout.SetMinimumSize)
        self.horizontalLayout_3.setObjectName("horizontalLayout_3")
        self.scrollView = QtWidgets.QGraphicsView(self.centralwidget)
        sizePolicy = QtWidgets.QSizePolicy(
            QtWidgets.QSizePolicy.Ignored, QtWidgets.QSizePolicy.Maximum)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(
            self.scrollView.sizePolicy().hasHeightForWidth())
        self.scrollView.setSizePolicy(sizePolicy)
        self.scrollView.setObjectName("scrollView")
        self.horizontalLayout_3.addWidget(self.scrollView)
        self.verticalLayout.addLayout(self.horizontalLayout_3)
        self.horizontalLayout = QtWidgets.QHBoxLayout()
        self.horizontalLayout.setSizeConstraint(
            QtWidgets.QLayout.SetMinimumSize)
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.pb_prev = QtWidgets.QPushButton(self.centralwidget)
        self.pb_prev.setObjectName("pb_prev")
        self.horizontalLayout.addWidget(self.pb_prev)
        self.pb_next = QtWidgets.QPushButton(self.centralwidget)
        self.pb_next.setObjectName("pb_next")
        self.horizontalLayout.addWidget(self.pb_next)
        spacerItem = QtWidgets.QSpacerItem(
            40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout.addItem(spacerItem)
        self.pb_save = QtWidgets.QPushButton(self.centralwidget)
        self.pb_save.setObjectName("pb_save")
        self.horizontalLayout.addWidget(self.pb_save)
        self.pb_toggle = QtWidgets.QPushButton(self.centralwidget)
        self.pb_toggle.setObjectName("pb_toggle")
        self.horizontalLayout.addWidget(self.pb_toggle)
        self.pb_edit = QtWidgets.QPushButton(self.centralwidget)
        self.pb_edit.setObjectName("pb_edit")
        self.horizontalLayout.addWidget(self.pb_edit)
        self.pb_debug = QtWidgets.QPushButton(self.centralwidget)
        self.pb_debug.setObjectName("pb_debug")
        self.horizontalLayout.addWidget(self.pb_debug)
        spacerItem1 = QtWidgets.QSpacerItem(
            40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout.addItem(spacerItem1)
        self.cb_create = QtWidgets.QCheckBox(self.centralwidget)
        self.cb_create.setChecked(True)
        self.cb_create.setObjectName("cb_create")
        self.horizontalLayout.addWidget(self.cb_create)
        spacerItem2 = QtWidgets.QSpacerItem(
            40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout.addItem(spacerItem2)
        self.cb_labelType = QtWidgets.QComboBox(self.centralwidget)
        self.cb_labelType.setObjectName("cb_labelType")
        self.horizontalLayout.addWidget(self.cb_labelType)
        self.verticalLayout.addLayout(self.horizontalLayout)
        self.horizontalLayout_4 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_4.setSizeConstraint(
            QtWidgets.QLayout.SetMinimumSize)
        self.horizontalLayout_4.setObjectName("horizontalLayout_4")
        self.lbl_audio = QtWidgets.QLabel(self.centralwidget)
        sizePolicy = QtWidgets.QSizePolicy(
            QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(
            self.lbl_audio.sizePolicy().hasHeightForWidth())
        self.lbl_audio.setSizePolicy(sizePolicy)
        self.lbl_audio.setAlignment(
            QtCore.Qt.AlignRight | QtCore.Qt.AlignTrailing | QtCore.Qt.AlignVCenter)
        self.lbl_audio.setObjectName("lbl_audio")
        self.horizontalLayout_4.addWidget(self.lbl_audio)
        self.pb_play = QtWidgets.QPushButton(self.centralwidget)
        sizePolicy = QtWidgets.QSizePolicy(
            QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(
            self.pb_play.sizePolicy().hasHeightForWidth())
        self.pb_play.setSizePolicy(sizePolicy)
        self.pb_play.setObjectName("pb_play")
        self.horizontalLayout_4.addWidget(self.pb_play)
        self.pb_stop = QtWidgets.QPushButton(self.centralwidget)
        sizePolicy = QtWidgets.QSizePolicy(
            QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(
            self.pb_stop.sizePolicy().hasHeightForWidth())
        self.pb_stop.setSizePolicy(sizePolicy)
        self.pb_stop.setObjectName("pb_stop")
        self.horizontalLayout_4.addWidget(self.pb_stop)
        self.pb_seek = QtWidgets.QPushButton(self.centralwidget)
        self.pb_seek.setObjectName("pb_seek")
        self.horizontalLayout_4.addWidget(self.pb_seek)
        spacerItem3 = QtWidgets.QSpacerItem(
            40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout_4.addItem(spacerItem3)
        self.lbl_audio_position = QtWidgets.QLabel(self.centralwidget)
        sizePolicy = QtWidgets.QSizePolicy(
            QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(
            self.lbl_audio_position.sizePolicy().hasHeightForWidth())
        self.lbl_audio_position.setSizePolicy(sizePolicy)
        self.lbl_audio_position.setAlignment(
            QtCore.Qt.AlignRight | QtCore.Qt.AlignTrailing | QtCore.Qt.AlignVCenter)
        self.lbl_audio_position.setObjectName("lbl_audio_position")
        self.horizontalLayout_4.addWidget(self.lbl_audio_position)
        spacerItem4 = QtWidgets.QSpacerItem(
            40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout_4.addItem(spacerItem4)
        self.cb_followSound = QtWidgets.QCheckBox(self.centralwidget)
        self.cb_followSound.setObjectName("cb_followSound")
        self.horizontalLayout_4.addWidget(self.cb_followSound)
        spacerItem5 = QtWidgets.QSpacerItem(
            40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout_4.addItem(spacerItem5)
        self.lbl_zoom = QtWidgets.QLabel(self.centralwidget)
        sizePolicy = QtWidgets.QSizePolicy(
            QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(
            self.lbl_zoom.sizePolicy().hasHeightForWidth())
        self.lbl_zoom.setSizePolicy(sizePolicy)
        self.lbl_zoom.setObjectName("lbl_zoom")
        self.horizontalLayout_4.addWidget(self.lbl_zoom)
        spacerItem6 = QtWidgets.QSpacerItem(
            40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout_4.addItem(spacerItem6)
        self.label = QtWidgets.QLabel(self.centralwidget)
        self.label.setAlignment(
            QtCore.Qt.AlignRight | QtCore.Qt.AlignTrailing | QtCore.Qt.AlignVCenter)
        self.label.setObjectName("label")
        self.horizontalLayout_4.addWidget(self.label)
        self.cb_playbackSpeed = QtWidgets.QComboBox(self.centralwidget)
        self.cb_playbackSpeed.setObjectName("cb_playbackSpeed")
        self.horizontalLayout_4.addWidget(self.cb_playbackSpeed)
        spacerItem7 = QtWidgets.QSpacerItem(
            40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout_4.addItem(spacerItem7)
        self.label_2 = QtWidgets.QLabel(self.centralwidget)
        self.label_2.setAlignment(
            QtCore.Qt.AlignRight | QtCore.Qt.AlignTrailing | QtCore.Qt.AlignVCenter)
        self.label_2.setObjectName("label_2")
        self.horizontalLayout_4.addWidget(self.label_2)
        self.cb_specType = QtWidgets.QComboBox(self.centralwidget)
        self.cb_specType.setObjectName("cb_specType")
        self.cb_specType.addItem("")
        self.cb_specType.addItem("")
        self.horizontalLayout_4.addWidget(self.cb_specType)
        self.verticalLayout.addLayout(self.horizontalLayout_4)
        self.horizontalLayout_6 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_6.setObjectName("horizontalLayout_6")
        self.cb_file = QtWidgets.QComboBox(self.centralwidget)
        sizePolicy = QtWidgets.QSizePolicy(
            QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(
            self.cb_file.sizePolicy().hasHeightForWidth())
        self.cb_file.setSizePolicy(sizePolicy)
        self.cb_file.setObjectName("cb_file")
        self.horizontalLayout_6.addWidget(self.cb_file)
        self.verticalLayout.addLayout(self.horizontalLayout_6)
        self.verticalLayout_2.addLayout(self.verticalLayout)
        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 876, 21))
        self.menubar.setObjectName("menubar")
        self.menuFile = QtWidgets.QMenu(self.menubar)
        self.menuFile.setObjectName("menuFile")
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QtWidgets.QStatusBar(MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)
        self.actionOpen_folder = QtWidgets.QAction(MainWindow)
        self.actionOpen_folder.setObjectName("actionOpen_folder")
        self.actionClass_settings = QtWidgets.QAction(MainWindow)
        self.actionClass_settings.setObjectName("actionClass_settings")
        self.actionExport_settings = QtWidgets.QAction(MainWindow)
        self.actionExport_settings.setObjectName("actionExport_settings")
        self.actionImport_settings = QtWidgets.QAction(MainWindow)
        self.actionImport_settings.setObjectName("actionImport_settings")
        self.menuFile.addAction(self.actionOpen_folder)
        self.menuFile.addSeparator()
        self.menuFile.addAction(self.actionClass_settings)
        self.menuFile.addAction(self.actionExport_settings)
        self.menuFile.addAction(self.actionImport_settings)
        self.menubar.addAction(self.menuFile.menuAction())

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        MainWindow.setWindowTitle(QtWidgets.QApplication.translate(
            "MainWindow", "MainWindow", None, -1))
        self.pb_prev.setText(QtWidgets.QApplication.translate(
            "MainWindow", "show previous audio file", None, -1))
        self.pb_next.setText(QtWidgets.QApplication.translate(
            "MainWindow", "show next audio file", None, -1))
        self.pb_save.setText(QtWidgets.QApplication.translate(
            "MainWindow", "save", None, -1))
        self.pb_toggle.setText(QtWidgets.QApplication.translate(
            "MainWindow", "toggle", None, -1))
        self.pb_edit.setText(QtWidgets.QApplication.translate(
            "MainWindow", "edit", None, -1))
        self.pb_debug.setText(QtWidgets.QApplication.translate(
            "MainWindow", "debug", None, -1))
        self.cb_create.setText(QtWidgets.QApplication.translate(
            "MainWindow", "create", None, -1))
        self.lbl_audio.setText(QtWidgets.QApplication.translate(
            "MainWindow", "audio: ", None, -1))
        self.pb_play.setText(QtWidgets.QApplication.translate(
            "MainWindow", "play", None, -1))
        self.pb_stop.setText(QtWidgets.QApplication.translate(
            "MainWindow", "stop", None, -1))
        self.pb_seek.setText(QtWidgets.QApplication.translate(
            "MainWindow", "seek", None, -1))
        self.lbl_audio_position.setText(
            QtWidgets.QApplication.translate("MainWindow", "position:", None, -1))
        self.cb_followSound.setText(QtWidgets.QApplication.translate(
            "MainWindow", "follow sound", None, -1))
        self.lbl_zoom.setText(QtWidgets.QApplication.translate(
            "MainWindow", " Vertical zoom: 1x", None, -1))
        self.label.setText(QtWidgets.QApplication.translate(
            "MainWindow", "playback speed:", None, -1))
        self.label_2.setText(QtWidgets.QApplication.translate(
            "MainWindow", "spectrogram type:", None, -1))
        self.cb_specType.setItemText(0, QtWidgets.QApplication.translate(
            "MainWindow", "audible range", None, -1))
        self.cb_specType.setItemText(1, QtWidgets.QApplication.translate(
            "MainWindow", "ultra sonic range", None, -1))
        self.menuFile.setTitle(QtWidgets.QApplication.translate(
            "MainWindow", "File", None, -1))
        self.actionOpen_folder.setText(QtWidgets.QApplication.translate(
            "MainWindow", "Open folder", None, -1))
        self.actionClass_settings.setText(QtWidgets.QApplication.translate(
            "MainWindow", "Class settings", None, -1))
        self.actionExport_settings.setText(QtWidgets.QApplication.translate(
            "MainWindow", "export settings", None, -1))
        self.actionImport_settings.setText(QtWidgets.QApplication.translate(
            "MainWindow", "import settings", None, -1))
