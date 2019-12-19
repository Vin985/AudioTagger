import configparser
import csv
import datetime as dt
import os
import sys
import traceback
import warnings
from collections import OrderedDict

import librosa
import numpy as np
import qimage2ndarray as qim2np
import scipy.io.wavfile
from PySide2 import QtCore, QtGui, QtWidgets

import AudioTagger.colourMap as CM
import AudioTagger.modifyableRect as MR
from AudioTagger.gui.audio_tagger_ui import Ui_MainWindow
from AudioTagger.sound_player import SoundPlayer
from AudioTagger.tag_dialog import TagDialog
from AudioTagger.tags import Tags

# from PySide import QtCore, QtGui

WAV_EXTENSIONS = [".wav", ".WAV"]
CSV_EXTENSION = [".csv"]


class AudioTagger(QtWidgets.QMainWindow, Ui_MainWindow):

    BG_COLOR_DONE = "lightgreen"
    BG_COLOR_WIP = "peachpuff"
    LABEL_DEFAULT_COLOR = QtGui.QColor()
    LABEL_DEFAULT_COLOR.setRgb(0, 0, 200)

    def __init__(self, basefolder=None, labelfolder=None, labelTypes=None,
                 ignoreSettings=False):
        super(AudioTagger, self).__init__()

        # Usual setup stuff. Set up the user interface from Designer
        self.setupUi(self)

        # Set Event filters
        self.setFilters()

        # Working folders and files
        if not ignoreSettings:
            self.loadFoldersLocal()
        else:
            self.basefolder = None
            self.labelfolder = None
            self.files_done = []

        # Overwrite settings if provided by command line
        if basefolder:
            self.basefolder = basefolder
        if labelfolder:
            self.labelfolder = labelfolder

        # local config file
        self.local_config = None
        self.current_file = None
        self.filelist = []
        self.label_filelist = []
        self.hide_done = False

        # Sound parameters
        self.sound_player = SoundPlayer()
        self.soundSec = 0.0
        self.soundDurationSec = 0.0
        self.lastMarkerUpdate = None
        self.soundMarker = None
        self.seekingSound = False
        self.playing = False
        self.soundTimer = QtCore.QTimer()
        self.soundTimer.timeout.connect(self.updateSoundPosition)
        self.sound_speed = 1
        self.sound_speeds = [0.1, 0.125, 0.2, 0.25, 0.5, 1, 2]
        self.mouse_scene_y = None
        self.mouse_scene_x = None

        # Spectrogram settings
        self.audibleRange = True
        self.specNStepMod = 0.01    # horizontal resolution of spectogram 0.01
        self.specNWinMod = 0.03     # vertical resolution of spectogram 0.03
        self.specHeight = 360
        self.specWidth = 20000

        # Initialize gui variable
        self.mouseInOverview = False
        self.horzScrollbarValue = 0
        self.vertScrollbarValue = 0
        self.scrollingWithoutUser = False
        self.contentChanged = False
        self.isDeletingRects = False
        self.yscale = 1
        self.xscale = 1

        self.bgImg = None
        self.tracker = None
        self.viewHeight = 0
        self.viewX = 0
        self.viewY = 0
        self.viewWidth = 0
        self.viewHeight = 0
        self.setupGraphicsView()

        # Rectangle drawing
        self.rectOrgX = None
        self.rectOrgY = None
        self.isRectangleOpen = False

        # Shortcuts
        self.shortcuts = []
        self.defineShortcuts()

        # Color map
        self.cm = CM.getColourMap()

        # Label creation settings
        self.createOn = True
        self.activeLabel = None
        self.unconfiguredLabels = []
        self.labelRects = []
        self.labelRect = None
        self.labels = Tags()
        self.setupLabelMenu()
        if labelTypes is None:
            if not ignoreSettings:
                self.loadSettingsLocal()
            self.contentChanged = False
        else:
            self.labels = labelTypes

        self.configureElements()
        self.link_events()
        self.show()

        self.open_folder(self.basefolder, self.labelfolder)

        # Select opened file in tree
        # current_item = self.file_tree.findItems(
        #     self.current_file, QtCore.Qt.MatchExactly, 0)[0]
        # self.file_tree.setCurrentItem(current_item)

        self.deactivateAllLabelRects()
        self.tracker.deactivate()

    def setFilters(self):
        self.mouseEventFilter = MouseFilterObj(self)
        self.KeyboardFilter = KeyboardFilterObj(self)
        self.mouseInsideFilter = MouseInsideFilterObj(
            self.enterGV, self.leaveGV)
        self.installEventFilter(self.KeyboardFilter)

    def link_events(self):
        # GUI elements
        self.pb_next.clicked.connect(self.load_next)
        self.pb_prev.clicked.connect(self.load_previous)
        self.pb_save.clicked.connect(self.saveSceneRects)
        self.pb_toggle_create.clicked.connect(self.toggleCreateMode)
        self.pb_previous_tag.clicked.connect(self.select_previous_tag)
        self.pb_next_tag.clicked.connect(self.select_next_tag)
        self.pb_first_tag.clicked.connect(self.select_first_tag)
        self.pb_last_tag.clicked.connect(self.select_last_tag)
        self.sound_controller.pb_play.clicked.connect(self.play_pause_sound)
        self.sound_controller.pb_stop.clicked.connect(self.stopSound)
        self.sound_controller.pb_seek.clicked.connect(
            self.activateSoundSeeking)
        self.sound_controller.cb_playbackSpeed.activated.connect(
            self.selectPlaybackSpeed)
        self.sound_controller.cb_specType.activated.connect(
            self.selectSpectrogramMode)
        self.sound_controller.slider_contrast.valueChanged.connect(
            self.updateLabelWithSpectrogram)
        self.cb_labelType.currentIndexChanged.connect(
            self.changeTag)
        self.btn_done.clicked.connect(self.set_file_done)

        # Tree interaction
        self.file_tree.currentItemChanged.connect(self.change_file)

        # menu
        self.actionOpen_folder.triggered.connect(self.open_folder)
        self.actionClass_settings.triggered.connect(self.openClassSettings)
        self.actionExport_settings.triggered.connect(self.exportSettings)

        # Scroll bars
        self.scrollView.horizontalScrollBar().valueChanged.connect(self.scrollbarSlideEvent)
        self.scrollView.verticalScrollBar().valueChanged.connect(self.scrollbarSlideEvent)

    def configureElements(self):
        self.scrollView.setSizePolicy(
            QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Ignored)

        w = self.specWidth
        h = self.specHeight
        self.sceneRect = QtCore.QRectF(0, 0, w, h)
        self.overviewScene.setSceneRect(self.sceneRect)

        self.sound_controller.init_playback_speeds(
            self.sound_speeds, self.sound_speed)

    ######################## GUI STUFF ########################

    def updateViews(self):
        self.gw_overview.fitInView(self.overviewScene.itemsBoundingRect())
        self.setZoomBoundingBox()

    def resizeEvent(self, event):
        super(AudioTagger, self).resizeEvent(event)
        self.updateViews()

    # def resize(self, *size):
    #     super(AudioTagger, self).resize(*size)
    #     try:
    #         self.gw_overview.fitInView(self.overviewScene.itemsBoundingRect())
    #     except AttributeError:
    #         pass

    def closeEvent(self, event):
        canProceed = self.checkIfSavingNecessary()
        if canProceed:
            event.accept()
            self.sound_player.terminate()
        else:
            event.ignore()

    def init_tree(self):
        self.file_tree.clear()

        # Display empty tree if no files are found
        if not self.filelist:
            item = QtWidgets.QTreeWidgetItem()
            item.setText(0,
                         "No files found in folder. Please select another folder")
            self.file_tree.addTopLevelItem(item)
            return

        tree_items = []
        for file in self.filelist:
            filename = os.path.basename(file)

            item = QtWidgets.QTreeWidgetItem()
            item.setText(0, filename)

            if filename in self.files_done:
                item.setBackground(0, QtGui.QBrush(
                    QtGui.QColor(self.BG_COLOR_DONE)))
            else:
                label_file = self.create_label_filename(filename)
                if os.path.exists(label_file):
                    print(label_file + " exists")
                    item.setBackground(0, QtGui.QBrush(
                        QtGui.QColor(self.BG_COLOR_WIP)))
            tree_items.append(item)
        self.file_tree.addTopLevelItems(tree_items)

        # Select opened file in tree
        res = self.file_tree.findItems(
            os.path.basename(self.current_file), QtCore.Qt.MatchExactly, 0)
        if res:
            current_item = res[0]
            self.file_tree.setCurrentItem(current_item)

    def setupGraphicsView(self):
        self.gw_overview.setFrameStyle(QtWidgets.QFrame.NoFrame)
        self.overviewScene = QtWidgets.QGraphicsScene(self)

        # self.overviewScene.setItemIndexMethod(QtWidgets.QGraphicsScene.NoIndex)

        self.gw_overview.setScene(self.overviewScene)
        self.gw_overview.setMouseTracking(True)
        self.gw_overview.setFixedHeight(100)

        self.gw_overview.installEventFilter(self.mouseInsideFilter)

        self.scrollView.setScene(self.overviewScene)
        self.scrollView.setMouseTracking(True)

        self.overviewScene.installEventFilter(self.mouseEventFilter)

    def zoom(self, scale, scenePos=None):
        self.yscale *= scale
        self.scrollView.scale(scale, scale)
        if scenePos:
            self.scrollView.centerOn(scenePos)

        # self.lbl_zoom.setText("Vertical zoom: {0:.1f}x".format(self.yscale))
        # self.setZoomBoundingBox()

    def selectLabel0(self):
        self.cb_labelType.setCurrentIndex(0)

    def selectLabel1(self):
        self.cb_labelType.setCurrentIndex(1)

    def selectLabel2(self):
        self.cb_labelType.setCurrentIndex(2)

    def defineShortcuts(self):
        QtWidgets.QShortcut(QtGui.QKeySequence(QtCore.Qt.Key_Right + QtCore.Qt.CTRL),
                            self, self.load_next)
        QtWidgets.QShortcut(QtGui.QKeySequence(QtCore.Qt.Key_Left + QtCore.Qt.CTRL),
                            self, self.load_previous)
        QtWidgets.QShortcut(QtGui.QKeySequence(QtCore.Qt.Key_Right),
                            self, self.select_next_tag)
        QtWidgets.QShortcut(QtGui.QKeySequence(QtCore.Qt.Key_Left),
                            self, self.select_previous_tag)
        QtWidgets.QShortcut(QtGui.QKeySequence(QtCore.Qt.Key_Tab),
                            self, self.select_next_tag)
        QtWidgets.QShortcut(QtGui.QKeySequence(QtCore.Qt.CTRL + QtCore.Qt.Key_S),
                            self, self.saveSceneRects)
        QtWidgets.QShortcut(QtGui.QKeySequence(QtCore.Qt.Key_Delete),
                            self, self.deteleActiveLabel)
        QtWidgets.QShortcut(QtGui.QKeySequence(QtCore.Qt.Key_Escape),
                            self, self.abortSceneRectangle)
        QtWidgets.QShortcut(QtGui.QKeySequence(QtCore.Qt.Key_Space),
                            self, self.sound_controller.pb_play.click)
        QtWidgets.QShortcut(QtGui.QKeySequence(QtCore.Qt.Key_S),
                            self, self.activateSoundSeeking)

        def zoomIn(): return None is self.zoom(1.5)
        QtWidgets.QShortcut(QtGui.QKeySequence(QtCore.Qt.CTRL + QtCore.Qt.Key_Plus),
                            self, zoomIn)

        def zoomOut(): return None is self.zoom(0.75)
        QtWidgets.QShortcut(QtGui.QKeySequence(QtCore.Qt.CTRL + QtCore.Qt.Key_Minus),
                            self, zoomOut)

    # MOVEABLE RECT

    def setupLabelMenu(self):
        wa = QtWidgets.QWidgetAction(self)
        self.cle = MR.ContextLineEdit(wa, self)
        self.cle.setModel(self.labels.get_names())

        wa.setDefaultWidget(self.cle)

        self.menu = QtWidgets.QMenu(self)
        zAction = self.menu.addAction("Send to back")
        delAction = self.menu.addAction("Delete")
        self.menu.addAction(wa)

        delAction.triggered.connect(self.deleteLabel)
        zAction.triggered.connect(self.sendLabelToBack)
        wa.triggered.connect(self.lineEditChanged)

    def sendLabelToBack(self):
        self.activeLabel = self.labelRects.index(self.lastLabelRectContext)

        for i, labelRect in enumerate(self.labelRects):
            if i == self.activeLabel:
                labelRect.setZValue(0)
            else:
                labelRect.setZValue(labelRect.zValue() + 1)

    def deleteLabel(self):
        self.activeLabel = self.labelRects.index(self.lastLabelRectContext)
        self.deteleActiveLabel()

    def lineEditChanged(self):
        self.menu.hide()
        c = self.cle.text()

        self.lastLabelRectContext.setColor(self.labels.get_color(c))
        self.lastLabelRectContext.setInfoString(c)
        # self.rectClasses[self.lastLabelRectContext] = c
        self.contentChanged = True

    def registerLastLabelRectContext(self, labelRect):
        self.lastLabelRectContext = labelRect

    def deactivateAllLabelRects(self):
        for lr in self.labelRects:
            if lr:
                lr.deactivate()

    def activateAllLabelRects(self):
        for lr in self.labelRects:
            if lr:
                lr.activate()

    def toggleCreateMode(self):
        if not self.createOn:
            self.createOn = True
            self.deactivateAllLabelRects()
        else:
            self.createOn = False
            self.activateAllLabelRects()

        self.select_tag(None)

    def labelRectChangedSlot(self):
        self.contentChanged = True

    # SETTINGS

    def saveSettingsLocal(self):

        # settings = QtCore.QSettings()
        # settings.beginGroup("labels")
        # for i, label in enumerate(self.labels):
        #     settings.setValue("label." + str(i) + ".name", label["name"])
        #     settings.setValue("label." + str(i) + ".color", label["color"])
        #     settings.setValue("label." + str(i) +
        #                       ".keyseq", label["keyseq"])
        # settings.endGroup()
        self.labels.save("tags.yaml")

    def saveFoldersLocal(self):
        settings = QtCore.QSettings()
        settings.setValue("basefolder", self.basefolder)
        settings.setValue("labelfolder", self.labelfolder)

    def loadSettingsLocal(self):
        settings = QtCore.QSettings()
        self.labels.load("tags.yaml")
        # settings.beginGroup("labels")
        # i = 0
        # res = []
        # while True:
        #     label = {}
        #     name = settings.value("label." + str(i) + ".name", None)
        #     if not name:
        #         break
        #     label["name"] = name
        #     label["color"] = settings.value("label." + str(i) + ".color", None)
        #     label["keyseq"] = settings.value(
        #         "label." + str(i) + ".keyseq", i)
        #     res.append(label)
        #     i += 1
        # settings.endGroup()
        # self.labels = res

        #self.current_file = settings.value("current_file", None)

        self.update_labels_Ui()

    def loadFoldersLocal(self):
        settings = QtCore.QSettings()
        self.basefolder = settings.value("basefolder")
        self.labelfolder = settings.value("labelfolder")
        self.files_done = settings.value("files_done", [])
        # Special case if there is only one file, will be stored as string
        if type(self.files_done) is str:
            self.files_done = [self.files_done]

    def load_local_config(self):
        local_conf = self.basefolder + "/config.conf"
        if os.path.isfile(local_conf):
            print("conf file exists")
            config = configparser.ConfigParser()
            config.read(local_conf)
            files_done = config['files'].get("files_done", [])
            if type(files_done) is str:
                self.files_done = files_done.split(",")
            self.current_file = config['files'].get("current_file", None)
            if self.current_file and not os.path.join(self.basefolder, self.current_file) in self.filelist:
                self.current_file = None
            self.local_config = config
        else:
            self.local_config = None

    def save_local_config(self):
        local_conf = self.basefolder + "/config.conf"
        if not self.local_config:
            print("config does not loaded")
            config = configparser.ConfigParser()
            config.add_section("files")
            self.local_config = config
        self.local_config.set("files", "files_done", ",".join(self.files_done))
        if self.current_file:
            self.local_config.set("files", "current_file", self.current_file)
        try:
            with open(local_conf, 'w') as conf_file:
                self.local_config.write(conf_file)
        except Exception as e:
            # TODO add specific cases
            print(traceback.format_exc())

    def exportSettings(self):
        savePath = QtWidgets.QFileDialog().getSaveFileName(self,
                                                           "Filename to save settings",
                                                           ".",
                                                           "Setting files (*.ini)")
        saveSettings = QtCore.QSettings(savePath[0],
                                        QtCore.QSettings.IniFormat)

        settings = QtCore.QSettings()
        settings.setFallbacksEnabled(False)  # remove extra keys in Mac

        for key in settings.allKeys():
            saveSettings.setValue(key,
                                  settings.value(key))

    def openClassSettings(self):
        # cd = CD.ClassDialog(self, self.labels)
        # cd.settingsSig.connect(self.updateSettings)
        # cd.show()
        td = TagDialog(self, self.labels)
        td.settingsSig.connect(self.updateSettings)
        td.update_label_name.connect(self.update_label_name)
        td.show()

    def changeLabelIdx(self, i):
        self.cb_labelType.setCurrentIndex(i)

    def addKeySequenceToShortcuts(self, keySequence, idx):
        def func(): return self.changeLabelIdx(idx)
        self.shortcuts += [QtWidgets.QShortcut(keySequence, self, func)]

    def updateShortcuts(self):
        # keySequences = [label["keyseq"] for label in self.labels]
        keySequences = self.labels.get_key_sequences()
        n_shortcuts = len(self.shortcuts)
        for idx, keySequence in enumerate(keySequences):
            if idx < n_shortcuts:
                self.shortcuts[idx].setKey(keySequence)
            else:
                self.addKeySequenceToShortcuts(keySequence, idx)

            self.shortcuts[idx].setEnabled(bool(keySequence))

        # disable all shortcuts that do not have corresponding class
        if len(keySequences) < len(self.shortcuts):
            for i in range(len(keySequences), len(self.shortcuts)):
                self.shortcuts[i].setEnabled(False)
                del self.shortcuts[i]

    def update_labels_Ui(self):
        cc = self.contentChanged

        # update all label colours by forcing a redraw
        self.convertRectsToLabelRects(self.convertLabelRectsToRects())
        self.contentChanged = cc

        # Remove all entries in annotation combobox
        for i in range(self.cb_labelType.count()):
            self.cb_labelType.removeItem(0)

        # Update combobox with new labels
        # label_names = [label["name"] for label in self.labels]
        label_names = self.labels.get_names()
        self.cb_labelType.addItems(label_names)
        self.cle.setModel(label_names)

        # update keyboard shortcuts
        self.updateShortcuts()

    def updateSettings(self, labels):
        # self.labels = labels
        # print("in update settings")
        self.update_labels_Ui()
        self.saveSettingsLocal()

    def update_label_name(self, old, new):
        for labelRect in self.labelRects:
            if labelRect.infoString == old:
                labelRect.setInfoString(new)
                print("replacing: " + old + "by: " + new)

    def change_file(self, item, column):
        file = item.text(0)
        if file != self.current_file:
            self.load_file(file)

    def selectPlaybackSpeed(self, idx):
        self.change_playback_speed(
            float(self.sound_controller.cb_playbackSpeed.itemText(idx)))

    def selectSpectrogramMode(self, idx):
        canProceed = self.checkIfSavingNecessary()

        if not canProceed:
            if idx == 0:
                self.sound_controller.cb_specType.setCurrentIndex(1)
            elif idx == 1:
                self.sound_controller.cb_specType.setCurrentIndex(0)
            return

        if idx == 0:
            self.changeSpectrogramModeToAudible()
        elif idx == 1:
            self.changeSpectrogramModeToUltraSonic()

        self.resetView()
        self.updateViews()

    # def get_label_names(self):
    #     return [label["name"] for label in self.labels]

    # def get_label_color(self, label_name):
    #     for label in self.labels:
    #         if label["name"] == label_name:
    #             return label["color"]

    ################### SOUND STUFF #######################
    def updateSoundMarker(self):
        # 100 # multiply by step-size in SpecGen()
        markerPos = self.soundSec * (1.0 / self.specNStepMod)
        line = QtCore.QLineF(markerPos, 0, markerPos, self.specHeight)
        if not self.soundMarker:
            penCol = QtGui.QColor()
            penCol.setRgb(255, 0, 0)
            self.soundMarker = self.overviewScene.addLine(
                line, QtGui.QPen(penCol))
        else:
            self.soundMarker.setLine(line)

        self.gw_overview.update()
        self.overviewScene.update()

        if self.sound_controller.follow():
            self.scrollingWithoutUser = True
            # self.soundMarker)
            self.scrollView.centerOn(markerPos, self.viewCenter.y())
            self.scrollingWithoutUser = False
            self.setZoomBoundingBox(updateCenter=False)

    def change_playback_speed(self, speed):
        self.sound_speed = speed
        self.sound_player.change_speed(self.sound_speed)

    def activateSoundSeeking(self):
        if not self.playing:
            self.seekingSound = True

    def updateSoundPosition(self):
        if not self.sound_player.playing:
            self.pause_sound()
            return

        # TODO: Use sound player information instead!
        currentTime = dt.datetime.now()
        increment = (currentTime - self.lastMarkerUpdate).total_seconds()
        self.soundSec += increment * self.sound_speed
        self.lastMarkerUpdate = currentTime

        self.updateSoundMarker()
        self.update_info_viewer()

    def play_sound(self):
        if self.activeLabel is not None:
            label = self.labelRects[self.activeLabel]
            start = self.get_label_start_pos(label)
            self.seekSound(start)
        self.playing = True
        self.sound_controller.update_play_tooltip("Pause")
        self.sound_player.play()

        self.lastMarkerUpdate = dt.datetime.now()
        self.soundTimer.start(100)

    def pause_sound(self):
        self.playing = False
        self.sound_player.pause()
        self.sound_controller.update_play_tooltip("Play")
        self.soundTimer.stop()

    def play_pause_sound(self):
        if self.playing:
            self.pause_sound()
        else:
            self.play_sound()

    def stopSound(self):
        self.playing = False
        self.sound_controller.pb_play.setText("play")
        self.sound_player.stop()
        # self.s4p.stop()
        self.soundTimer.stop()

    def seekSound(self, graphicsPos):
        sec = graphicsPos * self.specNStepMod
        # self.s4p.seek(sec)
        self.sound_player.seek(sec)
        self.soundSec = sec
        self.updateSoundMarker()
        self.seekingSound = False

    def loadSound(self, wavfile):
        self.sound_player.load(wavfile)

        ################### WAV FILE LOAD  ######################

    def resetView(self):
        self.clearSceneRects()

        if self.specNStepMod == 0.01 and self.specNWinMod == 0.03:
            self.sound_controller.cb_specType.setCurrentIndex(0)
        elif self.specNStepMod == 0.001 and self.specNWinMod == 0.003:
            self.sound_controller.cb_specType.setCurrentIndex(1)
        else:
            warnings.warn(
                "loaded spectrogram does not fit in preprogrammed values of audible and ultrasonic range")

        self.zoom(1)

        self.activeLabel = None

        if self.playing:
            self.stopSound()

        self.soundSec = 0.0
        self.updateSoundMarker()

        if self.current_file:
            self.loadSceneRects()
            self.updateSpecLabel()
            file_path = os.path.join(self.basefolder, self.current_file)
            self.loadSound(file_path)
            self.setWindowTitle(
                "Audio Tagger " + os.path.basename(file_path))

        self.scrollView.horizontalScrollBar().triggerAction(
            QtWidgets.QAbstractSlider.SliderToMinimum)
        self.btn_done.setChecked(self.current_file in self.files_done)

    def load_file(self, file_name):
        if not file_name:
            if self.filelist:
                file_name = os.path.basename(self.filelist[0])
        canProceed = self.checkIfSavingNecessary()
        if not canProceed:
            return
        self.unconfiguredLabels = []
        self.current_file = file_name
        self.resetView()

        self.save_local_config()
        settings = QtCore.QSettings()
        settings.setValue("current_file", self.current_file)
        self.setZoomBoundingBox()

    def load_next(self):
        next_item = self.file_tree.itemBelow(
            self.file_tree.currentItem())
        self.load_file(next_item.text(0))
        self.file_tree.setCurrentItem(next_item)
        # self.loadFileIdx(self.fileidx + 1)
        # canProceed = self.checkIfSavingNecessary()
        # if not canProceed:
        #     return
        #
        # if self.fileidx < len(self.filelist) - 1:
        #     self.fileidx += 1
        #     self.resetView()
        #
        # self.setZoomBoundingBox()

    def load_previous(self):
        previous_item = self.file_tree.itemAbove(
            self.file_tree.currentItem())
        self.load_file(previous_item.text(0))
        self.file_tree.setCurrentItem(previous_item)
        # self.loadFileIdx(self.fileidx - 1)
        # canProceed = self.checkIfSavingNecessary()
        # if not canProceed:
        #     return
        #
        # if self.fileidx > 0:
        #     self.fileidx -= 1
        #     self.resetView()
        #
        # self.setZoomBoundingBox()

    def updateSpecLabel(self):
        self.spec = self.SpecGen(
            os.path.join(self.basefolder, self.current_file))
        self.updateLabelWithSpectrogram()
        self.specHeight = self.spec.shape[1]
        self.specWidth = self.spec.shape[0]
        self.configureElements()
        self.update_info_viewer()

    def get_file_list(self, folder, extensions=[]):
        fileList = []
        for root, dirs, files in os.walk(folder):
            for f in sorted(files):
                ext = f[-4:]
                if ext in extensions:
                    fileList.append(os.path.join(root, f))
        return fileList

    def getListOfWavefiles(self, folder):
        fileList = []
        for root, dirs, files in os.walk(folder):
            for f in sorted(files):
                if f.endswith('.wav') or f.endswith('.WAV'):
                    fileList += [os.path.join(root, f)]

        return fileList

    def open_folder(self, wavFolder=None, labelFolder=None):
        # reset current file as we are changing directory
        self.current_file = None

        # Open
        if wavFolder is None:
            dialog = QtWidgets.QFileDialog()
            dialog.setFileMode(QtWidgets.QFileDialog.Directory)
            wavFolder = dialog.getExistingDirectory(self,
                                                    "Open Folder with wav files",
                                                    "")

        self.filelist = self.get_file_list(wavFolder, WAV_EXTENSIONS)
        self.basefolder = wavFolder

        self.load_local_config()

        if labelFolder is None:
            dialog = QtWidgets.QFileDialog()
            dialog.setFileMode(QtWidgets.QFileDialog.Directory)
            labelFolder = dialog.getExistingDirectory(self,
                                                      "Open Folder with label files",
                                                      os.path.split(wavFolder)[0])
            self.labelfolder = labelFolder

        # if not self.filelist:
        #     return

        self.saveFoldersLocal()

        # self.cb_file.clear()
        # self.cb_file.addItems(self.filelist)

        self.load_file(self.current_file)

        self.init_tree()
        # TODO: reinit tree

    ####################### SPECTROGRAM #############################

    def changeSpectrogramResolution(self, nstepMod, nWinMod):
        self.specNStepMod = nstepMod    # horizontal resolution of spectogram
        self.specNWinMod = nWinMod     # vertical resolution of spectogram

    def changeSpectrogramModeToAudible(self):
        self.changeSpectrogramResolution(0.01, 0.03)

    def changeSpectrogramModeToUltraSonic(self):
        self.changeSpectrogramResolution(0.001, 0.003)

    def SpecGen(self, filepath):
        # TODO: hande multichannel!

        # audio, sr = librosa.load(filepath, sr=None)
        # spectro = librosa.stft(
        #     audio, 1024,  window="hamming")
        # #spectro = librosa.feature.melspectrogram(S=spectro)
        # spec = np.log(np.abs(spectro))
        # print(spec.shape)
        # # if self.denoised:
        # #     # TODO: check SNR to remove noise?
        # #     spec = self.remove_noise(spec, self.nr_N,
        # #                              self.nr_hist_rel_size, self.nr_window_smoothing)
        # #     spec = spec.astype("float32")
        # #
        # # if self.normalize:
        # #     spec = librosa.util.normalize(spec)
        # #
        # # if self.to_db:
        # #     spec = librosa.amplitude_to_db(spec, ref=np.max)
        # #
        # return spec.T
        """
        Code to generate spectrogram adapted from code posted on https://mail.python.org/pipermail/chicago/2010-December/007314.html by Ken Schutte (kenshutte@gmail.com)
        """
        sr, x = scipy.io.wavfile.read(filepath)
        # Convert stereo to mono
        if len(x.shape) > 1:
            x = x.sum(axis=1) / 2

        self.soundDurationSec = x.shape[0] / float(sr)

        # Parameters
        nstep = int(sr * self.specNStepMod)
        nwin = int(sr * self.specNWinMod)
        nfft = nwin

        # Get all windows of x with length n as a single array, using strides to avoid data duplication
        # shape = (nfft, len(range(nfft, len(x), nstep)))
        shape = (nfft, int((x.shape[0] - nfft - 1) / nstep) + 1)
        strides = (x.itemsize, nstep * x.itemsize)
        x_wins = np.lib.stride_tricks.as_strided(
            x, shape=shape, strides=strides)

        # Apply hamming window
        x_wins_ham = np.hamming(x_wins.shape[0])[..., np.newaxis] * x_wins

        # compute fft
        fft_mat = np.fft.rfft(x_wins_ham, n=nfft, axis=0)[:int(nfft / 2), :]

        # log magnitude
        fft_mat_lm = np.log(np.abs(fft_mat))
        # return spec.T

        return fft_mat_lm.T

    def updateLabelWithSpectrogram(self):
        # clrSpec = np.uint8(plt.cm.binary(spec / np.max(spec)) * 255)#To change color, alter plt.cm.jet to plt.cm.#alternative code#
        # To change color, alter plt.cm.jet to plt.cm.#alternative code#
        clrSpec = self.spec / self.sound_controller.contrast()
        clrSpec = np.uint8(self.cm(clrSpec) * 255)
        clrSpec = np.rot90(clrSpec, 1)
        # clrSpec = spmisc.imresize(clrSpec, 0.25)
        # converting from numpy array to qt image
        qi = qim2np.array2qimage(clrSpec, True)
        self.setBackgroundImage(qi)

    def setBackgroundImage(self, qi):
        px = QtGui.QPixmap().fromImage(qi)
        if self.bgImg:
            self.overviewScene.removeItem(self.bgImg)

        self.bgImg = QtWidgets.QGraphicsPixmapItem(
            px)  # Change Qt array to a Qt graphic
        self.overviewScene.addItem(self.bgImg)
        # Ensure spectrogram graphic is displayed as background
        self.bgImg.setZValue(-100)
        self.bgImg.setPos(0, 0)

        self.gw_overview.ensureVisible(self.bgImg)
        self.gw_overview.fitInView(self.overviewScene.itemsBoundingRect())

    def debug(self):
        self.isDeletingRects = not self.isDeletingRects
        print(self.isDeletingRects)

    #################### VISUALZATION/ INTERACTION (GRAPHICVIEWS) #######################

    def leaveGV(self, gv):
        if gv is self.gw_overview:
            self.mouseInOverview = False
            self.tracker.deactivate()

            if not self.createOn:
                self.activateAllLabelRects()

    def enterGV(self, gv):
        if gv is self.gw_overview:
            self.mouseInOverview = True
            self.tracker.activate()
            self.deactivateAllLabelRects()

    def setZoomBoundingBox(self, updateCenter=True):

        self.viewX = self.scrollView.horizontalScrollBar().value()
        areaWidth = self.scrollView.width()
        self.viewWidth = float(areaWidth)

        self.viewY = self.scrollView.verticalScrollBar().value() * (1.0 / self.yscale)

        self.viewHeight = self.scrollView.height()
        if self.viewHeight > self.specHeight * self.yscale:
            self.viewHeight = self.specHeight * self.yscale

        self.viewHeight *= (1.0 / self.yscale)
        if updateCenter:
            self.viewCenter = self.scrollView.mapToScene(
                self.scrollView.viewport().rect().center())

        self.updateZoomBoundingBox()

    def moveScrollViewSceneRect(self, pos):
        self.scrollingWithoutUser = True
        self.scrollView.fitInView(self.tracker)
        self.scrollingWithoutUser = False

    def updateZoomBoundingBox(self):
        rect = QtCore.QRectF(self.viewX, self.viewY,
                             self.viewWidth, self.viewHeight)
        if not self.tracker:
            penCol = QtGui.QColor()
            penCol.setRgb(255, 255, 255)
            # self.tracker = self.overviewScene.addRect(rect, QtGui.QPen(penCol))
            self.tracker = MovableGraphicsRectItem(
                self.moveScrollViewSceneRect)
            self.tracker.setPen(penCol)
            self.overviewScene.addItem(self.tracker)

        self.tracker.setPos(0, 0)
        self.tracker.setRect(rect)

        self.gw_overview.update()
        self.overviewScene.update()

    def scrollbarSlideEvent(self, tracking):
        if self.scrollingWithoutUser:
            return

        self.horzScrollbarValue = self.scrollView.horizontalScrollBar().value()
        self.vertScrollbarValue = self.scrollView.verticalScrollBar().value()

        if tracking:
            self.setZoomBoundingBox()
        else:
            self.setZoomBoundingBox(updateCenter=False)

    def clickInScene(self, scenePos):
        x = int(scenePos.x())
        y = int(scenePos.y())
        if self.seekingSound:
            self.seekSound(x)
            return

        # if self.cb_create.checkState() == QtCore.Qt.Checked:
        if self.createOn:
            if not self.mouseInOverview \
                    or not self.tracker.active:
                self.openSceneRectangle(x, y)

        else:
            self.toggleToItem(self.overviewScene.itemAt(scenePos, QtGui.QTransform()),
                              centerOnActiveLabel=False)

    def select_label(self, scenePos):
        self.toggleToItem(self.overviewScene.itemAt(scenePos, QtGui.QTransform()),
                          centerOnActiveLabel=False)

    def releaseInScene(self, scenePos):
        if self.isRectangleOpen:
            self.closeSceneRectangle(scenePos)

    def openSceneRectangle(self, x, y):
        if not self.labels:
            msgBox = QtWidgets.QMessageBox()
            msgBox.setText(
                "You have not specified labels yet. Please do so in File -> Class Settings.")
            msgBox.exec_()
            return

        rect = QtCore.QRectF(x, y, 0, 0)
        if self.labelRect:
            self.overviewScene.removeItem(self.labelRect)

        penCol = self.labels.get_color(self.cb_labelType.currentText())
        # self.labelRect = self.overviewScene.addRect(rect, QtGui.QPen(penCol))

        self.labelRect = MR.LabelRectItem(self.menu,
                                          self.registerLastLabelRectContext,
                                          self.cb_labelType.currentText(),
                                          rectChangedCallback=self.labelRectChangedSlot)
        self.labelRect.deactivate()
        self.labelRect.setRect(x, y, 20, 20)
        self.labelRect.setResizeBoxColor(QtGui.QColor(255, 255, 255, 50))
        self.labelRect.setupInfoTextItem(fontSize=12, color=penCol)
        # self.labelRect.rectChangedSignal.connect(self.labelRectChangedSlot)
        self.overviewScene.addItem(self.labelRect)

        # self.rectClasses[self.labelRect] = self.cb_labelType.currentText()

        self.rectOrgX = x
        self.rectOrgY = y

        self.isRectangleOpen = True

    def closeSceneRectangle(self, scenePos):
        x = int(scenePos.x())
        y = int(scenePos.y())
        # Do not create an annotation if it is a single click
        if x == self.rectOrgX and y == self.rectOrgY:
            self.overviewScene.removeItem(self.labelRect)
        else:
            self.labelRects.append(self.labelRect)
            self.labelRects.sort(key=self.getLabelTimeValue)

        self.labelRect = None
        self.contentChanged = True
        self.rectOrgX = None
        self.rectOrgY = None
        self.isRectangleOpen = False

    def resizeSceneRectangle(self, x, y):
        if self.labelRect:
            if x > self.rectOrgX:
                newX = self.rectOrgX
            else:
                newX = x

            if y > self.rectOrgY:
                newY = self.rectOrgY
            else:
                newY = y

            w = np.abs(x - self.rectOrgX)
            h = np.abs(y - self.rectOrgY)

            self.labelRect.setRect(newX,
                                   newY, w, h)

    def abortSceneRectangle(self):
        if self.isRectangleOpen:
            self.overviewScene.removeItem(self.labelRect)
            self.isRectangleOpen = False
        else:
            self.select_tag(None)
        self.labelRect = None

    def clearSceneRects(self):
        if self.labelRect:
            self.overviewScene.removeItem(self.labelRect)

        self.isRectangleOpen = False

        for labelRect in self.labelRects:
            self.overviewScene.removeItem(labelRect)

        self.labelRects = []
        self.contentChanged = True

    def show_position(self, scenePos):
        self.mouse_scene_x = int(scenePos.x())
        self.mouse_scene_y = int(scenePos.y())
        self.update_info_viewer()

    def changeTag(self, new_index):
        if self.activeLabel is not None:
            label = self.labelRects[self.activeLabel]
            tag = self.cb_labelType.itemText(new_index)
            label.setInfoString(tag)
            # label.infoString = tag
            # self.rectClasses[label] = tag

    ################### LABELS (SAVE/LOAD/NAVIGATION) #########################

    def getBoxCoordinates(self, r):
        """
        Function which parses coordinates of bounding boxes in .json files to x1, x2, y1, and y2 objects.

        Takes account of different methods of drawing bounding boxes, so that coordinates are correct regardless of how bounding boxes are drawn.

        Also takes account of boxes that are accidently drawn outside of the spectrogram.

        """
        # Get x coordinates. r[2] is the width of the box
        if r[2] > 0:
            x1 = r[0]
            x2 = r[0] + r[2]
        else:
            x1 = r[0] + r[2]
            x2 = r[0]

        # Get y coordinates. r[3] is the height of the box
        if r[3] > 0:
            y1 = r[1]
            y2 = r[1] + r[3]
        else:
            y1 = r[1] + r[3]
            y2 = r[1]

        if x1 < 0:
            x1 = 0
        if y1 < 0:
            y1 = 0
        if y2 > self.specHeight:
            y2 = self.specHeight
        # Transform y coordinates
        # y1 = (y1 - SpecRows)#*-1
        # y2 = (y2 - SpecRows)#*-1

        return x1, x2, y1, y2

    def get_label_start_pos(self, label):
        start_pos = label.sceneBoundingRect().x()
        width = label.sceneBoundingRect().width()
        # If width is negative, remove it to get true starting pos
        if width < 0:
            start_pos += width
        return start_pos

    def convertLabelRectsToRects(self):
        labels = []
        for labelRect in self.labelRects:
            if not labelRect:
                continue

            r = [labelRect.sceneBoundingRect().x(),
                 labelRect.sceneBoundingRect().y(),
                 labelRect.sceneBoundingRect().width(),
                 labelRect.sceneBoundingRect().height()]
            # rect = [r.x(), r.y(), r.width(), r.height()]

            # freqStep = float(self.s4p.wav[0]) / self.specHeight / 2.0
            # sr = scipy.io.wavfile.read(filepath)[0]              # sampling rate
            sr = self.sound_player.sr
            maxSigFreq = sr / 2.0                               # maxium signal frequency
            # step in freqency for every pixel in y-direction
            freqStep = self.specHeight / maxSigFreq

            # boundingBox = self.spec[rect[0]:rect[0] + rect[2],
            #                         rect[1]:rect[1] + rect[3]]

            x1, x2, y1, y2 = self.getBoxCoordinates(r)
            boundingBox = self.spec[int(x1):int(x2), int(y1):int(y2)]

            # label head:
            # (wav)Filename    Label    LabelTimeStamp     Spec_NStep
            # Spec_NWin     Spec_x1     Spec_y1     Spec_x2     Spec_y2
            # LabelStartTime_Seconds    LabelEndTime_Seconds    MinimumFreq_Hz
            # MaximumFreq_Hz    MaxAmp    MinAmp    MeanAmp
            # AmpSD LabelArea_DataPoints
            label = [
                self.current_file,  # filename
                # self.rectClasses[labelRect],                    # Label
                labelRect.infoString,
                dt.datetime.now().isoformat(),                  # LabelTimeStamp
                self.specNStepMod,                              # Spec_NStep
                self.specNWinMod,                               # Spec_NWin
                x1, y1, x2, y2,                                 # Spec_x1, y1, x2, y2
                x1 * self.specNStepMod,                         # LabelStartTime_Seconds
                x2 * self.specNStepMod,                         # LabelEndTime_Seconds
                # MinimumFreq_Hz
                maxSigFreq - (y2 / freqStep),
                # MaximumFreq_Hz
                maxSigFreq - (y1 / freqStep),
                np.max(boundingBox),                            # MaxAmp
                np.min(boundingBox),                            # MinAmp
                np.mean(boundingBox),                           # MeanAmp
                np.std(boundingBox),                            # AmpSD
                # LabelArea_DataPoints
                (x2 - x1) * (y2 - y1),
                ",".join(self.labels[labelRect.infoString].get_related())
            ]

            labels += [label]

        return labels

    def convertRectsToLabelRects(self, labels):
        self.clearSceneRects()

        for l in labels:
            labelIsEmpty = True

            for item in l:
                labelIsEmpty = labelIsEmpty and item == ""

            if labelIsEmpty:
                continue

            rect = QtCore.QRectF(float(l[5]), float(l[6]),
                                 float(l[7]) - float(l[5]),
                                 float(l[8]) - float(l[6]))
            c = l[1]

            self.specNStepMod = float(l[3])
            self.specNWinMod = float(l[4])

            try:
                penCol = self.labels.get_color(c)
            except KeyError:
                if c not in self.unconfiguredLabels:
                    msgBox = QtWidgets.QMessageBox()
                    msgBox.setText("File contained undefined class")
                    msgBox.setInformativeText(
                        "Class <b>{c}</b> found in saved data. No colour for this class defined. Using standard color. Define colour in top of the source code to fix this error message".format(c=c))
                    msgBox.setStandardButtons(QtWidgets.QMessageBox.Ok)
                    ret = msgBox.exec_()

                    penCol = self.LABEL_DEFAULT_COLOR

                    self.unconfiguredLabels += [c]

            # labelRect = self.overviewScene.addRect(rect, QtGui.QPen(penCol))

            labelRect = MR.LabelRectItem(self.menu,
                                         self.registerLastLabelRectContext,
                                         infoString=c,
                                         rectChangedCallback=self.labelRectChangedSlot)
            labelRect.setRect(rect)
            labelRect.setResizeBoxColor(QtGui.QColor(255, 255, 255, 50))
            labelRect.setupInfoTextItem(fontSize=12, color=penCol)
            # labelRect.rectChangedSignal.connect(self.labelRectChangedSlot)
            self.overviewScene.addItem(labelRect)

            self.labelRects += [labelRect]
            # self.rectClasses[labelRect] = c
        self.labelRects.sort(key=self.getLabelTimeValue)

    def saveSceneRects(self, checked=False, to_append="-sceneRect"):
        filename = self.create_label_filename(
            self.current_file, to_append=to_append, ext='.csv')

        if not os.path.exists(self.labelfolder):
            os.makedirs(self.labelfolder)

        labels = self.convertLabelRectsToRects()

        with open(filename, "w") as f:
            wr = csv.writer(f, dialect='excel')
            wr.writerow(["Filename", "Label", "LabelTimeStamp", "Spec_NStep", "Spec_NWin", "Spec_x1", "Spec_y1", "Spec_x2", "Spec_y2",
                         "LabelStartTime_Seconds", "LabelEndTime_Seconds", "MinimumFreq_Hz", "MaximumFreq_Hz",
                         "MaxAmp", "MinAmp", "MeanAmp", "AmpSD", "LabelArea_DataPoints", "Related"])
            for label in labels:

                wr.writerow(label)

        self.contentChanged = False
        if not self.current_file in self.files_done:
            self.file_tree.currentItem().setBackground(0,
                                                       QtGui.QBrush(QtGui.QColor(self.BG_COLOR_WIP)))

    def print_start_time(self):
        res = [self.getLabelTimeValue(label) for label in self.labelRects]
        print(res)

    def loadSceneRects(self, to_append="-sceneRect"):
        filename = self.create_label_filename(
            self.current_file, to_append=to_append, ext='.csv')

        if os.path.exists(filename):
            with open(filename, "r") as f:
                # dialect = csv.Sniffer().sniff(f.read(1024))
                # f.seek(0)
                reader = csv.reader(f, dialect='excel')
                rects = []
                for line in reader:
                    rects += [line]
                # rects = json.load(f)
                self.convertRectsToLabelRects(rects[1:])

        self.contentChanged = False

        if self.createOn:  # self.cb_create.checkState == QtCore.Qt.Checked:
            self.deactivateAllLabelRects()

        self.update_info_viewer()

    def create_label_filename(self, file, to_append="-sceneRect", ext='.csv'):
        file_ext = file[-4:]
        if file_ext in WAV_EXTENSIONS:
            # Everything other than last 4 characters, i.e. .wav
            filename = file[:-4]
        else:
            raise RuntimeError("Program only works for wav files")
        filename += to_append + ext  # ".csv"
        filename = os.path.join(self.labelfolder, filename)

        return filename

    def getLabelTimeValue(self, labelRect):
        return labelRect.sceneBoundingRect().x()

    def get_tag_index(self, offset):
        if not self.labelRects:
            return None
        if self.activeLabel is None:
            tag_idx = 0
        else:
            tag_idx = self.activeLabel + offset
        return tag_idx

    def select_next_tag(self):
        next_idx = self.get_tag_index(offset=1)
        if next_idx and next_idx >= len(self.labelRects):
            next_idx = 0
        self.select_tag(next_idx)

    def select_previous_tag(self):
        prev_idx = self.get_tag_index(offset=-1)
        if prev_idx and prev_idx < 0:
            prev_idx = len(self.labelRects) - 1
        self.select_tag(prev_idx)

    def select_first_tag(self):
        if not self.labelRects:
            idx = None
        else:
            idx = 0
        self.select_tag(idx)

    def select_last_tag(self):
        if not self.labelRects:
            idx = None
        else:
            idx = len(self.labelRects) - 1
        self.select_tag(idx)

    def select_tag(self, tag_idx, centerOnActiveLabel=True):
        if self.activeLabel is not None:
            old_tag = self.labelRects[self.activeLabel]
            if old_tag:
                if not old_tag.infoString in self.unconfiguredLabels:
                    penCol = self.labels.get_color(old_tag.infoString)
                else:
                    penCol = self.LABEL_DEFAULT_COLOR
                # self.rectClasses[old_tag])
                pen = QtGui.QPen(penCol)
                old_tag.setPen(pen)

        self.activeLabel = tag_idx
        if tag_idx is None:
            return

        new_tag = self.labelRects[self.activeLabel]
        penCol = QtGui.QColor()
        penCol.setRgb(255, 255, 255)
        pen = QtGui.QPen(penCol)
        new_tag.setPen(pen)

        if centerOnActiveLabel:
            self.scrollView.centerOn(new_tag)
            self.setZoomBoundingBox()
        # change tag in combo_box
        cb_tag_idx = self.cb_labelType.findText(
            new_tag.infoString, QtCore.Qt.MatchExactly)
        self.cb_labelType.setCurrentIndex(cb_tag_idx)

    def toggleToItem(self, item, centerOnActiveLabel=True):
        itemIdx = self.labelRects.index(item)
        self.select_tag(itemIdx, centerOnActiveLabel)

    def deteleActiveLabel(self):
        if self.activeLabel is None:
            return

        labelRect = self.labelRects.pop(self.activeLabel)
        self.overviewScene.removeItem(labelRect)

        self.activeLabel = None

        self.contentChanged = True

    def set_file_done(self, checked):
        if checked:
            self.files_done.append(self.current_file)
            self.file_tree.currentItem().setBackground(0,
                                                       QtGui.QBrush(QtGui.QColor(self.BG_COLOR_DONE)))
        else:
            self.files_done.remove(self.current_file)
            self.file_tree.currentItem().setBackground(0,
                                                       QtGui.QBrush(QtGui.QColor(self.BG_COLOR_WIP)))
        # settings = QtCore.QSettings()
        # settings.setValue("files_done", self.files_done)
        self.save_local_config()

    def checkIfSavingNecessary(self):
        if self.contentChanged:
            msgBox = QtWidgets.QMessageBox()
            msgBox.setText("The document has been modified.")
            msgBox.setInformativeText("Do you want to save your changes?")
            msgBox.setStandardButtons(QtWidgets.QMessageBox.Save
                                      | QtWidgets.QMessageBox.Discard
                                      | QtWidgets.QMessageBox.Cancel)
            msgBox.setDefaultButton(QtWidgets.QMessageBox.Save)
            ret = msgBox.exec_()

            if ret == QtWidgets.QMessageBox.Save:
                self.saveSceneRects()
                return True
            elif ret == QtWidgets.QMessageBox.Discard:
                return True
            elif ret == QtWidgets.QMessageBox.Cancel:
                return False
            else:
                return True
                # should never be reached
        else:
            return True

    def count_annotations(self):
        if not self.labelRects:
            return {}

        d = {}
        for labelRect in self.labelRects:
            if not labelRect:
                continue
            try:
                d[labelRect.infoString] += 1
            except KeyError:
                d[labelRect.infoString] = 1

        return d

    def update_info_viewer(self):
        if not self.current_file:
            return

        s = ''
        # s += "<p><b>File:</b> {}</p>".format(self.filelist[self.fileidx])
        curTime = "%5.3f" % self.soundSec
        dur = "%5.3f" % self.soundDurationSec

        if self.mouse_scene_x and self.mouse_scene_y:
            x_pos = round(self.mouse_scene_x *
                          self.soundDurationSec / self.overviewScene.width(), 3)

            y_pos = round((self.overviewScene.height() - self.mouse_scene_y) *
                          self.sound_player.sr / (2 * self.overviewScene.height() * 1000), 3)

            s += "<p><b>Mouse position:</b> {time}s;  {freq}kHz</p>".format(
                freq=y_pos, time=x_pos)

        # s += "<p>Mouse position x: {mx}; Mouse position y: {my}</p>".format(
        #     mx=self.mouse_scene_x, my=self.mouse_scene_y)
        # s += "<p>Scene height: {sh}; Scene width: {sw}; Scroll height: {sch}; Scroll width: {scw}</p>".format(
        #     sh=self.overviewScene.height(), sw=self.overviewScene.width(), sch=self.scrollView.height(), scw=self.scrollView.width())

        # if self.mouse_scene_y:
        #     freqs_bin = len(self.freqs) - 1
        #     loc = freqs_bin - self.mouse_scene_y
        #     if loc < 0:
        #         loc = 0
        #
        #     if loc > freqs_bin:
        #         loc = freqs_bin
        #
        #     # convert the position into kHz taking into account freq division
        #     freq_kHz = round(self.freqs[loc] / 1000.0,
        #                      3) * (1.0 / self.soundSpeed)
        #     s += "<p><b>Mouse position:</b> {}kHz".format(freq_kHz)

        s += "<p><b>Sound position:</b> {curTime}/{dur} sec</p>".format(
            curTime=curTime, dur=dur)

        c = self.count_annotations()

        if c:
            s += '<p><b>Annotations:</b></p><p style=" margin-left: 30px;">'
            for k in sorted(c.keys()):
                s += '{}  [ {} ]<br>'.format(k, c[k])

            s += "</p}"
        # self.info_viewer.setHtml(s)
        self.info_viewer.setText(s)


