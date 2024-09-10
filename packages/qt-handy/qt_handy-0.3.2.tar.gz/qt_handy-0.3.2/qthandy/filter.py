import pickle
from typing import List, Optional

from qtpy import PYSIDE2, QT5
from qtpy.QtCore import QObject, QEvent, Signal, QMimeData, QByteArray, Qt, QPoint, QPointF
from qtpy.QtGui import QCursor, QDrag
from qtpy.QtWidgets import QWidget, QToolTip, QPushButton, QToolButton, QAbstractButton, QApplication

from qthandy import translucent


class InstantTooltipEventFilter(QObject):
    def __init__(self, parent):
        super(InstantTooltipEventFilter, self).__init__(parent)

    def eventFilter(self, watched: QObject, event: QEvent) -> bool:
        if isinstance(watched, QWidget) and event.type() == QEvent.Enter:
            QToolTip.showText(QCursor.pos(), watched.toolTip())
        elif event.type() == QEvent.Leave:
            QToolTip.hideText()

        return super(InstantTooltipEventFilter, self).eventFilter(watched, event)


class ObjectReferenceMimeData(QMimeData):
    def __init__(self):
        super(ObjectReferenceMimeData, self).__init__()
        self._reference = None

    def reference(self):
        return self._reference

    def setReference(self, reference):
        self._reference = reference


class DragEventFilter(QObject):
    dragStarted = Signal()
    dragFinished = Signal()

    def __init__(self, target, mimeType: str, dataFunc, useObjectReference: bool = True, grabbed=None,
                 hideTarget: bool = False, startedSlot=None,
                 finishedSlot=None):
        super(DragEventFilter, self).__init__(target)
        self._target = target
        self._pressedPos: Optional[QPoint] = None
        self._useObjectReference = useObjectReference
        self._hideTarget = hideTarget
        self._mimeType = mimeType
        self._dataFunc = dataFunc
        self._grabbed = grabbed
        self._startedSlot = startedSlot
        self._finishedSlot = finishedSlot

    def eventFilter(self, watched: QObject, event: QEvent) -> bool:
        if event.type() == QEvent.MouseButtonPress:
            self._pressedPos = event.pos()
        elif event.type() == QEvent.MouseButtonRelease:
            self._pressedPos = None
        elif event.type() == QEvent.MouseMove and self._pressedPos and (
                event.pos() - self._pressedPos).manhattanLength() >= QApplication.startDragDistance():
            self._pressedPos = None
            drag = QDrag(watched)
            if self._grabbed:
                pix = self._grabbed.grab()
            else:
                pix = watched.grab()

            mimedata = ObjectReferenceMimeData()
            _object = self._dataFunc(watched)
            mimedata.setData(self._mimeType, QByteArray(pickle.dumps(_object)))
            if self._useObjectReference:
                mimedata.setReference(_object)
            drag.setMimeData(mimedata)
            drag.setPixmap(pix)
            drag.setHotSpot(event.pos())

            if self._startedSlot:
                self._startedSlot()
            self.dragStarted.emit()
            if self._hideTarget:
                self._target.setHidden(True)
            if PYSIDE2:
                drag.exec_()
            else:
                drag.exec()
            if self._finishedSlot:
                self._finishedSlot()
            self.dragFinished.emit()
            if self._hideTarget:
                self._target.setVisible(True)
        return super(DragEventFilter, self).eventFilter(watched, event)


