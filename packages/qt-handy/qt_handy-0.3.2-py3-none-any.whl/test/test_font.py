from qtpy.QtWidgets import QWidget

from qthandy import bold, italic, incr_font, decr_font, underline


def test_bold(qtbot):
    widget = QWidget()
    bold(widget)

    assert widget.font().bold()


def test_italic(qtbot):
    widget = QWidget()
    italic(widget)

    assert widget.font().italic()


def test_underline(qtbot):
    widget = QWidget()
    underline(widget)

    assert widget.font().underline()


def test_increase_font(qtbot):
    widget = QWidget()
    size = widget.font().pointSize()

    incr_font(widget)

    assert widget.font().pointSize() > size


def test_decrease_font(qtbot):
    widget = QWidget()
    size = widget.font().pointSize()

    decr_font(widget)

    assert widget.font().pointSize() < size
