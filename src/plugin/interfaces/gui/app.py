import logging
from functools import wraps
from typing import Callable

from PySide6 import QtWidgets

from plugin.interfaces.gui.windows import ProgressWindow

LOGGER = logging.getLogger('plugin-peak-shape')


def progress_wrapper(quiet: bool):
    def inner(func: Callable):

        @wraps(func)
        def wrapper(*args, **kwargs):
            if quiet:
                return func(*args, **kwargs, progress_callback=None)

            app = QtWidgets.QApplication.instance() or QtWidgets.QApplication()

            window = ProgressWindow()
            window.show()

            try:
                result = func(*args, **kwargs, progress_callback=window.update)
            except Exception:
                window.close()
                raise
            else:
                window.close()
                return result
            finally:
                app.quit()

        return wrapper
    return inner