# Ask Peter why these are seperate classes?
class ScrollAreaEventFilter(QtCore.QObject):
    def __init__(self, callback):
        QtCore.QObject.__init__(self)
        self.callback = callback

    def eventFilter(self, obj, event):
        if type(event) == QtCore.QDynamicPropertyChangeEvent \
                or event.type() == QtCore.QEvent.MouseMove:
            self.callback()


class MouseFilterObj(QtCore.QObject):  # And this one
    def __init__(self, parent):
        QtCore.QObject.__init__(self)
        self.parent = parent

    def eventFilter(self, obj, event):
        # print(event.type())

        if event.type() == QtCore.QEvent.GraphicsSceneMouseDoubleClick:
            if event.button() == QtCore.Qt.LeftButton:
                self.parent.select_label(event.scenePos())

        elif event.type() == QtCore.QEvent.GraphicsSceneMouseRelease:
            if event.button() == QtCore.Qt.LeftButton:
                self.parent.releaseInScene(event.scenePos())
            elif event.button() == QtCore.Qt.MiddleButton:
                self.parent.seekSound(event.scenePos().x())

            self.parent.update_info_viewer()

        elif event.type() == QtCore.QEvent.GraphicsSceneMousePress:
            if event.button() == QtCore.Qt.LeftButton:
                self.parent.clickInScene(event.scenePos())

        elif event.type() == QtCore.QEvent.GraphicsSceneMouseMove:
            self.parent.show_position(event.scenePos())
            if self.parent.isRectangleOpen:
                self.parent.resizeSceneRectangle(int(event.scenePos().x()),
                                                 int(event.scenePos().y()))

        elif event.type() == QtCore.QEvent.GraphicsSceneWheel:
            if event.modifiers() & QtCore.Qt.CTRL:
                if event.delta() > 0:
                    self.parent.zoom(1.1, event.scenePos())
                else:
                    self.parent.zoom(0.9, event.scenePos())
                event.setAccepted(True)
                return True

        return False


