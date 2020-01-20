import time

from PySide2 import QtCore, QtGui, QtWidgets


class KeyboardFilter(QtCore.QObject):

    def __init__(self, parent):
        QtCore.QObject.__init__(self)
        self.parent = parent

    def eventFilter(self, obj, event):
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


class MouseFilter(QtCore.QObject):  # And this one

    PRESS_OPEN_TIME = 200

    def __init__(self, parent):
        QtCore.QObject.__init__(self)
        self.parent = parent
        self.timer = None
        self.timer_args = None
        self.timer_callback = None
        self.timer_kwargs = None

    def timerEvent(self, event):
        if self.timer_callback:
            self.timer_callback(*self.timer_args, **self.timer_kwargs)
        self.stop_timer()

    def start_timer(self, func, *args, **kwargs):
        self.timer = self.startTimer(self.PRESS_OPEN_TIME)
        self.timer_callback = func
        self.timer_args = args
        self.timer_kwargs = kwargs

    def stop_timer(self):
        if self.timer:
            self.killTimer(self.timer)
            self.timer = None

    def eventFilter(self, obj, event):
        if event.type() == QtCore.QEvent.GraphicsSceneMouseDoubleClick:
            if event.button() == QtCore.Qt.LeftButton:
                self.parent.select_label(event.scenePos())

        elif event.type() == QtCore.QEvent.GraphicsSceneMouseRelease:
            if event.button() == QtCore.Qt.LeftButton:
                self.stop_timer()
                self.parent.releaseInScene(event.scenePos())
            elif event.button() == QtCore.Qt.MiddleButton:
                self.parent.seekSound(event.scenePos().x())

            self.parent.update_info_viewer()

        elif event.type() == QtCore.QEvent.GraphicsSceneMousePress:
            if event.button() == QtCore.Qt.LeftButton:
                self.start_timer(self.parent.clickInScene, event.scenePos())
                if self.parent.activeLabel is not None:
                    self.parent.select_tag(None)
                # self.parent.clickInScene(event.scenePos())

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


class MouseInsideFilter(QtCore.QObject):
    def __init__(self, enter_callback, leave_callback):
        QtCore.QObject.__init__(self)

        self.enter_callback = enter_callback
        self.leave_callback = leave_callback

    def eventFilter(self, obj, event):
        if event.type() == QtCore.QEvent.Enter:
            self.enter_callback(obj)

        if event.type() == QtCore.QEvent.Leave:
            self.leave_callback(obj)

        return False


# Ask Peter why these are seperate classes?
class ScrollAreaEventFilter(QtCore.QObject):
    def __init__(self, callback):
        QtCore.QObject.__init__(self)
        self.callback = callback

    def eventFilter(self, obj, event):
        if isinstance(event, QtCore.QDynamicPropertyChangeEvent) \
                or event.type() == QtCore.QEvent.MouseMove:
            self.callback()
