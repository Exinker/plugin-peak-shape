import logging
import pickle
from collections.abc import Mapping
from functools import wraps
from multiprocessing import Queue
from typing import Callable

import matplotlib.pyplot as plt
from PySide6 import QtWidgets

from plugin.config import PLUGIN_CONFIG
from plugin.presentation.view_model.windows import (
    ProgressBarWindow,
    ViewerWindow,
)
from plugin.presentation.view_model.shared_queue import send_to_queue
from spectrumapp.helpers import find_window
from spectrumlab.peaks.analyte_peaks.shapes.retrieve_shape import (
    SPECTRUM_CANVAS,
    SPECTRUM_INDEX,
)
from spectrumlab.spectra import Spectrum


LOGGER = logging.getLogger('plugin-peak-shape')


def progress_create(func: Callable):

    @wraps(func)
    def wrapper(*args, spectra: Mapping[int, Spectrum], **kwargs):

        app = QtWidgets.QApplication.instance() or QtWidgets.QApplication()

        progress_queue = Queue()

        window = ViewerWindow(
            indexes=tuple(spectra.keys()),
            queue=progress_queue,
        )
        # if PLUGIN_CONFIG.max_workers == 1:
        #     window = ViewerWindow(
        #         indexes=tuple(spectra.keys()),
        #     )
        # else:
        #     window = ProgressBarWindow(
        #         total=len(spectra),
        #     )

        try:
            result = func(
                *args,
                spectra=spectra,
                **kwargs,
                progress_callback=window.update,
                progress_queue=window.queue,
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


def progress_setup(func: Callable):

    @wraps(func)
    def wrapper(__args):
        n, _ = __args

        # window = find_window('progressWindow')
        # if isinstance(window, ViewerWindow):
        #     SPECTRUM_CANVAS.set(window.content_widget.canvas[n])
        #     SPECTRUM_INDEX.set(n)

        fig, (ax_left, ax_right) = plt.subplots(ncols=2, figsize=(12, 4), width_ratios=[2, 1], tight_layout=True)
        SPECTRUM_CANVAS.set(dict(
            left=ax_left,
            right=ax_right,
        ))
        SPECTRUM_INDEX.set(n)

        try:
            result = func(__args)

        except Exception:
            raise

        else:
            send_to_queue(n, fig)
            return result

    return wrapper