class KeyboardFilterObj(QtCore.QObject):
    def __init__(self, parent):
        QtCore.QObject.__init__(self)
        self.parent = parent

    def eventFilter(self, obj, event):
        # print event.type()
        if event.type() == QtCore.QEvent.KeyPress:
            if event.key() == QtCore.Qt.Key_Tab:
                self.parent.toggleLabels()
            elif event.key() == QtCore.Qt.Key_Left:
                if event.modifiers() & QtCore.Qt.ControlModifier:
                    self.parent.load_previous()
                else:
                    self.parent.select_previous_tag()
            elif event.key() == QtCore.Qt.Key_Right:
                if event.modifiers() & QtCore.Qt.ControlModifier:
                    self.parent.load_next()
                else:
                    self.parent.select_next_tag()
            elif event.key() == QtCore.Qt.Key_Shift:
                if self.parent.createOn:
                    self.parent.toggleCreateMode()

            else:
                print(event.key())
        elif event.type() == QtCore.QEvent.KeyRelease:
            if event.key() == QtCore.Qt.Key_Shift:
                if not self.parent.createOn:
                    self.parent.toggleCreateMode()
        return False

# special GraphicsRectItem that is aware of its position and does something if the position is changed


class MovableGraphicsRectItem(QtWidgets.QGraphicsRectItem):
    """ from http://stackoverflow.com/a/24757931/2156909
    """

    def __init__(self, callback=None):
        super(MovableGraphicsRectItem, self).__init__()
        self.setFlags(QtWidgets.QGraphicsItem.ItemIsMovable
                      | QtWidgets.QGraphicsItem.ItemSendsScenePositionChanges)
        self.setCursor(QtCore.Qt.PointingHandCursor)
        self.setAcceptHoverEvents(True)
        self.active = False

        self.callback = callback

    def hoverEnterEvent(self, event):
        self.active = True

    def hoverLeaveEvent(self, event):
        self.active = False

    def itemChange(self, change, value):
        if change == QtWidgets.QGraphicsItem.ItemPositionChange and self.callback:
            self.callback(value)

        return super(MovableGraphicsRectItem, self).itemChange(change, value)

    def activate(self):
        self.setFlags(QtWidgets.QGraphicsItem.ItemIsMovable
                      | QtWidgets.QGraphicsItem.ItemSendsScenePositionChanges)
        self.setCursor(QtCore.Qt.PointingHandCursor)

    def deactivate(self):
        self.setFlags(QtWidgets.QGraphicsItem.ItemSendsScenePositionChanges)
        self.setCursor(QtCore.Qt.ArrowCursor)


