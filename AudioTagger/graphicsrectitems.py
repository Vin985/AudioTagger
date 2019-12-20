import copy
import sys

import numpy as np
from PySide2 import QtCore, QtGui, QtWidgets


class ResizeableGraphicsRectItem(QtWidgets.QGraphicsRectItem):
    def __init__(self, callback=None, rectChangedCallback=None, *args, **kwargs):
        super(ResizeableGraphicsRectItem, self).__init__(*args, **kwargs)
        self.setFlags(QtWidgets.QGraphicsItem.ItemIsMovable |
                      QtWidgets.QGraphicsItem.ItemSendsScenePositionChanges)
        self.setAcceptHoverEvents(True)
        self.setCursor(QtCore.Qt.PointingHandCursor)
        self.callback = callback
        self.rectChangedCallback = rectChangedCallback
        self.resizeActivated = False
        self.activated = True
        self.resizeBox = None
        self.resizeFunction = None
        self.resizeBoxColor = QtGui.QColor(0, 0, 0, 50)
        self.setupResizeBox()

    def setupResizeBox(self):
        self.resizeBox = QtWidgets.QGraphicsRectItem(self)
        self.resizeBox.setRect(self.rect().x(), self.rect().y(), 0, 0)
        self.resizeBoxPenWidth = 0
        penColor = copy.copy(self.resizeBoxColor)
        penColor.setAlpha(255)
        pen = QtGui.QPen(penColor)
        pen.setWidthF(self.resizeBoxPenWidth)
        self.resizeBox.setPen(pen)
        self.resizeBox.setBrush(QtGui.QBrush(self.resizeBoxColor))
        self.resizeBox.setFlag(
            QtWidgets.QGraphicsItem.ItemStacksBehindParent, True)

    def setResizeBoxColor(self, color):
        self.resizeBoxColor = color
        self.setupResizeBox()

    def itemChange(self, change, value):
        if change == QtWidgets.QGraphicsItem.ItemPositionChange and self.callback:
            self.callback(value)

        return super(ResizeableGraphicsRectItem, self).itemChange(change, value)

    def activate(self):
        self.activated = True
        self.setFlags(QtWidgets.QGraphicsItem.ItemIsMovable |
                      QtWidgets.QGraphicsItem.ItemSendsScenePositionChanges)
        self.setCursor(QtCore.Qt.PointingHandCursor)

    def deactivate(self):
        self.deactivateResize()
        self.activated = False
        self.setFlags(QtWidgets.QGraphicsItem.ItemSendsScenePositionChanges)
        self.setCursor(QtCore.Qt.ArrowCursor)

    def contextMenuEvent(self, event):
        wa = QtWidgets.QWidgetAction(self.parent)
        self.cle = ContextLineEdit(self.parent)
        wa.setDefaultWidget(self.cle)

        menu = QtWidgets.QMenu(self.parent)
        menu.addAction("test")
        menu.addAction(wa)
        menu.exec_(event.screenPos())

    def drawResizeBox(self, x, y, width, height):
        self.resizeBox.setVisible(True)
        self.resizeActivated = True
        # self.deactivate()
        self.resizeBox.setRect(self.rect().x() + x,
                               self.rect().y() + y,
                               width,
                               height)

    def activateResizeTop(self, y):
        self.drawResizeBox(0,
                           0,
                           self.rect().width(),
                           self.rect().height() / 5.0)
        self.setCursor(QtCore.Qt.SizeVerCursor)

    def activateResizeBottom(self, y):
        self.drawResizeBox(0,
                           self.rect().height() - self.rect().height() / 5.0,
                           self.rect().width(),
                           self.rect().height() / 5.0)
        self.setCursor(QtCore.Qt.SizeVerCursor)

    def activateResizeLeft(self, x):
        self.drawResizeBox(0,
                           0,
                           self.rect().width() / 5.0,
                           self.rect().height())
        self.setCursor(QtCore.Qt.SizeHorCursor)

    def activateResizeRight(self, x):
        self.drawResizeBox(self.rect().width() - self.rect().width() / 5.0,
                           0,
                           self.rect().width() / 5.0,
                           self.rect().height())
        self.setCursor(QtCore.Qt.SizeHorCursor)

    def activateResizeTopLeft(self, x, y):
        self.drawResizeBox(0,
                           0,
                           self.rect().width() / 5.0,
                           self.rect().height() / 5.0)
        self.setCursor(QtCore.Qt.SizeFDiagCursor)

    def activateResizeTopRight(self, x, y):
        self.drawResizeBox(self.rect().width() - self.rect().width() / 5.0,
                           0,
                           self.rect().width() / 5.0,
                           self.rect().height() / 5.0)
        self.setCursor(QtCore.Qt.SizeBDiagCursor)

    def activateResizeBottomLeft(self, x, y):
        self.drawResizeBox(0,
                           self.rect().height() - self.rect().height() / 5.0,
                           self.rect().width() / 5.0,
                           self.rect().height() / 5.0)
        self.setCursor(QtCore.Qt.SizeBDiagCursor)

    def activateResizeBottomRight(self, x, y):
        self.drawResizeBox(self.rect().width() - self.rect().width() / 5.0,
                           self.rect().height() - self.rect().height() / 5.0,
                           self.rect().width() / 5.0,
                           self.rect().height() / 5.0)
        self.setCursor(QtCore.Qt.SizeFDiagCursor)

    def activateMove(self):
        self.drawResizeBox(self.rect().width() / 5.0,
                           self.rect().height() / 5.0,
                           self.rect().width() - 2 * self.rect().width() / 5.0,
                           self.rect().height() - 2 * self.rect().height() / 5.0)

        self.activate()
        self.resizeActivated = False

    def deactivateResize(self):
        self.activate()
        self.resizeActivated = False
        self.resizeBox.setVisible(False)

    def mouseCloseToTop(self, y):
        return y < self.rect().height() / 5

    def mouseCloseToBottom(self, y):
        return y > self.rect().height() - self.rect().height() / 5

    def mouseCloseToLeft(self, x):
        return x < self.rect().width() / 5

    def mouseCloseToRight(self, x):
        return x > self.rect().width() - self.rect().width() / 5

    def mouseCloseToUpperLeftCorner(self, x, y):
        return self.mouseCloseToTop(y) and self.mouseCloseToLeft(x)

    def mouseCloseToUpperRightCorner(self, x, y):
        return self.mouseCloseToTop(y) and self.mouseCloseToRight(x)

    def mouseCloseToLowerLeftCorner(self, x, y):
        return self.mouseCloseToBottom(y) and self.mouseCloseToLeft(x)

    def mouseCloseToLowerRightCorner(self, x, y):
        return self.mouseCloseToBottom(y) and self.mouseCloseToRight(x)

    def hoverMoveEvent(self, event):
        if not self.activated:
            return

        itemPos = event.pos()
        x = itemPos.x() - self.rect().x()
        y = itemPos.y() - self.rect().y()

        if self.mouseCloseToUpperLeftCorner(x, y):
            self.activateResizeTopLeft(x, y)

        elif self.mouseCloseToUpperRightCorner(x, y):
            self.activateResizeTopRight(x, y)

        elif self.mouseCloseToLowerLeftCorner(x, y):
            self.activateResizeBottomLeft(x, y)

        elif self.mouseCloseToLowerRightCorner(x, y):
            self.activateResizeBottomRight(x, y)

        elif self.mouseCloseToTop(y):
            self.activateResizeTop(y)

        elif self.mouseCloseToBottom(y):
            self.activateResizeBottom(y)

        elif self.mouseCloseToLeft(x):
            self.activateResizeLeft(x)

        elif self.mouseCloseToRight(x):
            self.activateResizeRight(x)
        else:
            self.activateMove()

    def hoverLeaveEvent(self, event):
        self.deactivateResize()

    def resizeTop(self, dx, dy):
        rect = self.rect()
        rect.setY(rect.y() + dy)
        self.setRect(rect)
        self.activateResizeTop(self.rect().y())

    def resizeBottom(self, dx, dy):
        rect = self.rect()
        rect.setHeight(rect.height() + dy)
        self.setRect(rect)
        self.activateResizeBottom(self.rect().y())

    def resizeLeft(self, dx, dy):
        rect = self.rect()
        rect.setX(rect.x() + dx)
        self.setRect(rect)
        self.activateResizeLeft(self.rect().x())

    def resizeRight(self, dx, dy):
        rect = self.rect()
        rect.setWidth(rect.width() + dx)
        self.setRect(rect)
        self.activateResizeRight(self.rect().x())

    def resizeTopLeft(self, dx, dy):
        rect = self.rect()
        rect.setY(rect.y() + dy)
        rect.setX(rect.x() + dx)
        self.setRect(rect)
        self.activateResizeTopLeft(self.rect().x(), self.rect().y())

    def resizeTopRight(self, dx, dy):
        rect = self.rect()
        rect.setY(rect.y() + dy)
        rect.setWidth(rect.width() + dx)
        self.setRect(rect)
        self.activateResizeTopRight(self.rect().x(), self.rect().y())

    def resizeBottomLeft(self, dx, dy):
        rect = self.rect()
        rect.setHeight(rect.height() + dy)
        rect.setX(rect.x() + dx)
        self.setRect(rect)
        self.activateResizeBottomLeft(self.rect().x(), self.rect().y())

    def resizeBottomRight(self, dx, dy):
        rect = self.rect()
        rect.setHeight(rect.height() + dy)
        rect.setWidth(rect.width() + dx)
        self.setRect(rect)
        self.activateResizeBottomRight(self.rect().x(), self.rect().y())

    def mousePressEvent(self, event):
        if not self.activated:
            return

        itemPos = event.pos()
        x = itemPos.x() - self.rect().x()
        y = itemPos.y() - self.rect().y()

        if self.resizeActivated:
            if self.mouseCloseToUpperLeftCorner(x, y):
                self.resizeFunction = self.resizeTopLeft

            elif self.mouseCloseToUpperRightCorner(x, y):
                self.resizeFunction = self.resizeTopRight

            elif self.mouseCloseToLowerLeftCorner(x, y):
                self.resizeFunction = self.resizeBottomLeft

            elif self.mouseCloseToLowerRightCorner(x, y):
                self.resizeFunction = self.resizeBottomRight

            elif self.mouseCloseToTop(y):
                self.resizeFunction = self.resizeTop

            elif self.mouseCloseToBottom(y):
                self.resizeFunction = self.resizeBottom

            elif self.mouseCloseToLeft(x):
                self.resizeFunction = self.resizeLeft

            elif self.mouseCloseToRight(x):
                self.resizeFunction = self.resizeRight

    def mouseMoveEvent(self, event):
        if not self.activated:
            return

        if not self.resizeActivated:
            return super(ResizeableGraphicsRectItem, self).mouseMoveEvent(event)

        itemPos = event.pos()
        lastPos = event.lastPos()
        dx = itemPos.x() - lastPos.x()
        dy = itemPos.y() - lastPos.y()

        self.resizeFunction(dx, dy)

    def setRect(self, *args, **kwargs):
        super(ResizeableGraphicsRectItem, self).setRect(*args, **kwargs)
        if self.rectChangedCallback:
            self.rectChangedCallback()


