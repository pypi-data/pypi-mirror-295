from typing import List, Optional

from qtpy.QtCore import QRect, Qt, QSize, QPoint
from qtpy.QtWidgets import QSizePolicy, QLayout, QLayoutItem


# based on https://doc.qt.io/qt-5/qtwidgets-layouts-flowlayout-example.html
class FlowLayout(QLayout):
    def __init__(self, margin: int = 2, spacing: int = 3, parent=None):
        super().__init__(parent)
        self._items: List[QLayoutItem] = []
        self.setSpacing(spacing)
        self.setContentsMargins(margin, margin, margin, margin)

    def addItem(self, item: QLayoutItem):
        self._items.append(item)

    def insertWidget(self, i: int, widget):
        self.addWidget(widget)
        new = self._items.pop(-1)

        self._items.insert(i, new)
        self.update()

    def count(self) -> int:
        return len(self._items)

    def itemAt(self, index: int) -> Optional[QLayoutItem]:
        if 0 <= index < self.count():
            return self._items[index]
        return None

    def takeAt(self, index: int) -> Optional[QLayoutItem]:
        if 0 <= index < self.count():
            return self._items.pop(index)
        return None

    def hasHeightForWidth(self) -> bool:
        return True

    def heightForWidth(self, width: int) -> int:
        return self._arrange(QRect(0, 0, width, 0), True)

    def setGeometry(self, rect: QRect):
        super(FlowLayout, self).setGeometry(rect)
        self._arrange(rect, False)

    def sizeHint(self) -> QSize:
        return self.minimumSize()

    def minimumSize(self) -> QSize:
        size = QSize()
        for item in self._items:
            size = size.expandedTo(item.minimumSize())

        left, top, right, bottom = self.getContentsMargins()
        size += QSize(left + right, top + bottom)

        return size

    def _arrange(self, rect: QRect, testOnly: bool) -> int:
        left, top, right, bottom = self.getContentsMargins()
        effectiveRect: QRect = rect.adjusted(left, top, -right, -bottom)
        x = effectiveRect.x()
        y = effectiveRect.y()
        lineHeight = 0

        for item in self._items:
            widget = item.widget()
            if widget and widget.isHidden():
                continue

            spacing = self.spacing()
            if spacing == -1 and widget:
                spacing = widget.style().layoutSpacing(QSizePolicy.PushButton, QSizePolicy.PushButton,
                                                       Qt.Horizontal)

            nextX = x + item.sizeHint().width() + spacing
            if nextX - spacing > effectiveRect.right() and lineHeight > 0:
                x = effectiveRect.x()
                y = y + lineHeight + spacing
                nextX = x + item.sizeHint().width() + spacing
                lineHeight = 0

            if not testOnly:
                item.setGeometry(QRect(QPoint(x, y), item.sizeHint()))

            x = nextX
            lineHeight = max(lineHeight, item.sizeHint().height())

        return y + lineHeight - rect.y() + bottom


class CurvedFlowLayout(FlowLayout):

    def _arrange(self, rect: QRect, testOnly: bool) -> int:
        left, top, right, bottom = self.getContentsMargins()
        effectiveRect: QRect = rect.adjusted(left, top, -right, -bottom)
        x = effectiveRect.x()
        y = effectiveRect.y()
        lineHeight = 0

        forward = True

        for item in self._items:
            widget = item.widget()
            spacing = self.spacing()
            if spacing == -1:
                spacing = widget.style().layoutSpacing(QSizePolicy.PushButton, QSizePolicy.PushButton,
                                                       Qt.Horizontal)
            if forward:
                nextX = x + item.sizeHint().width() + spacing
                if nextX - spacing > effectiveRect.right() and lineHeight > 0:
                    forward = False
                    x = nextX - spacing - item.sizeHint().width()
                    nextX = x - item.sizeHint().width() - spacing
                    y = y + lineHeight + spacing
                    lineHeight = 0
            else:
                nextX = x - item.sizeHint().width() - spacing
                if nextX + spacing < effectiveRect.x() and lineHeight > 0:
                    forward = True
                    x = effectiveRect.x()
                    nextX = x + item.sizeHint().width() + spacing
                    y = y + lineHeight + spacing

                    lineHeight = 0

            if not forward:
                x = x - item.sizeHint().width()

            if not testOnly:
                item.setGeometry(QRect(QPoint(x, y), item.sizeHint()))

            x = nextX
            lineHeight = max(lineHeight, item.sizeHint().height())

        return y + lineHeight - rect.y() + bottom
