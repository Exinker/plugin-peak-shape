import logging
from collections.abc import Mapping
from functools import wraps
from typing import Callable

from PySide6 import QtWidgets

from plugin.presentation.view_model.windows import ObservabilityWindow
from spectrumlab.shapes.factories.retrieve_shape_from_spectrum import (
    FIGURES,
)
from spectrumlab.spectra import Spectrum

LOGGER = logging.getLogger('plugin-peak-shape')


def progress_wrapper(func: Callable):

    @wraps(func)
    def wrapper(*args, spectra: Mapping[int, Spectrum], **kwargs):

        app = QtWidgets.QApplication.instance() or QtWidgets.QApplication()

        window = ObservabilityWindow(
            n_tabs=len(spectra),
        )
        window.show()

        FIGURES.set(window.figures)

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
            app.exec()
            return result
        finally:
            app.quit()

    return wrapper
