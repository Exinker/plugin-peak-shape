import logging
from functools import wraps
from typing import Callable

from PySide6 import QtWidgets


from src.interfaces.gui.windows import ProgressWindow


LOGGER = logging.getLogger('app')


def observe(quiet: bool):
    def inner(func: Callable):

        @wraps(func)
        def wrapper(*args, **kwargs):
            if quiet:
                return func(*args, **kwargs, callback=None)

            app = QtWidgets.QApplication()

            window = ProgressWindow()
            window.show()

            try:
                return func(*args, **kwargs, callback=window.update)
            finally:
                app.quit()

        return wrapper
    return inner
