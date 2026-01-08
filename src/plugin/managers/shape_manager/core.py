import logging
from collections.abc import Mapping
from multiprocessing import Pool, Queue

from plugin.presentation.callbacks import ProgressCallbackABC
from plugin.presentation.view_model import progress_setup
from plugin.presentation.view_model.shared_queue import init_pool
from spectrumlab.peaks.analyte_peaks.shapes.peak_shape import PeakShape
from spectrumlab.peaks.analyte_peaks.shapes.retrieve_shape import (
    RETRIEVE_SHAPE_CONFIG,
    retrieve_shape_from_spectrum,
)
from spectrumlab.peaks.blink_peaks.draft_blinks import draft_blinks
from spectrumlab.spectra import Spectrum


LOGGER = logging.getLogger('plugin-peak-shape')


@progress_setup
def retrieve_shape(__args) -> tuple[int, PeakShape]:
    n, spectrum = __args

    LOGGER.debug(
        'detector %02d - retrieve peak\'s shape',
        n+1,
    )
    try:
        peaks = draft_blinks(
            spectrum=spectrum,
        )
        shape = retrieve_shape_from_spectrum(
            spectrum=spectrum,
            peaks=peaks,
        )
        shape = PeakShape(
            width=shape.width,
            asymmetry=shape.asymmetry,
            ratio=(1 - shape.ratio),  # Atom's lagacy: never change it!
        )

    except Exception as error:
        LOGGER.warning(
            'detector %02d - shape is not retrieved: %r',
            n+1,
            error,
        )
        return RETRIEVE_SHAPE_CONFIG.default_shape

    LOGGER.info(
        'detector %02d - shape is retrieved: %s',
        n+1,
        shape,
    )
    return n, shape


def retrieve_shapes(
    n_workers: int,
    spectra: Mapping[int, Spectrum],
    progress_callback: ProgressCallbackABC,
    progress_queue: Queue,
) -> Mapping[int, PeakShape]:

    if n_workers > 1:
        return retrieve_shapes_multiprocess(
            n_workers=n_workers,
            spectra=spectra,
            progress_callback=progress_callback,
            progress_queue=progress_queue,
        )

    shapes = {}
    for n, spectrum in spectra.items():
        n, shape = retrieve_shape((n, spectrum, progress_queue))

        shapes[n] = shape
        progress_callback(n=n)

    return shapes


def retrieve_shapes_multiprocess(
    n_workers: int,
    spectra: Mapping[int, Spectrum],
    progress_callback: ProgressCallbackABC,
    progress_queue: Queue,
) -> Mapping[int, PeakShape]:

    shapes = {}
    with Pool(n_workers, initializer=init_pool, initargs=(progress_queue,)) as pool:
        for n, shape in pool.imap_unordered(
            retrieve_shape,
            [
                (n, spectrum)
                for n, spectrum in spectra.items()
            ],
        ):
            shapes[n] = shape
            progress_callback(n=n)

    return shapes
