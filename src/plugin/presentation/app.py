import logging
from collections.abc import Mapping
from functools import wraps
from typing import Callable

from PySide6 import QtWidgets

from plugin.config import PLUGIN_CONFIG
from plugin.presentation.windows import (
    PreviewWindow,
    ProgressWindow,
)
from spectrumapp.helpers import find_window
from spectrumlab.peaks.analyte_peaks.shapes.retrieve_shape import (
    RETRIEVE_SHAPE_AXES,
    RETRIEVE_SHAPE_INDEX,
)
from spectrumlab.spectra import Spectrum

LOGGER = logging.getLogger('plugin-peak-shape')


def progress_create(func: Callable):

    @wraps(func)
    def wrapper(*args, spectra: Mapping[int, Spectrum], **kwargs):

        app = QtWidgets.QApplication.instance() or QtWidgets.QApplication()

        if PLUGIN_CONFIG.max_workers == 1:
            window = PreviewWindow(
                indexes=tuple(spectra.keys()),
            )
        else:
            window = ProgressWindow(
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
            if isinstance(window, PreviewWindow):
                app.exec()
            return result

        finally:
            app.quit()

    return wrapper


def progress_setup(func: Callable):

    @wraps(func)
    def wrapper(__args):
        n, _ = __args

        window = find_window('previewWindow')
        if window:
            widget = window.content.widget(n)

            RETRIEVE_SHAPE_AXES.set(widget.axes)
            RETRIEVE_SHAPE_INDEX.set(n)

        try:
            result = func(__args)
            return result

        except Exception:
            raise

    return wrapper
