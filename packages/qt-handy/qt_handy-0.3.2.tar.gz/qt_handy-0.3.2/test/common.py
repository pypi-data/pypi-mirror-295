import platform
import sys


def is_darwin() -> bool:
    return platform.system() == 'Darwin'


def is_pyqt6() -> bool:
    return 'PyQt6' in sys.modules
