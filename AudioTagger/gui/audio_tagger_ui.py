# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'audio_tagger.ui'
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

from pysoundplayer.gui.QSoundPlayer import QSoundPlayer
from AudioTagger.spectrogram_options import SpectrogramOptions

import resources_rc

class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        if MainWindow.objectName():
            MainWindow.setObjectName(u"MainWindow")
        MainWindow.resize(1152, 660)
        self.actionOpen_folder = QAction(MainWindow)
        self.actionOpen_folder.setObjectName(u"actionOpen_folder")
        self.actionClass_settings = QAction(MainWindow)
        self.actionClass_settings.setObjectName(u"actionClass_settings")
        self.actionExport_settings = QAction(MainWindow)
        self.actionExport_settings.setObjectName(u"actionExport_settings")
        self.actionImport_settings = QAction(MainWindow)
        self.actionImport_settings.setObjectName(u"actionImport_settings")
        self.action_split_files = QAction(MainWindow)
        self.action_split_files.setObjectName(u"action_split_files")
        self.action_shortcut_list = QAction(MainWindow)
        self.action_shortcut_list.setObjectName(u"action_shortcut_list")
        self.centralwidget = QWidget(MainWindow)
        self.centralwidget.setObjectName(u"centralwidget")
        self.verticalLayout_2 = QVBoxLayout(self.centralwidget)
        self.verticalLayout_2.setObjectName(u"verticalLayout_2")
        self.frame_1 = QFrame(self.centralwidget)
        self.frame_1.setObjectName(u"frame_1")
        sizePolicy = QSizePolicy(QSizePolicy.Expanding, QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.frame_1.sizePolicy().hasHeightForWidth())
        self.frame_1.setSizePolicy(sizePolicy)
        self.frame_1.setFrameShape(QFrame.NoFrame)
        self.frame_1.setFrameShadow(QFrame.Plain)
        self.horizontalLayout_7 = QHBoxLayout(self.frame_1)
        self.horizontalLayout_7.setSpacing(0)
        self.horizontalLayout_7.setObjectName(u"horizontalLayout_7")
        self.horizontalLayout_7.setContentsMargins(0, 0, 0, 0)
        self.splitter = QSplitter(self.frame_1)
        self.splitter.setObjectName(u"splitter")
        sizePolicy.setHeightForWidth(self.splitter.sizePolicy().hasHeightForWidth())
        self.splitter.setSizePolicy(sizePolicy)
        self.splitter.setOrientation(Qt.Horizontal)
        self.file_frame = QFrame(self.splitter)
        self.file_frame.setObjectName(u"file_frame")
        sizePolicy.setHeightForWidth(self.file_frame.sizePolicy().hasHeightForWidth())
        self.file_frame.setSizePolicy(sizePolicy)
        self.verticalLayout_5 = QVBoxLayout(self.file_frame)
        self.verticalLayout_5.setObjectName(u"verticalLayout_5")
        self.verticalLayout_5.setContentsMargins(0, 0, 0, 0)
        self.horizontalLayout_5 = QHBoxLayout()
        self.horizontalLayout_5.setSpacing(0)
        self.horizontalLayout_5.setObjectName(u"horizontalLayout_5")
        self.horizontalSpacer_9 = QSpacerItem(40, 10, QSizePolicy.Expanding, QSizePolicy.Minimum)

        self.horizontalLayout_5.addItem(self.horizontalSpacer_9)

        self.pb_prev = QPushButton(self.file_frame)
        self.pb_prev.setObjectName(u"pb_prev")
        icon = QIcon()
        icon.addFile(u":/icons/left", QSize(), QIcon.Normal, QIcon.Off)
        self.pb_prev.setIcon(icon)
        self.pb_prev.setIconSize(QSize(10, 10))
        self.pb_prev.setFlat(True)

        self.horizontalLayout_5.addWidget(self.pb_prev)

        self.pb_next = QPushButton(self.file_frame)
        self.pb_next.setObjectName(u"pb_next")
        icon1 = QIcon()
        icon1.addFile(u":/icons/right", QSize(), QIcon.Normal, QIcon.Off)
        self.pb_next.setIcon(icon1)
        self.pb_next.setIconSize(QSize(10, 10))
        self.pb_next.setFlat(True)

        self.horizontalLayout_5.addWidget(self.pb_next)


        self.verticalLayout_5.addLayout(self.horizontalLayout_5)

        self.file_tree = QTreeWidget(self.file_frame)
        __qtreewidgetitem = QTreeWidgetItem()
        __qtreewidgetitem.setText(0, u"1");
        self.file_tree.setHeaderItem(__qtreewidgetitem)
        self.file_tree.setObjectName(u"file_tree")
        sizePolicy1 = QSizePolicy(QSizePolicy.Preferred, QSizePolicy.Expanding)
        sizePolicy1.setHorizontalStretch(0)
        sizePolicy1.setVerticalStretch(0)
        sizePolicy1.setHeightForWidth(self.file_tree.sizePolicy().hasHeightForWidth())
        self.file_tree.setSizePolicy(sizePolicy1)
        self.file_tree.setMinimumSize(QSize(250, 0))
        self.file_tree.setSizeAdjustPolicy(QAbstractScrollArea.AdjustToContents)
        self.file_tree.setUniformRowHeights(True)
        self.file_tree.setSortingEnabled(True)
        self.file_tree.header().setVisible(True)

        self.verticalLayout_5.addWidget(self.file_tree)

        self.splitter.addWidget(self.file_frame)
        self.spectro_frame = QFrame(self.splitter)
        self.spectro_frame.setObjectName(u"spectro_frame")
        sizePolicy2 = QSizePolicy(QSizePolicy.Preferred, QSizePolicy.Preferred)
        sizePolicy2.setHorizontalStretch(0)
        sizePolicy2.setVerticalStretch(0)
        sizePolicy2.setHeightForWidth(self.spectro_frame.sizePolicy().hasHeightForWidth())
        self.spectro_frame.setSizePolicy(sizePolicy2)
        self.spectro_frame.setFrameShape(QFrame.StyledPanel)
        self.spectro_frame.setFrameShadow(QFrame.Raised)
        self.verticalLayout_7 = QVBoxLayout(self.spectro_frame)
        self.verticalLayout_7.setObjectName(u"verticalLayout_7")
        self.horizontalLayout_2 = QHBoxLayout()
        self.horizontalLayout_2.setObjectName(u"horizontalLayout_2")
        self.horizontalLayout_2.setSizeConstraint(QLayout.SetMinimumSize)
        self.gw_overview = QGraphicsView(self.spectro_frame)
        self.gw_overview.setObjectName(u"gw_overview")
        sizePolicy3 = QSizePolicy(QSizePolicy.Preferred, QSizePolicy.Maximum)
        sizePolicy3.setHorizontalStretch(0)
        sizePolicy3.setVerticalStretch(0)
        sizePolicy3.setHeightForWidth(self.gw_overview.sizePolicy().hasHeightForWidth())
        self.gw_overview.setSizePolicy(sizePolicy3)

        self.horizontalLayout_2.addWidget(self.gw_overview)


        self.verticalLayout_7.addLayout(self.horizontalLayout_2)

        self.horizontalLayout_3 = QHBoxLayout()
        self.horizontalLayout_3.setObjectName(u"horizontalLayout_3")
        self.scrollView = QGraphicsView(self.spectro_frame)
        self.scrollView.setObjectName(u"scrollView")
        sizePolicy1.setHeightForWidth(self.scrollView.sizePolicy().hasHeightForWidth())
        self.scrollView.setSizePolicy(sizePolicy1)

        self.horizontalLayout_3.addWidget(self.scrollView)


        self.verticalLayout_7.addLayout(self.horizontalLayout_3)

        self.frame = QFrame(self.spectro_frame)
        self.frame.setObjectName(u"frame")
        sizePolicy3.setHeightForWidth(self.frame.sizePolicy().hasHeightForWidth())
        self.frame.setSizePolicy(sizePolicy3)
        self.verticalLayout = QVBoxLayout(self.frame)
        self.verticalLayout.setSpacing(0)
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.verticalLayout.setContentsMargins(0, 0, 0, 0)
        self.horizontalLayout_12 = QHBoxLayout()
        self.horizontalLayout_12.setObjectName(u"horizontalLayout_12")
        self.horizontalLayout_12.setSizeConstraint(QLayout.SetFixedSize)
        self.sound_player = QSoundPlayer(self.frame)
        self.sound_player.setObjectName(u"sound_player")

        self.horizontalLayout_12.addWidget(self.sound_player)


        self.verticalLayout.addLayout(self.horizontalLayout_12)


        self.verticalLayout_7.addWidget(self.frame)

        self.splitter.addWidget(self.spectro_frame)

        self.horizontalLayout_7.addWidget(self.splitter)


        self.verticalLayout_2.addWidget(self.frame_1)

        self.frame_2 = QFrame(self.centralwidget)
        self.frame_2.setObjectName(u"frame_2")
        sizePolicy4 = QSizePolicy(QSizePolicy.Preferred, QSizePolicy.Fixed)
        sizePolicy4.setHorizontalStretch(0)
        sizePolicy4.setVerticalStretch(0)
        sizePolicy4.setHeightForWidth(self.frame_2.sizePolicy().hasHeightForWidth())
        self.frame_2.setSizePolicy(sizePolicy4)
        self.frame_2.setFrameShape(QFrame.StyledPanel)
        self.frame_2.setFrameShadow(QFrame.Raised)
        self.gridLayout = QGridLayout(self.frame_2)
        self.gridLayout.setObjectName(u"gridLayout")
        self.gridLayout.setVerticalSpacing(0)
        self.groupBox_2 = QGroupBox(self.frame_2)
        self.groupBox_2.setObjectName(u"groupBox_2")
        sizePolicy5 = QSizePolicy(QSizePolicy.Maximum, QSizePolicy.Preferred)
        sizePolicy5.setHorizontalStretch(2)
        sizePolicy5.setVerticalStretch(0)
        sizePolicy5.setHeightForWidth(self.groupBox_2.sizePolicy().hasHeightForWidth())
        self.groupBox_2.setSizePolicy(sizePolicy5)
        self.verticalLayout_4 = QVBoxLayout(self.groupBox_2)
        self.verticalLayout_4.setObjectName(u"verticalLayout_4")
        self.verticalLayout_4.setContentsMargins(0, -1, -1, -1)
        self.horizontalLayout_13 = QHBoxLayout()
        self.horizontalLayout_13.setObjectName(u"horizontalLayout_13")
        self.lbl_spec_create = QLabel(self.groupBox_2)
        self.lbl_spec_create.setObjectName(u"lbl_spec_create")

        self.horizontalLayout_13.addWidget(self.lbl_spec_create)

        self.pb_toggle_create = QPushButton(self.groupBox_2)
        self.pb_toggle_create.setObjectName(u"pb_toggle_create")
        sizePolicy6 = QSizePolicy(QSizePolicy.Maximum, QSizePolicy.Fixed)
        sizePolicy6.setHorizontalStretch(0)
        sizePolicy6.setVerticalStretch(0)
        sizePolicy6.setHeightForWidth(self.pb_toggle_create.sizePolicy().hasHeightForWidth())
        self.pb_toggle_create.setSizePolicy(sizePolicy6)
        icon2 = QIcon()
        icon2.addFile(u":/icons/toggle-off", QSize(), QIcon.Normal, QIcon.Off)
        icon2.addFile(u":/icons/toggle-off", QSize(), QIcon.Active, QIcon.Off)
        icon2.addFile(u":/icons/toggle-on", QSize(), QIcon.Active, QIcon.On)
        self.pb_toggle_create.setIcon(icon2)
        self.pb_toggle_create.setIconSize(QSize(20, 20))
        self.pb_toggle_create.setCheckable(True)
        self.pb_toggle_create.setFlat(True)

        self.horizontalLayout_13.addWidget(self.pb_toggle_create)

        self.lbl_spec_modify = QLabel(self.groupBox_2)
        self.lbl_spec_modify.setObjectName(u"lbl_spec_modify")

        self.horizontalLayout_13.addWidget(self.lbl_spec_modify)

        self.horizontalSpacer_10 = QSpacerItem(40, 20, QSizePolicy.Maximum, QSizePolicy.Minimum)

        self.horizontalLayout_13.addItem(self.horizontalSpacer_10)

        self.pb_first_tag = QPushButton(self.groupBox_2)
        self.pb_first_tag.setObjectName(u"pb_first_tag")
        icon3 = QIcon()
        icon3.addFile(u":/icons/first", QSize(), QIcon.Normal, QIcon.Off)
        self.pb_first_tag.setIcon(icon3)
        self.pb_first_tag.setIconSize(QSize(20, 20))
        self.pb_first_tag.setFlat(True)

        self.horizontalLayout_13.addWidget(self.pb_first_tag)

        self.pb_previous_tag = QPushButton(self.groupBox_2)
        self.pb_previous_tag.setObjectName(u"pb_previous_tag")
        icon4 = QIcon()
        icon4.addFile(u":/icons/backward", QSize(), QIcon.Normal, QIcon.Off)
        self.pb_previous_tag.setIcon(icon4)
        self.pb_previous_tag.setIconSize(QSize(20, 20))
        self.pb_previous_tag.setFlat(True)

        self.horizontalLayout_13.addWidget(self.pb_previous_tag)

        self.pb_next_tag = QPushButton(self.groupBox_2)
        self.pb_next_tag.setObjectName(u"pb_next_tag")
        icon5 = QIcon()
        icon5.addFile(u":/icons/forward", QSize(), QIcon.Normal, QIcon.Off)
        self.pb_next_tag.setIcon(icon5)
        self.pb_next_tag.setIconSize(QSize(20, 20))
        self.pb_next_tag.setFlat(True)

        self.horizontalLayout_13.addWidget(self.pb_next_tag)

        self.pb_last_tag = QPushButton(self.groupBox_2)
        self.pb_last_tag.setObjectName(u"pb_last_tag")
        icon6 = QIcon()
        icon6.addFile(u":/icons/last", QSize(), QIcon.Normal, QIcon.Off)
        self.pb_last_tag.setIcon(icon6)
        self.pb_last_tag.setIconSize(QSize(20, 20))
        self.pb_last_tag.setFlat(True)

        self.horizontalLayout_13.addWidget(self.pb_last_tag)

        self.horizontalSpacer_11 = QSpacerItem(40, 20, QSizePolicy.Maximum, QSizePolicy.Minimum)

        self.horizontalLayout_13.addItem(self.horizontalSpacer_11)

        self.pb_save = QPushButton(self.groupBox_2)
        self.pb_save.setObjectName(u"pb_save")
        icon7 = QIcon()
        icon7.addFile(u":/icons/save", QSize(), QIcon.Normal, QIcon.Off)
        self.pb_save.setIcon(icon7)
        self.pb_save.setIconSize(QSize(20, 20))
        self.pb_save.setFlat(True)

        self.horizontalLayout_13.addWidget(self.pb_save)

        self.horizontalSpacer_6 = QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)

        self.horizontalLayout_13.addItem(self.horizontalSpacer_6)


        self.verticalLayout_4.addLayout(self.horizontalLayout_13)

        self.horizontalLayout_16 = QHBoxLayout()
        self.horizontalLayout_16.setObjectName(u"horizontalLayout_16")
        self.label_9 = QLabel(self.groupBox_2)
        self.label_9.setObjectName(u"label_9")
        sizePolicy7 = QSizePolicy(QSizePolicy.Maximum, QSizePolicy.Preferred)
        sizePolicy7.setHorizontalStretch(0)
        sizePolicy7.setVerticalStretch(0)
        sizePolicy7.setHeightForWidth(self.label_9.sizePolicy().hasHeightForWidth())
        self.label_9.setSizePolicy(sizePolicy7)

        self.horizontalLayout_16.addWidget(self.label_9)

        self.cb_labelType = QComboBox(self.groupBox_2)
        self.cb_labelType.setObjectName(u"cb_labelType")

        self.horizontalLayout_16.addWidget(self.cb_labelType)

        self.label = QLabel(self.groupBox_2)
        self.label.setObjectName(u"label")

        self.horizontalLayout_16.addWidget(self.label)

        self.pb_background = QPushButton(self.groupBox_2)
        self.pb_background.setObjectName(u"pb_background")
        icon8 = QIcon()
        icon8.addFile(u":/icons/toggle-off", QSize(), QIcon.Normal, QIcon.Off)
        icon8.addFile(u":/icons/toggle-on", QSize(), QIcon.Active, QIcon.On)
        self.pb_background.setIcon(icon8)
        self.pb_background.setIconSize(QSize(20, 20))
        self.pb_background.setCheckable(True)
        self.pb_background.setFlat(True)

        self.horizontalLayout_16.addWidget(self.pb_background)

        self.horizontalSpacer_2 = QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)

        self.horizontalLayout_16.addItem(self.horizontalSpacer_2)


        self.verticalLayout_4.addLayout(self.horizontalLayout_16)

        self.horizontalLayout = QHBoxLayout()
        self.horizontalLayout.setObjectName(u"horizontalLayout")
        self.label_2 = QLabel(self.groupBox_2)
        self.label_2.setObjectName(u"label_2")

        self.horizontalLayout.addWidget(self.label_2)

        self.checkbox_wind = QCheckBox(self.groupBox_2)
        self.checkbox_wind.setObjectName(u"checkbox_wind")

        self.horizontalLayout.addWidget(self.checkbox_wind)

        self.checkbox_rain = QCheckBox(self.groupBox_2)
        self.checkbox_rain.setObjectName(u"checkbox_rain")

        self.horizontalLayout.addWidget(self.checkbox_rain)

        self.horizontalSpacer = QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)

        self.horizontalLayout.addItem(self.horizontalSpacer)


        self.verticalLayout_4.addLayout(self.horizontalLayout)

        self.horizontalLayout_4 = QHBoxLayout()
        self.horizontalLayout_4.setObjectName(u"horizontalLayout_4")
        self.label_7 = QLabel(self.groupBox_2)
        self.label_7.setObjectName(u"label_7")

        self.horizontalLayout_4.addWidget(self.label_7)

        self.btn_done = QPushButton(self.groupBox_2)
        self.btn_done.setObjectName(u"btn_done")
        self.btn_done.setIcon(icon8)
        self.btn_done.setIconSize(QSize(20, 20))
        self.btn_done.setCheckable(True)
        self.btn_done.setFlat(True)

        self.horizontalLayout_4.addWidget(self.btn_done)

        self.horizontalSpacer_7 = QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)

        self.horizontalLayout_4.addItem(self.horizontalSpacer_7)


        self.verticalLayout_4.addLayout(self.horizontalLayout_4)

        self.verticalSpacer_2 = QSpacerItem(20, 40, QSizePolicy.Minimum, QSizePolicy.Expanding)

        self.verticalLayout_4.addItem(self.verticalSpacer_2)


        self.gridLayout.addWidget(self.groupBox_2, 0, 1, 1, 1)

        self.info_viewer = QTextEdit(self.frame_2)
        self.info_viewer.setObjectName(u"info_viewer")
        sizePolicy8 = QSizePolicy(QSizePolicy.Minimum, QSizePolicy.Preferred)
        sizePolicy8.setHorizontalStretch(3)
        sizePolicy8.setVerticalStretch(0)
        sizePolicy8.setHeightForWidth(self.info_viewer.sizePolicy().hasHeightForWidth())
        self.info_viewer.setSizePolicy(sizePolicy8)
        self.info_viewer.setMaximumSize(QSize(16777215, 150))

        self.gridLayout.addWidget(self.info_viewer, 0, 2, 1, 1)

        self.spectrogram_options = SpectrogramOptions(self.frame_2)
        self.spectrogram_options.setObjectName(u"spectrogram_options")
        sizePolicy5.setHeightForWidth(self.spectrogram_options.sizePolicy().hasHeightForWidth())
        self.spectrogram_options.setSizePolicy(sizePolicy5)

        self.gridLayout.addWidget(self.spectrogram_options, 0, 0, 1, 1)


        self.verticalLayout_2.addWidget(self.frame_2)

        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QMenuBar(MainWindow)
        self.menubar.setObjectName(u"menubar")
        self.menubar.setGeometry(QRect(0, 0, 1152, 23))
        self.menuFile = QMenu(self.menubar)
        self.menuFile.setObjectName(u"menuFile")
        self.menuHelp = QMenu(self.menubar)
        self.menuHelp.setObjectName(u"menuHelp")
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QStatusBar(MainWindow)
        self.statusbar.setObjectName(u"statusbar")
        MainWindow.setStatusBar(self.statusbar)
        self.toolBar = QToolBar(MainWindow)
        self.toolBar.setObjectName(u"toolBar")
        MainWindow.addToolBar(Qt.TopToolBarArea, self.toolBar)

        self.menubar.addAction(self.menuFile.menuAction())
        self.menubar.addAction(self.menuHelp.menuAction())
        self.menuFile.addAction(self.actionOpen_folder)
        self.menuFile.addSeparator()
        self.menuFile.addAction(self.actionClass_settings)
        self.menuFile.addAction(self.actionExport_settings)
        self.menuFile.addAction(self.actionImport_settings)
        self.menuFile.addAction(self.action_split_files)
        self.menuHelp.addAction(self.action_shortcut_list)
        self.toolBar.addAction(self.actionOpen_folder)
        self.toolBar.addAction(self.actionClass_settings)

        self.retranslateUi(MainWindow)

        QMetaObject.connectSlotsByName(MainWindow)
    # setupUi

    def retranslateUi(self, MainWindow):
        MainWindow.setWindowTitle(QCoreApplication.translate("MainWindow", u"MainWindow", None))
        self.actionOpen_folder.setText(QCoreApplication.translate("MainWindow", u"Open folder", None))
        self.actionClass_settings.setText(QCoreApplication.translate("MainWindow", u"Class settings", None))
        self.actionExport_settings.setText(QCoreApplication.translate("MainWindow", u"Export settings", None))
        self.actionImport_settings.setText(QCoreApplication.translate("MainWindow", u"Import settings", None))
        self.action_split_files.setText(QCoreApplication.translate("MainWindow", u"Split files", None))
        self.action_shortcut_list.setText(QCoreApplication.translate("MainWindow", u"Shortcut list", None))