class InfoRectItem(ResizeableGraphicsRectItem):
    def __init__(self, infoString=None, callback=None, *args, **kwargs):
        super(InfoRectItem, self).__init__(callback, *args, **kwargs)
        self.infoString = infoString
        self.infoTextItem = QtWidgets.QGraphicsSimpleTextItem(
            infoString, parent=self)

        self.infoTextItem.setPos(
            self.rect().x(), self.rect().y() - 20)

    def setupInfoTextItem(self, fontSize=12, color=None):
        self.infoTextFont = QtGui.QFont('', fontSize)
        self.infoTextItem.setFont(self.infoTextFont)

        if not color:
            color = QtGui.QColor(255, 0, 0, 100)
        self.setColor(color)

    def setColor(self, color):
        self.setPen(QtGui.QPen(color))
        self.infoTextItem.setBrush(QtGui.QBrush(color))

    def setInfoString(self, s):
        self.infoString = s
        if self.infoString and self.infoTextItem:
            self.infoTextItem.setText(self.infoString)

    def hoverEnterEvent(self, event):
        if not self.activated:
            return

        # self.infoTextItem.setVisible(True)
        super(InfoRectItem, self).hoverEnterEvent(event)

    def hoverLeaveEvent(self, event):
        if not self.activated:
            return

        # self.infoTextItem.setVisible(False)
        super(InfoRectItem, self).hoverLeaveEvent(event)

    def mouseMoveEvent(self, event):
        if not self.activated:
            return

        super(InfoRectItem, self).mouseMoveEvent(event)
        self.infoTextItem.setPos(self.rect().x(), self.rect().y() - 20)

    def setRect(self, *args, **kwargs):
        super(InfoRectItem, self).setRect(*args, **kwargs)
        if self.infoTextItem:
            self.infoTextItem.setPos(
                self.rect().x(), self.rect().y() - 20)


class ContextMenuItem():
    def __init__(self, menu=None, context_register_callback=None, **kwargs):
        self.menu = menu
        self.contextRegisterCallback = context_register_callback

    def contextMenuEvent(self, event):
        if not self.activated:
            return

        if self.contextRegisterCallback:
            self.contextRegisterCallback(self)

        self.menu.exec_(event.screenPos())