def main(ignoreSettings=False):
    labelTypes = OrderedDict()

    penCol = QtGui.QColor()
    penCol.setRgb(96, 96, 96)
    labelTypes["bat"] = penCol

    penCol = QtGui.QColor()
    penCol.setRgb(51, 51, 255)
    labelTypes["bird"] = penCol

    penCol = QtGui.QColor()
    penCol.setRgb(255, 0, 127)
    labelTypes["plane"] = penCol

    penCol = QtGui.QColor()
    penCol.setRgb(255, 0, 255)
    labelTypes["car"] = penCol

    app = QtWidgets.QApplication(sys.argv)

    app.setOrganizationName("UCL")
    app.setOrganizationDomain("https://github.com/groakat/AudioTagger")
    app.setApplicationName("audioTagger")

    w = AudioTagger(basefolder=None, labelfolder=None, labelTypes=None,
                    ignoreSettings=False)

    sys.exit(app.exec_())


class MouseInsideFilterObj(QtCore.QObject):
    def __init__(self, enterCallback, leaveCallback):
        QtCore.QObject.__init__(self)

        self.enterCallback = enterCallback
        self.leaveCallback = leaveCallback

    def eventFilter(self, obj, event):
        if event.type() == QtCore.QEvent.Enter:
            self.enterCallback(obj)

        if event.type() == QtCore.QEvent.Leave:
            self.leaveCallback(obj)

        return False


if __name__ == "__main__":
    main()