#if QT_CONFIG(tooltip)
        self.pb_prev.setToolTip(QCoreApplication.translate("MainWindow", u"Show previous audio file", None))
#endif // QT_CONFIG(tooltip)
        self.pb_prev.setText("")
#if QT_CONFIG(tooltip)
        self.pb_next.setToolTip(QCoreApplication.translate("MainWindow", u"Show next audio file", None))
#endif // QT_CONFIG(tooltip)
        self.pb_next.setText("")
        self.groupBox_2.setTitle(QCoreApplication.translate("MainWindow", u"Annotations", None))
        self.lbl_spec_create.setText(QCoreApplication.translate("MainWindow", u"Create", None))
        self.pb_toggle_create.setText("")
        self.lbl_spec_modify.setText(QCoreApplication.translate("MainWindow", u"Modify", None))
#if QT_CONFIG(tooltip)
        self.pb_first_tag.setToolTip(QCoreApplication.translate("MainWindow", u"Go to first annotation", None))
#endif // QT_CONFIG(tooltip)
        self.pb_first_tag.setText("")
#if QT_CONFIG(tooltip)
        self.pb_previous_tag.setToolTip(QCoreApplication.translate("MainWindow", u"Previous annotation", None))
#endif // QT_CONFIG(tooltip)
        self.pb_previous_tag.setText("")
