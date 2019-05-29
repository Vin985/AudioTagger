# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'gui.ui'
#
# Created: Wed Aug 20 16:40:42 2014
#      by: pyside-uic 0.2.15 running on PySide 1.2.1
#
# WARNING! All changes made in this file will be lost!

# from PySide import QtCore, QtWidgets


import os

from PySide2 import QtCore, QtSvg, QtWidgets


class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(876, 584)
        self.centralwidget = QtWidgets.QWidget(MainWindow)

        self.create_graphic_views()
        self.create_elements()
        self.create_layouts()
        self.fill_layouts()

        # MENU

        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = MainWindow.menuBar()  # QtWidgets.QMenuBar(MainWindow)
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

    def create_graphic_views(self):
        self.gw_overview = QtWidgets.QGraphicsView(self.centralwidget)
        sizePolicy = QtWidgets.QSizePolicy(
            QtWidgets.QSizePolicy.Ignored, QtWidgets.QSizePolicy.Ignored)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(
            self.gw_overview.sizePolicy().hasHeightForWidth())
        self.gw_overview.setSizePolicy(sizePolicy)
        self.gw_overview.setObjectName("gw_overview")

        self.scrollView = QtWidgets.QGraphicsView(self.centralwidget)
        sizePolicy = QtWidgets.QSizePolicy(
            QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Maximum)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(
            self.scrollView.sizePolicy().hasHeightForWidth())
        self.scrollView.setSizePolicy(sizePolicy)
        self.scrollView.setObjectName("scrollView")

    def create_elements(self):
        self.iconFolder = SVGButton.getIconFolder()

        self.pb_prev = SVGButton(self.centralwidget)
        self.pb_prev.load(self.iconFolder + '/fa-backward.svg')
        self.pb_prev.setToolTip("Load previous file")

        self.pb_next = SVGButton(self.centralwidget)
        self.pb_next.load(self.iconFolder + '/fa-forward.svg')
        self.pb_next.setToolTip("Load next file")

        self.pb_save = SVGButton(self.centralwidget)
        self.pb_save.load(self.iconFolder + '/fa-save.svg')
        self.pb_save.setToolTip("Save annotaions")

        self.pb_toggle = SVGButton(self.centralwidget)
        self.pb_toggle.load(self.iconFolder + '/fa-chevron-right.svg')
        self.pb_toggle.setToolTip("Toggle through annotaions")

        self.pb_toggle_back = SVGButton(self.centralwidget)
        self.pb_toggle_back.load(self.iconFolder + '/fa-chevron-left.svg')
        self.pb_toggle_back.setToolTip("Toggle backwards through annotaions")

        # self.pb_edit = QtWidgets.QPushButton(self.centralwidget)
        # self.pb_edit.setObjectName("pb_edit")

        self.pb_toggle_create = SVGButton(self.centralwidget)
        self.pb_toggle_create.load(self.iconFolder + '/fa-toggle-on.svg')
        self.pb_toggle_create.setToolTip("Click to modify annotations")

        self.lbl_spec_modify = QtWidgets.QLabel(self.centralwidget)
        self.lbl_spec_create = QtWidgets.QLabel(self.centralwidget)

        # self.cb_create = QtWidgets.QCheckBox(self.centralwidget)
        # self.cb_create.setChecked(True)
        # self.cb_create.setObjectName("cb_create")

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

        self.pb_play = SVGButton(self.centralwidget)
        self.pb_play.load(self.iconFolder + '/fa-play.svg')
        self.pb_play.setToolTip("Play sound")

        self.pb_stop = SVGButton(self.centralwidget)
        self.pb_stop.load(self.iconFolder + '/fa-stop.svg')
        self.pb_stop.setToolTip("Stop and reset sound")

        self.pb_seek = SVGButton(self.centralwidget)
        self.pb_seek.load(self.iconFolder + '/fa-map-signs.svg')
        self.pb_seek.setToolTip("Seek")

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
        self.lbl_audio_position.setVisible(False)

        self.lbl_followSound = QtWidgets.QLabel(self.centralwidget)
        self.cb_followSound = QtWidgets.QCheckBox(self.centralwidget)
        self.cb_followSound.setObjectName("cb_followSound")

        # self.lbl_zoom = QtWidgets.QLabel(self.centralwidget)
        # sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Fixed)
        # sizePolicy.setHorizontalStretch(0)
        # sizePolicy.setVerticalStretch(0)
        # sizePolicy.setHeightForWidth(self.lbl_zoom.sizePolicy().hasHeightForWidth())
        # self.lbl_zoom.setSizePolicy(sizePolicy)
        # self.lbl_zoom.setObjectName("lbl_zoom")

        self.lbl_playbackSpeed = QtWidgets.QLabel(self.centralwidget)
        self.cb_playbackSpeed = QtWidgets.QComboBox(self.centralwidget)
        self.cb_playbackSpeed.setObjectName("cb_playbackSpeed")

        self.lbl_specType = QtWidgets.QLabel(self.centralwidget)
        self.cb_specType = QtWidgets.QComboBox(self.centralwidget)
        self.cb_specType.setObjectName("cb_specType")
        self.cb_specType.addItem("")
        self.cb_specType.addItem("")

        self.lbl_labelType = QtWidgets.QLabel(self.centralwidget)
        self.cb_labelType = QtWidgets.QComboBox(self.centralwidget)
        self.cb_labelType.setObjectName("cb_labelType")

        self.cb_file = QtWidgets.QComboBox(self.centralwidget)
        sizePolicy = QtWidgets.QSizePolicy(
            QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(
            self.cb_file.sizePolicy().hasHeightForWidth())
        self.cb_file.setSizePolicy(sizePolicy)
        self.cb_file.setObjectName("cb_file")

        # self.info_viewer = QtWidgets.QLabel(self.centralwidget)
        # self.info_viewer = QtWidgets.QTextEdit(self.centralwidget)
        self.info_viewer = SmallEdit(self.centralwidget)

        # self.info_viewer.setMinimumSize(100, 10)
        # self.info_viewer.setFixedSize(100, 100)
        # self.info_viewer.setSizePolicy(QtWidgets.QSizePolicy.Ignored, QtWidgets.QSizePolicy.Ignored)

    def create_layouts(self):
        self.structure_layout = QtWidgets.QVBoxLayout(self.centralwidget)

        self.control_info_widget = QtWidgets.QWidget(self.centralwidget)
        self.control_info_splitter = QtWidgets.QHBoxLayout(
            self.control_info_widget)
        self.control_info_widget.setSizePolicy(
            QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Fixed)

        self.file_control_widget = QtWidgets.QWidget(self.centralwidget)
        self.file_control_layout = QtWidgets.QVBoxLayout(
            self.file_control_widget)
        self.file_control_layout.setContentsMargins(0, 0, 0, 0)
        self.file_control_widget.setSizePolicy(
            QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Fixed)

        self.sound_spec_widget = QtWidgets.QWidget(self.centralwidget)
        self.sound_spec_layout = QtWidgets.QHBoxLayout(self.sound_spec_widget)
        self.sound_spec_layout.setContentsMargins(0, 0, 0, 0)

        self.sound_parts_widget = QtWidgets.QWidget(self.centralwidget)
        self.sound_parts_layout = QtWidgets.QVBoxLayout(
            self.sound_parts_widget)
        self.sound_parts_layout.setSpacing(10)
        self.sound_parts_layout.setContentsMargins(0, 0, 0, 0)

        self.sound_settings_widget = QtWidgets.QWidget(self.centralwidget)
        self.sound_settings_layout = QtWidgets.QFormLayout(
            self.sound_settings_widget)
        self.sound_settings_layout.setContentsMargins(0, 0, 0, 0)

        self.spec_parts_widget = QtWidgets.QWidget(self.centralwidget)
        self.spec_parts_layout = QtWidgets.QVBoxLayout(self.spec_parts_widget)
        self.spec_parts_layout.setContentsMargins(0, 0, 0, 0)

        self.sound_controls_widget = QtWidgets.QWidget(self.centralwidget)
        self.sound_controls_layout = QtWidgets.QHBoxLayout(
            self.sound_controls_widget)
        self.sound_controls_layout.setSpacing(10)
        self.sound_controls_layout.setContentsMargins(0, 0, 0, 0)

        self.spec_interact_widget = QtWidgets.QWidget(self.centralwidget)
        self.spec_interact_layout = QtWidgets.QHBoxLayout(
            self.spec_interact_widget)
        self.spec_interact_layout.setSpacing(10)
        self.spec_interact_layout.setContentsMargins(0, 0, 0, 0)

        self.spec_settings_widget = QtWidgets.QWidget(self.centralwidget)
        self.spec_settings_layout = QtWidgets.QFormLayout(
            self.spec_settings_widget)
        self.spec_settings_layout.setSpacing(10)
        self.spec_settings_layout.setContentsMargins(0, 0, 0, 0)

        self.create_modify_widget = QtWidgets.QWidget(self.centralwidget)
        self.create_modify_layout = QtWidgets.QHBoxLayout(
            self.create_modify_widget)
        self.create_modify_layout.setSpacing(5)
        self.create_modify_layout.setContentsMargins(0, 0, 0, 0)

    def fill_layouts(self):
        self.structure_layout.addWidget(self.gw_overview)
        self.structure_layout.addWidget(self.scrollView)
        self.structure_layout.addWidget(self.control_info_widget)

        self.control_info_splitter.addWidget(self.file_control_widget)
        self.control_info_splitter.addWidget(self.info_viewer)

        self.file_control_layout.addWidget(self.sound_spec_widget)
        self.file_control_layout.addWidget(self.cb_file)

        self.sound_spec_layout.addWidget(self.sound_parts_widget)
        self.sound_spec_layout.addWidget(self.spec_parts_widget)

        self.sound_parts_layout.addWidget(self.sound_controls_widget)
        self.sound_parts_layout.addWidget(self.sound_settings_widget)

        self.sound_controls_layout.addStretch(0)
        self.sound_controls_layout.addWidget(self.pb_prev)
        self.sound_controls_layout.addWidget(self.pb_stop)
        self.sound_controls_layout.addWidget(self.pb_play)
        self.sound_controls_layout.addWidget(self.pb_next)
        self.sound_controls_layout.addSpacing(15)
        self.sound_controls_layout.addWidget(self.pb_seek)
        self.sound_controls_layout.addStretch(0)

        self.sound_settings_layout.addRow(
            self.lbl_followSound, self.cb_followSound)
        self.sound_settings_layout.addRow(
            self.lbl_playbackSpeed, self.cb_playbackSpeed)

        self.spec_parts_layout.addWidget(self.spec_interact_widget)
        self.spec_parts_layout.addWidget(self.spec_settings_widget)

        self.spec_interact_layout.addStretch(0)
        # self.spec_interact_layout.addWidget(self.cb_create)
        self.spec_interact_layout.addWidget(self.create_modify_widget)
        self.spec_interact_layout.addWidget(self.pb_toggle_back)
        self.spec_interact_layout.addWidget(self.pb_toggle)
        self.spec_interact_layout.addWidget(self.pb_save)
        self.spec_interact_layout.addStretch(0)

        self.spec_settings_layout.addRow(self.lbl_labelType, self.cb_labelType)
        self.spec_settings_layout.addRow(self.lbl_specType, self.cb_specType)

        self.create_modify_layout.addWidget(self.lbl_spec_modify)
        self.create_modify_layout.addWidget(self.pb_toggle_create)
        self.create_modify_layout.addWidget(self.lbl_spec_create)

        self.centralwidget.setLayout(self.structure_layout)

    def retranslateUi(self, MainWindow):
        MainWindow.setWindowTitle(QtWidgets.QApplication.translate("MainWindow",
                                                                   "MainWindow", None))
        # self.pb_prev.setText(QtWidgets.QApplication.translate("MainWindow", "show previous audio file", None))
        # self.pb_next.setText(QtWidgets.QApplication.translate("MainWindow", "show next audio file", None))
        # self.pb_save.setText(QtWidgets.QApplication.translate("MainWindow", "save", None))
        # self.pb_toggle.setText(QtWidgets.QApplication.translate("MainWindow", "toggle", None))
        # self.pb_edit.setText(QtWidgets.QApplication.translate("MainWindow", "edit", None))
        # self.pb_debug.setText(QtWidgets.QApplication.translate("MainWindow", "debug", None))
        # self.cb_create.setText(QtWidgets.QApplication.translate("MainWindow", "create", None))
        # self.lbl_audio.setText(QtWidgets.QApplication.translate("MainWindow", "audio: ", None))
        # self.pb_play.setText(QtWidgets.QApplication.translate("MainWindow", "play", None))
        # self.pb_stop.setText(QtWidgets.QApplication.translate("MainWindow", "stop", None))
        # self.pb_seek.setText(QtWidgets.QApplication.translate("MainWindow", "seek", None))
        # self.lbl_audio_position.setText(QtWidgets.QApplication.translate("MainWindow", "position:", None))
        self.lbl_followSound.setText(QtWidgets.QApplication.translate(
            "MainWindow", "follow sound", None))
        # self.lbl_zoom.setText(QtWidgets.QApplication.translate("MainWindow", " Vertical zoom: 1x", None))
        self.lbl_playbackSpeed.setText(QtWidgets.QApplication.translate(
            "MainWindow", "playback speed:", None))
        self.lbl_specType.setText(QtWidgets.QApplication.translate(
            "MainWindow", "spectrogram range", None))
        self.lbl_labelType.setText(QtWidgets.QApplication.translate(
            "MainWindow", "active label", None))
        self.cb_specType.setItemText(
            0, QtWidgets.QApplication.translate("MainWindow", "audible", None))
        self.cb_specType.setItemText(
            1, QtWidgets.QApplication.translate("MainWindow", "ultra sonic", None))
        self.lbl_spec_create.setText(
            QtWidgets.QApplication.translate("MainWindow", "create", None))
        self.lbl_spec_modify.setText(
            QtWidgets.QApplication.translate("MainWindow", "modify", None))
        self.menuFile.setTitle(
            QtWidgets.QApplication.translate("MainWindow", "File", None))
        self.actionOpen_folder.setText(
            QtWidgets.QApplication.translate("MainWindow", "Open folder", None))
        self.actionClass_settings.setText(
            QtWidgets.QApplication.translate("MainWindow", "Class settings", None))
        self.actionExport_settings.setText(
            QtWidgets.QApplication.translate("MainWindow", "export settings", None))
        self.actionImport_settings.setText(
            QtWidgets.QApplication.translate("MainWindow", "import settings", None))


class SmallEdit(QtWidgets.QTextEdit):
    def __init__(self, *args, **kwargs):
        super(SmallEdit, self).__init__(*args, **kwargs)

    def sizeHint(self):
        return QtCore.QSize(10, 10)


class SVGButton(QtWidgets.QPushButton):
    def __init__(self, svgPath=None, *args, **kwargs):
        super(SVGButton, self).__init__(*args, **kwargs)
        self.setSizePolicy(QtWidgets.QSizePolicy.Preferred,
                           QtWidgets.QSizePolicy.Preferred)
        self.icon = None

        self.centralWidget = QtWidgets.QWidget(self)
        self.setFlat(True)
        self.setContentsMargins(0, 0, 0, 0)
        self.setFixedSize(20, 20)

        if svgPath is not None:
            self.load(svgPath)

    def load(self, svgPath):
        if self.icon is None:
            self.icon = QtSvg.QSvgWidget(svgPath, self.centralWidget)
            self.icon.setFixedSize(self.size())
        else:
            self.icon.load(svgPath)

        self.layoutBase = QtWidgets.QHBoxLayout(self)
        self.layoutBase.setSpacing(0)
        self.layoutBase.setContentsMargins(0, 0, 0, 0)
        self.layoutBase.addWidget(self.icon)

    def resizeEvent(self, event):
        super(SVGButton, self).resizeEvent(event)

        if self.icon is not None:
            self.icon.setFixedSize(self.size())

    @staticmethod
    def getIconFolder():
        iconFolder = os.path.join(
            os.path.dirname(os.path.abspath(__file__)),
            os.path.pardir,
            'icons')

        return iconFolder
