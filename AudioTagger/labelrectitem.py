from PySide2 import QtCore

from AudioTagger.graphicsrectitems import ContextMenuItem, InfoRectItem


class LabelRectItem(InfoRectItem, ContextMenuItem):
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
        self.label_class = label_class

        if label_info:
            self.extract_info(label_info)

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
        self.setRect(rect)


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