#if QT_CONFIG(tooltip)
        self.pb_next_tag.setToolTip(QCoreApplication.translate("MainWindow", u"Next annotation", None))
#endif // QT_CONFIG(tooltip)
        self.pb_next_tag.setText("")
#if QT_CONFIG(tooltip)
        self.pb_last_tag.setToolTip(QCoreApplication.translate("MainWindow", u"Go to last annotation", None))
#endif // QT_CONFIG(tooltip)
        self.pb_last_tag.setText("")
#if QT_CONFIG(tooltip)
        self.pb_save.setToolTip(QCoreApplication.translate("MainWindow", u"Save", None))
#endif // QT_CONFIG(tooltip)
        self.pb_save.setText("")
        self.label_9.setText(QCoreApplication.translate("MainWindow", u"Active label:", None))
        self.label.setText(QCoreApplication.translate("MainWindow", u"In background:", None))
        self.pb_background.setText("")
        self.label_2.setText(QCoreApplication.translate("MainWindow", u"Background noise:", None))
        self.checkbox_wind.setText(QCoreApplication.translate("MainWindow", u"Wind", None))
        self.checkbox_rain.setText(QCoreApplication.translate("MainWindow", u"Rain", None))
        self.label_7.setText(QCoreApplication.translate("MainWindow", u"File Done:", None))
        self.btn_done.setText("")
        self.menuFile.setTitle(QCoreApplication.translate("MainWindow", u"File", None))
        self.menuHelp.setTitle(QCoreApplication.translate("MainWindow", u"Help", None))
        self.toolBar.setWindowTitle(QCoreApplication.translate("MainWindow", u"toolBar", None))
    # retranslateUi

