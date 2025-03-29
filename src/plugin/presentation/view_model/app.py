import logging
from collections.abc import Mapping
from functools import wraps
from typing import Callable

from PySide6 import QtWidgets

from plugin.config import PLUGIN_CONFIG
from plugin.presentation.view_model.windows import (
    ProgressBarWindow,
    ViewerWindow,
)
from spectrumlab.spectra import Spectrum

LOGGER = logging.getLogger('plugin-peak-shape')


def progress_wrapper(func: Callable):

    @wraps(func)
    def wrapper(*args, spectra: Mapping[int, Spectrum], **kwargs):

        app = QtWidgets.QApplication.instance() or QtWidgets.QApplication()

        if PLUGIN_CONFIG.max_workers == 1:
            window = ViewerWindow(
                total=len(spectra),
            )
        else:
            window = ProgressBarWindow(
                total=len(spectra),
            )

        try:
            result = func(
                *args,
                spectra=spectra,
                **kwargs,
                progress_callback=window.update,
            )
        except Exception:
            raise
        else:
            if isinstance(window, ViewerWindow):
                app.exec()

            return result
        finally:
            app.quit()

    return wrapper
