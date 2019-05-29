from PySide2 import QtSvg, QtWidgets
import os


class SVGButton(QtWidgets.QPushButton):
    def __init__(self, svgPath=None, *args, **kwargs):
        super(SVGButton, self).__init__(*args, **kwargs)
        self.setSizePolicy(QtWidgets.QSizePolicy.Preferred,
                           QtWidgets.QSizePolicy.Preferred)
        # self.icon = None
        #
        # self.centralWidget = QtWidgets.QWidget(self)
        # self.setFlat(True)
        # self.setContentsMargins(0, 0, 0, 0)
        # self.setFixedSize(20, 20)
        #
        # if svgPath is not None:
        #     self.load(svgPath)

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