class DropEventFilter(QObject):
    entered = Signal(QMimeData)
    left = Signal()
    moved = Signal(Qt.Edge, QPointF)
    dropped = Signal(QMimeData)

    def __init__(self, parent, mimeTypes: List[str], motionDetection: Optional[Qt.Orientation] = None, enteredSlot=None,
                 leftSlot=None, motionSlot=None, droppedSlot=None):
        super(DropEventFilter, self).__init__(parent)
        self._mimeTypes = mimeTypes
        self._motionDetection = motionDetection
        self._enteredSlot = enteredSlot
        self._leftSlot = leftSlot
        self._motionSlot = motionSlot
        self._droppedSlot = droppedSlot

    def eventFilter(self, watched: QObject, event: QEvent) -> bool:
        if event.type() == QEvent.DragEnter:
            for mime in self._mimeTypes:
                if event.mimeData().hasFormat(mime):
                    event.accept()
                    if self._enteredSlot:
                        self._enteredSlot(event.mimeData())
                    self.entered.emit(event.mimeData())
                    break
        elif event.type() == QEvent.DragLeave:
            if self._leftSlot:
                self._leftSlot()
            self.left.emit()
        elif event.type() == QEvent.Drop:
            if self._droppedSlot:
                self._droppedSlot(event.mimeData())
            self.dropped.emit(event.mimeData())
            event.accept()
        elif self._motionDetection and event.type() == QEvent.DragMove:
            pos = event.posF() if QT5 else event.position()
            if self._motionDetection == Qt.Horizontal:
                edge = Qt.LeftEdge if pos.x() < watched.width() / 2 else Qt.RightEdge
            else:
                edge = Qt.TopEdge if pos.y() < watched.height() / 2 else Qt.BottomEdge

            if self._motionSlot:
                self._motionSlot(edge, pos)
            self.moved.emit(edge, pos)

        return super(DropEventFilter, self).eventFilter(watched, event)


class DisabledClickEventFilter(QObject):
    clicked = Signal()

    def __init__(self, parent, slot=None):
        super(DisabledClickEventFilter, self).__init__(parent)
        self._slot = slot

    def eventFilter(self, watched: QObject, event: QEvent) -> bool:
        if isinstance(watched, QWidget) and event.type() == QEvent.MouseButtonRelease and not watched.isEnabled():
            self.clicked.emit()
            if self._slot:
                self._slot()

        return super(DisabledClickEventFilter, self).eventFilter(watched, event)


class VisibilityToggleEventFilter(QObject):

    def __init__(self, target: QWidget, parent: QWidget, freezeForMenu: bool = True):
        super(VisibilityToggleEventFilter, self).__init__(parent)
        self.target = target
        self.target.setHidden(True)
        self._frozen: bool = False

        if freezeForMenu and isinstance(self.target, (QPushButton, QToolButton)) and self.target.menu():
            self.target.menu().aboutToShow.connect(self._freeze)
            self.target.menu().aboutToHide.connect(self._resume)

    def eventFilter(self, watched: QObject, event: QEvent) -> bool:
        if self._frozen:
            return super(VisibilityToggleEventFilter, self).eventFilter(watched, event)
        if event.type() == QEvent.Enter:
            self.target.setVisible(True)
        elif event.type() == QEvent.Leave:
            self.target.setHidden(True)

        return super(VisibilityToggleEventFilter, self).eventFilter(watched, event)

    def _freeze(self):
        self._frozen = True

    def _resume(self):
        self._frozen = False
        self.target.setHidden(True)


class OpacityEventFilter(QObject):

    def __init__(self, parent, enterOpacity: float = 1.0, leaveOpacity: float = 0.4,
                 ignoreCheckedButton: bool = False):
        super(OpacityEventFilter, self).__init__(parent)
        self._enterOpacity = enterOpacity
        self._leaveOpacity = leaveOpacity
        self._ignoreCheckedButton = ignoreCheckedButton
        self._parent = parent
        if not ignoreCheckedButton or not self._checkedButton(parent):
            translucent(parent, leaveOpacity)
        if parent and isinstance(parent, QAbstractButton):
            parent.toggled.connect(self._btnToggled)

    def eventFilter(self, watched: QObject, event: QEvent) -> bool:
        if self._ignoreCheckedButton and self._checkedButton(watched) or not watched.isEnabled():
            return super(OpacityEventFilter, self).eventFilter(watched, event)
        if event.type() == QEvent.Type.Enter:
            translucent(watched, self._enterOpacity)
        elif event.type() == QEvent.Type.Leave:
            translucent(watched, self._leaveOpacity)

        return super(OpacityEventFilter, self).eventFilter(watched, event)

    def _checkedButton(self, obj: QObject) -> bool:
        return isinstance(obj, QAbstractButton) and obj.isChecked()

    def _btnToggled(self, toggled: bool):
        if toggled:
            translucent(self._parent, self._enterOpacity)
        else:
            translucent(self._parent, self._leaveOpacity)
