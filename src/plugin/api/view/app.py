import logging
from collections.abc import Sequence
from functools import wraps
from typing import Callable

from PySide6 import QtWidgets

from plugin.api.view.windows import ViewWindow
from spectrumlab.spectra import Spectrum

LOGGER = logging.getLogger('plugin-peak-shape')


def progress_wrapper(func: Callable):

    @wraps(func)
    def wrapper(*args, spectra: Sequence[Spectrum], **kwargs):

        app = QtWidgets.QApplication.instance() or QtWidgets.QApplication()

        window = ViewWindow(
            n_tabs=len(spectra),
        )
        window.show()

        try:
            result = func(
                *args,
                spectra=spectra,
                **kwargs,
                progress_callback=window.update,
                figures=window.figures,
            )
        except Exception:
            raise
        else:
            app.exec()
            return result
        finally:
            app.quit()

    return wrapper
