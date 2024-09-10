from qtpy.QtWidgets import QWidget

from qthandy import vbox, vline, line


def test_line(qtbot):
    widget = QWidget()
    qtbot.addWidget(widget)
    widget.show()

    vbox(widget)
    widget.layout().addWidget(line())
    widget.layout().addWidget(vline())

    assert widget.layout().count() == 2
