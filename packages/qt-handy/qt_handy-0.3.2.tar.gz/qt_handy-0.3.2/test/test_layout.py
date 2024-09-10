from qtpy.QtWidgets import QWidget, QPushButton, QSpacerItem, QHBoxLayout, QVBoxLayout, QLabel, QGridLayout

from qthandy import vbox, clear_layout, hbox, margins, flow, FlowLayout, grid


def test_clear_layout(qtbot):
    widget = QWidget()
    qtbot.addWidget(widget)
    widget.show()

    layout = vbox(widget)
    layout.addWidget(QPushButton('Btn1', widget))
    layout.addWidget(QPushButton('Btn2', widget))
    layout.addSpacerItem(QSpacerItem(50, 50))

    clear_layout(widget)
    assert layout.count() == 0


def test_hbox(qtbot):
    widget = QWidget()
    qtbot.addWidget(widget)
    widget.show()

    layout = hbox(widget)

    assert widget.layout() is not None
    assert widget.layout() is layout
    assert isinstance(widget.layout(), QHBoxLayout)


def test_vbox(qtbot):
    widget = QWidget()
    qtbot.addWidget(widget)
    widget.show()

    layout = vbox(widget)

    assert widget.layout() is not None
    assert widget.layout() is layout
    assert isinstance(widget.layout(), QVBoxLayout)


def test_grid(qtbot):
    widget = QWidget()
    qtbot.addWidget(widget)
    widget.show()

    layout = grid(widget)

    assert widget.layout() is not None
    assert widget.layout() is layout
    assert isinstance(widget.layout(), QGridLayout)
    assert layout.spacing() == 3
    assert layout.horizontalSpacing() == 3
    assert layout.verticalSpacing() == 3


def test_margins(qtbot):
    widget = QWidget()
    qtbot.addWidget(widget)
    widget.show()

    vbox(widget)
    margins(widget, left=1)

    assert widget.layout().contentsMargins().left() == 1
    assert widget.layout().contentsMargins().right() == 2
    assert widget.layout().contentsMargins().top() == 2
    assert widget.layout().contentsMargins().bottom() == 2

    margins(widget, top=20, bottom=0, right=3)
    assert widget.layout().contentsMargins().left() == 1
    assert widget.layout().contentsMargins().right() == 3
    assert widget.layout().contentsMargins().top() == 20
    assert widget.layout().contentsMargins().bottom() == 0


def test_flow(qtbot):
    widget = QWidget()
    qtbot.addWidget(widget)
    widget.show()

    layout_ = flow(widget)

    assert isinstance(widget.layout(), FlowLayout)
    assert widget.layout().contentsMargins().left() == 2
    assert widget.layout().spacing() == 3

    assert widget.layout().count() == 0

    for i in range(15):
        widget.layout().addWidget(QLabel(f'Label {i + 1}'))
    assert widget.layout().count() == 15
    w = widget.size().width()
    h = widget.size().height()
    widget.resize(w // 2, h // 2)

    assert widget.layout().count() == 15

    clear_layout(widget)
    assert widget.layout().count() == 0

    layout_.addWidget(QPushButton('1'))
    layout_.addWidget(QPushButton('2'))

    layout_.insertWidget(1, QPushButton('3'))

    assert widget.layout().count() == 3
    assert layout_.itemAt(0).widget().text() == '1'
    assert layout_.itemAt(1).widget().text() == '3'
    assert layout_.itemAt(2).widget().text() == '2'
