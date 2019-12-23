from PySide2 import QtCore

from AudioTagger.graphicsrectitems import ContextMenuItem, InfoRectItem


class LabelRectItem(InfoRectItem, ContextMenuItem):

    RESIZE_COLOR = "#32ffffff"

    def __init__(self, label_id=0, label_class=None, sr=0, spec_opts=None, label_info=None, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.id = label_id
        self.start = 0
        self.end = 0
        self.max_freq = 0
        self.min_freq = 0
        self.label = ""
        self.spec_opts = spec_opts
        self.sr = sr
        self.font_size = 12
        self.setResizeBoxColor(self.RESIZE_COLOR)

        if label_info:
            self.extract_info(label_info)

        self.label_class = label_class

    @property
    def label_class(self):
        return self._label_class

    @label_class.setter
    def label_class(self, label_class):
        self._label_class = label_class
        if label_class:
            self.load_label_class()

    def load_label_class(self):
        self.setInfoString(".".join([str(self.id), self.label_class.name]))
        self.setupInfoTextItem(fontSize=12, color=self.label_class.color)

    def setRect(self, *args, update_fields=True, **kwargs):
        super().setRect(*args, **kwargs)
        if update_fields:
            x1, x2, y1, y2 = self.getBoxCoordinates()
            maxSigFreq = self.sr / 2.0
            freqStep = self.spec_opts["height"] / maxSigFreq

            self.start = self.spec_opts["nstep"] * x1
            self.end = self.spec_opts["nstep"] * x2

            self.min_freq = maxSigFreq - (y2 / freqStep)
            self.max_freq = maxSigFreq - (y1 / freqStep)

    def extract_info(self, label_info):
        self.label = label_info["label"]
        self.start = float(label_info["start"])
        self.end = float(label_info["end"])
        self.max_freq = float(label_info["max_freq"])
        self.min_freq = float(label_info["min_freq"])

        self.spec_opts["nstep"] = float(label_info["nstep"])
        self.spec_opts["nwin"] = float(label_info["nwin"])

        self.create_rect()

    def create_rect(self):
        maxSigFreq = self.sr / 2.0
        freqStep = self.spec_opts["height"] / maxSigFreq

        x1 = self.start / self.spec_opts["nstep"]
        x2 = self.end / self.spec_opts["nstep"]

        y1 = (maxSigFreq - self.max_freq) * freqStep
        y2 = (maxSigFreq - self.min_freq) * freqStep

        rect = QtCore.QRectF(x1, y1, x2 - x1, y2 - y1)
        self.setRect(rect, update_fields=False)

    def update_infostring(self):
        if self.label != self.label_class.name:
            self.label = self.label_class.name
            self.setInfoString(".".join([str(self.id), self.label_class.name]))

    def update_color(self):
        self.setupInfoTextItem(fontSize=12, color=self.label_class.color)

    def update(self):
        self.update_infostring()
        self.update_color()

    def getBoxCoordinates(self):
        """
        Function which parses coordinates of bounding boxes in .json files to x1, x2, y1, and y2 objects.

        Takes account of different methods of drawing bounding boxes, so that coordinates are correct regardless of how bounding boxes are drawn.

        Also takes account of boxes that are accidently drawn outside of the spectrogram.

        """

        r = [self.sceneBoundingRect().x(),
             self.sceneBoundingRect().y(),
             self.sceneBoundingRect().width(),
             self.sceneBoundingRect().height()]
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
        if y2 > self.spec_opts["height"]:
            y2 = self.spec_opts["height"]
        # Transform y coordinates
        # y1 = (y1 - SpecRows)#*-1
        # y2 = (y2 - SpecRows)#*-1

        return x1, x2, y1, y2


# try:
#     penCol = self.labels.get_color(label_name)
# except KeyError:
#     if label_name not in self.unconfiguredLabels:
#         msgBox = QtWidgets.QMessageBox()
#         msgBox.setText("File contained undefined class")
#         msgBox.setInformativeText(
#             "Class <b>{c}</b> found in saved data. No colour " +
#             "for this class defined. Using standard color. " +
#             "Define colour in top of the source code to fix " +
#             "this error message".format(c=label_name))
#         msgBox.setStandardButtons(QtWidgets.QMessageBox.Ok)
#         ret = msgBox.exec_()
#
#         penCol = self.LABEL_DEFAULT_COLOR
#
#         self.unconfiguredLabels += [label_name]
#
# labelRect = LabelRectItem(menu=self.menu,
#                           context_register_callback=self.registerLastLabelRectContext,
#                           infoString=label_name,
#                           rectChangedCallback=self.labelRectChangedSlot)
# labelRect.setRect(rect)
# labelRect.setResizeBoxColor(QtGui.QColor(255, 255, 255, 50))
# labelRect.setupInfoTextItem(fontSize=12, color=penCol)
