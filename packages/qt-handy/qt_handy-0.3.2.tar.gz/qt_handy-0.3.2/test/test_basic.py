import sys

import pytest
from qtpy.QtCore import QSize
from qtpy.QtWidgets import QLabel, QWidget, QPushButton, QApplication, QToolButton, QMessageBox, QSizePolicy

from qthandy import translucent, hbox, retain_when_hidden, spacer, transparent, busy, btn_popup, ask_confirmation, \
    incr_icon, decr_icon, sp
from test.common import is_darwin, is_pyqt6


def test_translucent(qtbot):
    widget = QLabel('Test')
    qtbot.addWidget(widget)
    widget.show()

    translucent(widget)

    assert widget.graphicsEffect()


def test_retain_when_hidden(qtbot):
    parent = QWidget()
    parent.setFixedWidth(300)
    hbox(parent)
    stretched_btn = QPushButton('Stretched')
    btn = QPushButton()
    btn.setFixedWidth(100)
    parent.layout().addWidget(stretched_btn)
    parent.layout().addWidget(btn)

    qtbot.addWidget(parent)
    parent.show()

    prev_btn_size = stretched_btn.width()
    retain_when_hidden(btn)
    btn.setHidden(True)
    qtbot.wait(5)
    assert prev_btn_size == stretched_btn.width()


def test_spacer(qtbot):
    parent = QWidget()
    parent.setFixedWidth(300)
    hbox(parent)

    btn = QPushButton('Button')
    btn.setMinimumWidth(100)

    parent.layout().addWidget(spacer())
    parent.layout().addWidget(btn)
    qtbot.addWidget(parent)
    parent.show()

    assert btn.width() == 100


def test_spacer_with_max_stretch(qtbot):
    parent = QWidget()
    parent.setFixedWidth(300)
    hbox(parent, 0, 0)

    btn = QPushButton('Button')
    btn.setMinimumWidth(100)

    parent.layout().addWidget(spacer(max_stretch=150))
    parent.layout().addWidget(btn)
    qtbot.addWidget(parent)
    parent.show()

    if is_darwin():
        assert btn.width() == 150 if is_pyqt6() else 156
    else:
        assert btn.width() == 150


def test_transparent_label(qtbot):
    lbl = QLabel('Test')
    transparent(lbl)


@pytest.mark.skipif('PySide6' in sys.modules, reason="Cannot set override cursor with PySide6")
def test_busy(qtbot):
    @busy
    def busy_func():
        assert QApplication.overrideCursor()

    assert not QApplication.overrideCursor()
    busy_func()
    assert not QApplication.overrideCursor()


def test_btn_popup(qtbot):
    btn = QToolButton()
    qtbot.addWidget(btn)
    btn.show()

    lbl = QLabel('Test')
    popup = btn_popup(btn, lbl)

    assert popup
    assert popup.parent() is btn


def test_confirmation(qtbot, monkeypatch):
    monkeypatch.setattr(QMessageBox, "question", lambda *args: QMessageBox.Yes)  # confirm
    confirmed = ask_confirmation('Confirmation')
    assert confirmed

    monkeypatch.setattr(QMessageBox, "question", lambda *args: QMessageBox.No)  # confirm
    confirmed = ask_confirmation('Confirmation')
    assert not confirmed


def test_incr_icon(qtbot):
    btn = QPushButton()
    qtbot.addWidget(btn)

    btn.setIconSize(QSize(16, 16))
    incr_icon(btn)

    assert btn.iconSize().width() == 17
    assert btn.iconSize().height() == 17

    decr_icon(btn)

    assert btn.iconSize().width() == 16
    assert btn.iconSize().height() == 16

    incr_icon(btn, 4)

    assert btn.iconSize().width() == 20
    assert btn.iconSize().height() == 20


def test_sizepolicy_setup(qtbot):
    widget = QWidget()
    qtbot.addWidget(widget)

    pol: QSizePolicy = widget.sizePolicy()
    assert pol.horizontalPolicy() == QSizePolicy.Policy.Preferred
    assert pol.verticalPolicy() == QSizePolicy.Policy.Preferred

    sp(widget).h_max()
    pol = widget.sizePolicy()
    assert pol.horizontalPolicy() == QSizePolicy.Policy.Maximum
    assert pol.verticalPolicy() == QSizePolicy.Policy.Preferred
