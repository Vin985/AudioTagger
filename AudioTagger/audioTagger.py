import csv
import datetime as dt
import os
import sys
import warnings
from collections import OrderedDict

import numpy as np
import qimage2ndarray as qim2np
import scipy.io.wavfile
# from AudioTagger.gui_auto import Ui_MainWindow
from PySide2 import QtCore, QtGui, QtWidgets
from sound4python import sound4python as S4P

import AudioTagger.classDialog as CD
import AudioTagger.colourMap as CM
import AudioTagger.modifyableRect as MR
# from AudioTagger.main_gui import Ui_MainWindow
from AudioTagger.gui_mod import Ui_MainWindow
from AudioTagger.tag_dialog import TagDialog
from AudioTagger.tags import Tags

# from PySide import QtCore, QtGui


class AudioTagger(QtWidgets.QMainWindow):

    def __init__(self, basefolder=None, labelfolder=None, labelTypes=None, test=False,
                 ignoreSettings=False):
        super(AudioTagger, self).__init__()
        # Usual setup stuff. Set up the user interface from Designer
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)

        if test:
            return

        self.setFilters()

        self.mouseInOverview = False

        self.horzScrollbarValue = 0
        self.vertScrollbarValue = 0

        if not ignoreSettings:
            self.loadFoldersLocal()
        else:
            self.basefolder = None
            self.labelfolder = None

        if basefolder:
            self.basefolder = basefolder

        if labelfolder:
            self.labelfolder = labelfolder

        self.fileidx = 0
        self.current_file = None
        # self.filelist = self.getListOfWavefiles(self.basefolder)

        self.s4p = S4P.Sound4Python()
        self.soundSec = 0.0
        self.soundDurationSec = 0.0
        self.lastMarkerUpdate = None
        self.soundMarker = None
        self.seekingSound = False
        self.playing = False
        self.soundTimer = QtCore.QTimer()
        self.soundTimer.timeout.connect(self.updateSoundPosition)
        self.soundSpeed = 1
        self.soundSpeeds = [0.1, 0.125, 0.2, 0.25, 0.5, 1, 2]
        self.mouse_scene_y = None
        self.mouse_scene_x = None

        self.createOn = True

        self.audibleRange = True
        self.specNStepMod = 0.01    # horizontal resolution of spectogram 0.01
        self.specNWinMod = 0.03     # vertical resolution of spectogram 0.03

        self.scrollingWithoutUser = False

        self.activeLabel = None
        self.specHeight = 360
        self.specWidth = 20000
        self.contentChanged = False
        self.isDeletingRects = False
        self.yscale = 1
        self.xscale = 1

        self.unconfiguredLabels = []

        self.bgImg = None
        self.tracker = None
        self.scrollView = self.ui.scrollView
        self.viewHeight = 0
        self.viewX = 0
        self.viewY = 0
        self.viewWidth = 0
        self.viewHeight = 0
        self.setupGraphicsView()

        self.scrollView.horizontalScrollBar().valueChanged.connect(self.scrollbarSlideEvent)
        self.scrollView.verticalScrollBar().valueChanged.connect(self.scrollbarSlideEvent)
        self.installEventFilter(self.KeyboardFilter)

        self.shortcuts = []
        self.defineShortcuts()

        self.labelRects = []
        self.rectClasses = dict()
        self.labelRect = None

        self.cm = CM.getColourMap()
        self.rectOrgX = None
        self.rectOrgY = None
        self.isRectangleOpen = False

        # self.labelTypes = OrderedDict()
        # self.labels = []
        self.labels = Tags()
        self.setupLabelMenu()
        if labelTypes is None:
            if not ignoreSettings:
                self.loadSettingsLocal()
            self.contentChanged = False
        else:
            self.labels = labelTypes
            # self.labelTypes = labelTypes

        self.configureElements()
        self.connectElements()
        self.show()
        # self.ui.cb_labelType.addItems(self.labelTypes.keys())

        self.openFolder(self.basefolder, self.labelfolder, self.current_file)

        self.tracker.deactivate()
        self.deactivateAllLabelRects()

        self.createOn = True

        # self.ui.pb_debug.setText("toggle to last")

    def setFilters(self):
        self.mouseEventFilter = MouseFilterObj(self)
        self.KeyboardFilter = KeyboardFilterObj(self)
        self.mouseInsideFilter = MouseInsideFilterObj(
            self.enterGV, self.leaveGV)

    ######################## GUI STUFF ########################

    def updateViews(self):
        self.ui.gw_overview.fitInView(self.overviewScene.itemsBoundingRect())
        self.setZoomBoundingBox()

    def resizeEvent(self, event):
        super(AudioTagger, self).resizeEvent(event)
        self.updateViews()

    # def resize(self, *size):
    #     super(AudioTagger, self).resize(*size)
    #     try:
    #         self.ui.gw_overview.fitInView(self.overviewScene.itemsBoundingRect())
    #     except AttributeError:
    #         pass

    def closeEvent(self, event):
        canProceed = self.checkIfSavingNecessary()
        if canProceed:
            event.accept()
        else:
            event.ignore()

    def connectElements(self):
        # GUI elements
        self.ui.pb_next.clicked.connect(self.loadNext)
        self.ui.pb_prev.clicked.connect(self.loadPrev)
        self.ui.pb_toggle_back.clicked.connect(self.toggleToLast)
        self.ui.pb_save.clicked.connect(self.saveSceneRects)
        self.ui.pb_toggle.clicked.connect(self.toggleLabels)
        # self.ui.pb_edit.clicked.connect(self.toggleEdit)
        self.ui.pb_play.clicked.connect(self.playPauseSound)
        self.ui.pb_stop.clicked.connect(self.stopSound)
        self.ui.pb_seek.clicked.connect(self.activateSoundSeeking)
        # self.ui.cb_file.activated.connect(self.selectFromFilelist)
        self.ui.cb_playbackSpeed.activated.connect(self.selectPlaybackSpeed)
        self.ui.cb_specType.activated.connect(self.selectSpectrogramMode)
        self.ui.cb_labelType.currentIndexChanged.connect(self.changeTag)

        self.ui.file_tree.currentItemChanged.connect(self.change_file)

        # menu
        self.ui.actionOpen_folder.triggered.connect(self.openFolder)
        self.ui.actionClass_settings.triggered.connect(self.openClassSettings)
        self.ui.actionExport_settings.triggered.connect(self.exportSettings)

        self.ui.pb_toggle_create.clicked.connect(self.toggleCreateMode)

    def configureElements(self):
        self.scrollView.setSizePolicy(
            QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Ignored)

        w = self.specWidth
        h = self.specHeight
        self.sceneRect = QtCore.QRectF(0, 0, w, h)
        self.overviewScene.setSceneRect(self.sceneRect)

        self.ui.cb_playbackSpeed.clear()
        self.ui.cb_playbackSpeed.insertItems(
            0, [str(x) for x in self.soundSpeeds])
        self.ui.cb_playbackSpeed.setCurrentIndex(
            self.soundSpeeds.index(self.soundSpeed))

    def setupGraphicsView(self):
        self.ui.gw_overview.setFrameStyle(QtWidgets.QFrame.NoFrame)
        self.overviewScene = QtWidgets.QGraphicsScene(self)

        # self.overviewScene.setItemIndexMethod(QtWidgets.QGraphicsScene.NoIndex)

        self.ui.gw_overview.setScene(self.overviewScene)
        self.ui.gw_overview.setMouseTracking(True)
        self.ui.gw_overview.setFixedHeight(100)

        self.ui.gw_overview.installEventFilter(self.mouseInsideFilter)

        self.scrollView.setScene(self.overviewScene)
        self.scrollView.setMouseTracking(True)

        self.overviewScene.installEventFilter(self.mouseEventFilter)

    def zoom(self, scale, scenePos=None):
        self.yscale *= scale
        self.scrollView.scale(scale, scale)
        if scenePos:
            self.scrollView.centerOn(scenePos)

        # self.ui.lbl_zoom.setText("Vertical zoom: {0:.1f}x".format(self.yscale))
        # self.setZoomBoundingBox()

    def selectLabel0(self):
        self.ui.cb_labelType.setCurrentIndex(0)

    def selectLabel1(self):
        self.ui.cb_labelType.setCurrentIndex(1)

    def selectLabel2(self):
        self.ui.cb_labelType.setCurrentIndex(2)

    def defineShortcuts(self):
        QtWidgets.QShortcut(QtGui.QKeySequence(QtCore.Qt.Key_Right),
                            self, self.loadNext)
        QtWidgets.QShortcut(QtGui.QKeySequence(QtCore.Qt.Key_Left),
                            self, self.loadPrev)
        QtWidgets.QShortcut(QtGui.QKeySequence(QtCore.Qt.Key_Tab),
                            self, self.toggleLabels)
        QtWidgets.QShortcut(QtGui.QKeySequence(QtCore.Qt.CTRL + QtCore.Qt.Key_S),
                            self, self.saveSceneRects)
        QtWidgets.QShortcut(QtGui.QKeySequence(QtCore.Qt.Key_Delete),
                            self, self.deteleActiveLabel)
        QtWidgets.QShortcut(QtGui.QKeySequence(QtCore.Qt.Key_Escape),
                            self, self.abortSceneRectangle)
        QtWidgets.QShortcut(QtGui.QKeySequence(QtCore.Qt.Key_Space),
                            self, self.playPauseSound)
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
        zAction = self.menu.addAction("send to back")
        delAction = self.menu.addAction("delete")
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
        self.rectClasses[self.lastLabelRectContext] = c
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

        self.toggleTo(None)

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

        # if settings.value("fileIdx") is None:
        #     self.fileidx = 0
        # else:
        #     self.fileidx = int(settings.value("fileIdx", 0))

        self.current_file = settings.value("current_file", None)

        self.update_labels_Ui()

    def loadFoldersLocal(self):
        settings = QtCore.QSettings()
        self.basefolder = settings.value("basefolder")
        self.labelfolder = settings.value("labelfolder")

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
        td.show()

    def changeLabelIdx(self, i):
        self.ui.cb_labelType.setCurrentIndex(i)

    def addKeySequenceToShortcuts(self, keySequence, idx):
        def func(): return self.changeLabelIdx(idx)
        self.shortcuts += [QtWidgets.QShortcut(keySequence, self, func)]

    def updateShortcuts(self):
        # keySequences = [label["keyseq"] for label in self.labels]
        keySequences = self.labels.get_key_sequences()
        for idx, keySequence in enumerate(keySequences):
            if idx < len(self.shortcuts) - 1:
                self.shortcuts[idx].setKey(keySequence)
            else:
                self.addKeySequenceToShortcuts(keySequence, idx)

            self.shortcuts[idx].setEnabled(True)

        # disable all shortcuts that do not have corresponding class
        if len(keySequences) < len(self.shortcuts):
            for i in range(len(keySequences), len(self.shortcuts)):
                self.shortcuts[i].setEnabled(False)

    def update_labels_Ui(self):
        cc = self.contentChanged

        # update all label colours by forcing a redraw
        self.convertRectsToLabelRects(self.convertLabelRectsToRects())
        self.contentChanged = cc

        # Remove all entries in annotation combobox
        for i in range(self.ui.cb_labelType.count()):
            self.ui.cb_labelType.removeItem(0)

        # Update combobox with new labels
        # label_names = [label["name"] for label in self.labels]
        label_names = self.labels.get_names()
        self.ui.cb_labelType.addItems(label_names)
        self.cle.setModel(label_names)

        # update keyboard shortcuts
        self.updateShortcuts()

    def updateSettings(self, labels):
        # self.labels = labels
        # print("in update settings")
        self.update_labels_Ui()
        self.saveSettingsLocal()

    def selectFromFilelist(self, idx):
        self.loadFileIdx(idx)

    def change_file(self, item, column):
        print(item.text(0))
        self.load_file(item.text(0))

    def selectPlaybackSpeed(self, idx):
        self.changePlaybackSpeed(float(self.ui.cb_playbackSpeed.itemText(idx)))

    def selectSpectrogramMode(self, idx):
        canProceed = self.checkIfSavingNecessary()

        if not canProceed:
            if idx == 0:
                self.ui.cb_specType.setCurrentIndex(1)
            elif idx == 1:
                self.ui.cb_specType.setCurrentIndex(0)
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

        self.ui.gw_overview.update()
        self.overviewScene.update()

        if self.ui.cb_followSound.isChecked():
            self.scrollingWithoutUser = True
            # self.soundMarker)
            self.scrollView.centerOn(markerPos, self.viewCenter.y())
            self.scrollingWithoutUser = False
            self.setZoomBoundingBox(updateCenter=False)

    def changePlaybackSpeed(self, speed):
        self.soundSpeed = speed
        self.s4p.changePlaybackSpeed(self.soundSpeed)

    def activateSoundSeeking(self):
        if not self.playing:
            self.seekingSound = True

    def updateSoundPosition(self):
        if not self.s4p.playing:
            self.pauseSound()
            return

        currentTime = dt.datetime.now()
        increment = (currentTime - self.lastMarkerUpdate).total_seconds()
        self.soundSec += increment * self.soundSpeed
        self.lastMarkerUpdate = currentTime

        self.updateSoundMarker()
        self.update_info_viewer()

    def playSound(self):
        self.playing = True
        self.ui.pb_play.setToolTip("Pause")
    #    self.ui.pb_play.load(self.ui.pb_play.getIconFolder() + "/fa-pause.svg")
        self.s4p.play()
        self.soundSec = self.s4p.seekSec

        self.lastMarkerUpdate = dt.datetime.now()
        self.soundTimer.start(100)

    def pauseSound(self):
        self.playing = False
        # self.ui.pb_play.setText("play")
        self.ui.pb_play.setToolTip("Play")
    #    self.ui.pb_play.load(self.ui.pb_play.getIconFolder() + "/fa-play.svg")
        try:
            self.s4p.pause()
        except ValueError:
            pass
        self.soundTimer.stop()

    def playPauseSound(self):
        if self.playing:
            self.pauseSound()
        else:
            self.playSound()

    def stopSound(self):
        self.playing = False
        self.ui.pb_play.setText("play")
        self.s4p.stop()
        self.soundTimer.stop()

    def seekSound(self, graphicsPos):
        sec = graphicsPos * self.specNStepMod
        self.s4p.seek(sec)
        self.soundSec = sec
        self.updateSoundMarker()
        self.seekingSound = False

    def loadSound(self, wavfile):
        self.s4p.loadWav(wavfile)
        if self.soundSpeed != 1:
            self.s4p.changePlaybackSpeed(self.soundSpeed)

    ################### WAV FILE LOAD  ######################

    def resetView(self):
        self.clearSceneRects()
        self.loadSceneRects()
        self.updateSpecLabel()
        if self.specNStepMod == 0.01 and self.specNWinMod == 0.03:
            self.ui.cb_specType.setCurrentIndex(0)
        elif self.specNStepMod == 0.001 and self.specNWinMod == 0.003:
            self.ui.cb_specType.setCurrentIndex(1)
        else:
            warnings.warn(
                "loaded spectrogram does not fit in preprogrammed values of audible and ultrasonic range")

        self.zoom(1)

        self.activeLabel = None

        if self.playing:
            self.stopSound()

        self.soundSec = 0.0
        self.updateSoundMarker()

        file_path = os.path.join(self.basefolder, self.current_file)
        # self.loadSound(self.filelist[self.fileidx])
        self.loadSound(file_path)
        self.setWindowTitle(
            "Audio Tagger " + os.path.basename(file_path))

        self.scrollView.horizontalScrollBar().triggerAction(
            QtWidgets.QAbstractSlider.SliderToMinimum)

        # self.ui.cb_file.setCurrentIndex(self.fileidx)

        # print(self.filelist[self.fileidx])

    def load_file(self, file_name):
        canProceed = self.checkIfSavingNecessary()
        if not canProceed:
            return

        self.unconfiguredLabels = []
        self.current_file = file_name
        self.resetView()

        settings = QtCore.QSettings()
        settings.setValue("current_file", self.current_file)
        self.setZoomBoundingBox()

    def loadFileIdx(self, idx):
        canProceed = self.checkIfSavingNecessary()
        if not canProceed:
            return

        self.unconfiguredLabels = []
        if 0 <= idx < len(self.filelist):
            self.fileidx = idx
            self.resetView()

        settings = QtCore.QSettings()
        settings.setValue("fileIdx", self.fileidx)
        self.setZoomBoundingBox()

    def loadNext(self):
        self.loadFileIdx(self.fileidx + 1)
        # canProceed = self.checkIfSavingNecessary()
        # if not canProceed:
        #     return
        #
        # if self.fileidx < len(self.filelist) - 1:
        #     self.fileidx += 1
        #     self.resetView()
        #
        # self.setZoomBoundingBox()

    def loadPrev(self):
        self.loadFileIdx(self.fileidx - 1)
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
        self.spec, self.freqs = self.SpecGen(
            os.path.join(self.basefolder, self.current_file))
        self.updateLabelWithSpectrogram(self.spec)
        self.specHeight = self.spec.shape[1]
        self.specWidth = self.spec.shape[0]
        self.configureElements()
        self.update_info_viewer()

    def getListOfWavefiles(self, folder):
        fileList = []
        for root, dirs, files in os.walk(folder):
            for f in sorted(files):
                if f.endswith('.wav') or f.endswith('.WAV'):
                    fileList += [os.path.join(root, f)]

        return fileList

    def openFolder(self, wavFolder=None, labelFolder=None, current_file=None):
        if wavFolder is None:
            dialog = QtWidgets.QFileDialog()
            dialog.setFileMode(QtWidgets.QFileDialog.Directory)
            wavFolder = dialog.getExistingDirectory(self,
                                                    "Open Folder with wav files",
                                                    "")

        self.filelist = self.getListOfWavefiles(wavFolder)
        self.basefolder = wavFolder

        if labelFolder is None:
            dialog = QtWidgets.QFileDialog()
            dialog.setFileMode(QtWidgets.QFileDialog.Directory)
            labelFolder = dialog.getExistingDirectory(self,
                                                      "Open Folder with label files",
                                                      os.path.split(wavFolder)[0])

        self.labelfolder = labelFolder

        if len(self.filelist) == 0:
            return

        self.saveFoldersLocal()

        # self.ui.cb_file.clear()
        # self.ui.cb_file.addItems(self.filelist)

        tree_items = []
        for file in self.filelist:
            print(file)
            item = QtWidgets.QTreeWidgetItem()
            item.setText(0, os.path.basename(file))
            tree_items.append(item)
        self.ui.file_tree.addTopLevelItems(tree_items)

        if current_file:
            self.load_file(current_file)
        else:
            self.load_file(self.filelist[0])

    ####################### SPECTROGRAM #############################

    def changeSpectrogramResolution(self, nstepMod, nWinMod):
        self.specNStepMod = nstepMod    # horizontal resolution of spectogram
        self.specNWinMod = nWinMod     # vertical resolution of spectogram

    def changeSpectrogramModeToAudible(self):
        self.changeSpectrogramResolution(0.01, 0.03)

    def changeSpectrogramModeToUltraSonic(self):
        self.changeSpectrogramResolution(0.001, 0.003)

    def SpecGen(self, filepath):
        """
        Code to generate spectrogram adapted from code posted on https://mail.python.org/pipermail/chicago/2010-December/007314.html by Ken Schutte (kenshutte@gmail.com)
        """

        sr, x = scipy.io.wavfile.read(filepath)
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

        freqs = np.fft.rfftfreq(nfft, 1.0 / sr)

        # log magnitude
        fft_mat_lm = np.log(np.abs(fft_mat))

        return fft_mat_lm.T, freqs

    def updateLabelWithSpectrogram(self, spec):
        # clrSpec = np.uint8(plt.cm.binary(spec / np.max(spec)) * 255)#To change color, alter plt.cm.jet to plt.cm.#alternative code#
        # To change color, alter plt.cm.jet to plt.cm.#alternative code#
        clrSpec = np.uint8(self.cm(spec / 18.0) * 255)
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

        self.ui.gw_overview.ensureVisible(self.bgImg)
        self.ui.gw_overview.fitInView(self.overviewScene.itemsBoundingRect())

    def debug(self):
        self.isDeletingRects = not self.isDeletingRects
        print(self.isDeletingRects)

    #################### VISUALZATION/ INTERACTION (GRAPHICVIEWS) #######################

    def leaveGV(self, gv):
        if gv is self.ui.gw_overview:
            self.mouseInOverview = False
            self.tracker.deactivate()

            if not self.createOn:
                self.activateAllLabelRects()

    def enterGV(self, gv):
        if gv is self.ui.gw_overview:
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

        self.ui.gw_overview.update()
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
            self.mouseEventFilter.isRectangleOpen = False
            self.seekSound(x)
            return

        # if self.ui.cb_create.checkState() == QtCore.Qt.Checked:
        if self.createOn:
            if not self.mouseInOverview \
                    or not self.tracker.active:
                self.openSceneRectangle(x, y)

        else:
            self.mouseEventFilter.isRectangleOpen = False
            self.toggleToItem(self.overviewScene.itemAt(scenePos, QtGui.QTransform()),
                              centerOnActiveLabel=False)

    def releaseInScene(self, scenePos):
        self.closeSceneRectangle(scenePos)
        self.isRectangleOpen = False

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

        penCol = self.labels.get_color(self.ui.cb_labelType.currentText())
        # self.labelRect = self.overviewScene.addRect(rect, QtGui.QPen(penCol))

        self.labelRect = MR.LabelRectItem(self.menu,
                                          self.registerLastLabelRectContext,
                                          self.ui.cb_labelType.currentText(),
                                          rectChangedCallback=self.labelRectChangedSlot)
        self.labelRect.deactivate()
        self.labelRect.setRect(x, y, 20, 20)
        self.labelRect.setResizeBoxColor(QtGui.QColor(255, 255, 255, 50))
        self.labelRect.setupInfoTextItem(fontSize=12, color=penCol)
        # self.labelRect.rectChangedSignal.connect(self.labelRectChangedSlot)
        self.overviewScene.addItem(self.labelRect)

        self.rectClasses[self.labelRect] = self.ui.cb_labelType.currentText()

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

        self.labelRect = None
        self.contentChanged = True
        self.rectOrgX = None
        self.rectOrgY = None

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
        self.overviewScene.removeItem(self.labelRect)
        self.labelRect = None
        self.mouseEventFilter.isRectangleOpen = False

    def clearSceneRects(self):
        if self.labelRect:
            self.overviewScene.removeItem(self.labelRect)

        self.mouseEventFilter.isRectangleOpen = False

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
            tag = self.ui.cb_labelType.itemText(new_index)
            label.setInfoString(tag)
            self.rectClasses[label] = tag

    ################### LABELS (SAVE/LOAD/NAVIGATION) #########################

    def getBoxCoordinates(self, r):
        """
        Function which parses coordinates of bounding boxes in .json files to x1, x2, y1, and y2 objects.

        Takes account of different methods of drawing bounding boxes, so that coordinates are correct regardless of how bounding boxes are drawn.

        Also takes account of boxes that are accidently drawn outside of the spectrogram.

        """
        if r[2] > 0 and r[3] > 0:
            x1 = r[0]
            x2 = r[0] + r[2]
            y1 = r[1]
            y2 = r[1] + r[3]
        elif r[2] < 0 and r[3] < 0:
            x1 = r[0] + r[2]
            x2 = r[0]
            y1 = r[1] + r[3]
            y2 = r[1]
        elif r[2] > 0 and r[3] < 0:
            x1 = r[0]
            x2 = r[0] + r[2]
            y1 = r[1] + r[3]
            y2 = r[1]
        else:
            x1 = r[0] + r[2]
            x2 = r[0]
            y1 = r[1]
            y2 = r[1] + r[3]
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
            c = self.rectClasses[labelRect]

            # freqStep = float(self.s4p.wav[0]) / self.specHeight / 2.0
            # sr = scipy.io.wavfile.read(filepath)[0]              # sampling rate
            sr = self.s4p.wav[0]
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
                self.rectClasses[labelRect],                    # Label
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
                (x2 - x1) * (y2 - y1)
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

                    penCol = QtGui.QColor()
                    penCol.setRgb(0, 0, 200)

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
            self.rectClasses[labelRect] = c

    def saveSceneRects(self, checked=False, fileAppendix="-sceneRect"):
        filename = self.createLabelFilename(fileAppendix, ending='.csv')

        if not os.path.exists(self.labelfolder):
            os.makedirs(self.labelfolder)

        labels = self.convertLabelRectsToRects()

        with open(filename, "w") as f:
            wr = csv.writer(f, dialect='excel')
            wr.writerow(["Filename", "Label", "LabelTimeStamp", "Spec_NStep", "Spec_NWin", "Spec_x1", "Spec_y1", "Spec_x2", "Spec_y2",
                         "LabelStartTime_Seconds", "LabelEndTime_Seconds", "MinimumFreq_Hz", "MaximumFreq_Hz",
                         "MaxAmp", "MinAmp", "MeanAmp", "AmpSD", "LabelArea_DataPoints"])
            for label in labels:

                wr.writerow(label)

        self.contentChanged = False

    def loadSceneRects(self, fileAppendix="-sceneRect"):
        filename = self.createLabelFilename(fileAppendix, ending='.csv')

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

        if self.createOn:  # self.ui.cb_create.checkState == QtCore.Qt.Checked:
            self.deactivateAllLabelRects()

        self.update_info_viewer()

    def createLabelFilename(self, fileAppendix="-sceneRect", ending='.json'):
        currentWavFilename = self.current_file
        if currentWavFilename.endswith('.wav') or currentWavFilename.endswith('.WAV'):
            # Everything other than last 4 characters, i.e. .wav
            filename = currentWavFilename[:-4]
        else:
            raise RuntimeError("Program only works for wav files")

        # filename += fileAppendix + ".json"
        filename += fileAppendix + ending  # ".csv"
        # filename = os.path.basename(filename)
        filename = os.path.join(self.labelfolder, filename)

        return filename

    def getLabelTimeValue(self, labelRect):
        return labelRect.sceneBoundingRect().x()

    def findNextLabelInTime(self, currentActiveLabel):
        nearest = None
        for i, labelRect in enumerate(self.labelRects):
            if labelRect == self.labelRects[currentActiveLabel]:
                continue

            if labelRect is None:
                continue

            diff = self.getLabelTimeValue(labelRect) - \
                self.getLabelTimeValue(self.labelRects[currentActiveLabel])

            if diff > 0:
                if nearest is None:
                    nearest = (i, diff)
                elif nearest[1] > diff:
                    nearest = (i, diff)

        if nearest is not None:
            return nearest[0]
        else:
            return None

    def toggleLabels(self):
        # iF nothing is selected, highlight the [0] index label when toggle button pressed
        if self.activeLabel is None:
            activeLabel = 0
        else:
            activeLabel = self.findNextLabelInTime(self.activeLabel)
            if activeLabel is None:
                activeLabel = 0

        self.toggleTo(activeLabel)

    def toggleToLast(self):
        self.toggleTo(len(self.labelRects) - 1)

    def toggleTo(self, activeLabel, centerOnActiveLabel=True):
        if self.activeLabel is not None:
            penCol = self.labels.get_color(
                self.rectClasses[self.labelRects[self.activeLabel]])
            pen = QtGui.QPen(penCol)
            self.labelRects[self.activeLabel].setPen(pen)

        self.activeLabel = activeLabel
        if activeLabel is None:
            return

        print("toggling to", self.activeLabel, len(self.labelRects))
        penCol = QtGui.QColor()
        penCol.setRgb(255, 255, 255)
        pen = QtGui.QPen(penCol)
        self.labelRects[self.activeLabel].setPen(pen)

        if centerOnActiveLabel:
            self.scrollView.centerOn(self.labelRects[self.activeLabel])
            self.setZoomBoundingBox()

    def toggleToItem(self, item, centerOnActiveLabel=True):
        itemIdx = self.labelRects.index(item)
        self.toggleTo(itemIdx, centerOnActiveLabel)

    def deteleActiveLabel(self):
        if self.activeLabel is None:
            return

        labelRect = self.labelRects.pop(self.activeLabel)
        self.overviewScene.removeItem(labelRect)

        self.activeLabel = None

        self.contentChanged = True

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
        s = ''
        # s += "<p><b>File:</b> {}</p>".format(self.filelist[self.fileidx])
        curTime = "%5.3f" % self.soundSec
        dur = "%5.3f" % self.soundDurationSec

        if self.mouse_scene_x and self.mouse_scene_y:
            x_pos = round(self.mouse_scene_x *
                          self.soundDurationSec / self.overviewScene.width(), 3)

            y_pos = round((self.overviewScene.height() - self.mouse_scene_y) *
                          self.s4p.samprate / (2 * self.overviewScene.height() * 1000), 3)

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
        # self.ui.info_viewer.setHtml(s)
        self.ui.info_viewer.setText(s)


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
        self.isRectangleOpen = False

    def eventFilter(self, obj, event):
        # print(event.type())

        if event.type() == QtCore.QEvent.GraphicsSceneMouseRelease:
            if event.button() == QtCore.Qt.LeftButton:
                self.parent.releaseInScene(event.scenePos())
            # self.isRectangleOpen = not self.isRectangleOpen
            elif event.button() == QtCore.Qt.MiddleButton:
                self.parent.seekSound(event.scenePos().x())

            self.parent.update_info_viewer()

            # if self.isRectangleOpen:
        if event.type() == QtCore.QEvent.GraphicsSceneMousePress:
            if event.button() == QtCore.Qt.LeftButton:
                self.parent.clickInScene(event.scenePos())
            # else:
            #     self.parent.closeSceneRectangle()

        if event.type() == QtCore.QEvent.GraphicsSceneMouseMove:
            self.parent.show_position(event.scenePos())
            if self.parent.isRectangleOpen:
                self.parent.resizeSceneRectangle(int(event.scenePos().x()),
                                                 int(event.scenePos().y()))

        if event.type() == QtCore.QEvent.GraphicsSceneWheel:
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
                self.parent.loadPrev()
            elif event.key() == QtCore.Qt.Key_Right:
                self.parent.loadNext()
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
