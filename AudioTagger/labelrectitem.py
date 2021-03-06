from PySide2 import QtCore, QtGui

from AudioTagger.graphicsrectitems import ContextMenuItem
from pyqtextra.graphics.info_rect_item import InfoRectItem


class LabelRectItem(InfoRectItem, ContextMenuItem):

    RESIZE_COLOR = "#32ffffff"
    SELECTED_COLOR = "#ffffffff"
    BG_SUFFIX = " (bg)"
    BG_COLOR = "#bbb4b4b4"
    FG_COLOR = "#00ffffff"
    NOISE_RAIN = 1
    NOISE_WIND = 2

    def __init__(
        self,
        label_id=0,
        label_class=None,
        sr=0,
        spec_opts=None,
        label_info=None,
        *args,
        **kwargs
    ):
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
        self._selected = False
        self.overlap = []
        self._background = False
        self.noise = 0
        self.setResizeBoxColor(self.RESIZE_COLOR)
        self.current_color = self.SELECTED_COLOR

        self.label_class = label_class

        if label_info:
            self.extract_info(label_info)

    @property
    def selected(self):
        return self._selected

    @selected.setter
    def selected(self, selected):
        self._selected = selected
        if selected:
            self.current_color = self.SELECTED_COLOR
        else:
            self.current_color = self.label_class.color
        self.setRectColor(self.current_color)

    @property
    def background(self):
        return self._background

    @background.setter
    def background(self, background):
        self._background = background
        # info_string = self.infoString
        if background:
            # info_string += self.BG_SUFFIX
            self.setBrush(QtGui.QBrush(self.BG_COLOR, QtCore.Qt.BDiagPattern))
        else:
            # info_string = info_string.replace(self.BG_SUFFIX, "")
            self.setBrush(QtGui.QBrush(self.FG_COLOR, QtCore.Qt.SolidPattern))
        # self.setInfoString(info_string)

    @property
    def label_class(self):
        return self._label_class

    @label_class.setter
    def label_class(self, label_class):
        self._label_class = label_class
        if label_class:
            if not self.selected:
                self.current_color = self.label_class.color
            self.update()

    def add_noise(self, noise):
        self.noise += noise

    @property
    def rain(self):
        return bool(self.noise & self.NOISE_RAIN)

    @rain.setter
    def rain(self, rain):
        add = int(rain) or -1
        self.add_noise(add * self.NOISE_RAIN)

    @property
    def wind(self):
        return bool(self.noise & self.NOISE_WIND)

    @wind.setter
    def wind(self, wind):
        add = int(wind) or -1
        self.add_noise(add * self.NOISE_WIND)

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
        self.background = label_info["background"] == "True"
        self.noise = int(label_info.get("noise", 0))

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
            info_string = ".".join([str(self.id), self.label])
            self.setInfoString(info_string)

    def update_color(self):
        self.setupInfoTextItem(fontSize=12, color=self.label_class.color)
        self.setRectColor(color=self.current_color)

    def duration(self):
        return round(self.end - self.start, 3)

    def update(self):
        self.update_infostring()
        self.update_color()

    def get_overlaps(self):
        intersects = self.collidingItems()
        overlaps = [
            str(item.id) for item in intersects if isinstance(item, self.__class__)
        ]
        return overlaps

    def getBoxCoordinates(self):
        """
        Function which parses coordinates of bounding boxes in .json files to x1, x2, y1, and y2 objects.

        Takes account of different methods of drawing bounding boxes, so that coordinates are correct regardless of how bounding boxes are drawn.

        Also takes account of boxes that are accidently drawn outside of the spectrogram.

        """

        r = [
            self.sceneBoundingRect().x(),
            self.sceneBoundingRect().y(),
            self.sceneBoundingRect().width(),
            self.sceneBoundingRect().height(),
        ]
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
