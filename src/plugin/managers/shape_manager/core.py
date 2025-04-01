import logging
from collections.abc import Mapping
from multiprocessing import Pool

from plugin.presentation.callbacks import AbstractProgressCallback
from spectrumlab.peaks import (
    draft_peaks,
)
from spectrumlab.shapes import (
    Shape,
    retrieve_shape_from_spectrum, RETRIEVE_SHAPE_CONFIG,
)
from spectrumlab.spectra import Spectrum

LOGGER = logging.getLogger('plugin-peak-shape')


def retrieve_shape(__args) -> Shape:
    n, spectrum  = __args

    LOGGER.debug(
        'detector %02d - retrieve peak\'s shape',
        n+1,
    )
    try:
        peaks = draft_peaks(
            spectrum=spectrum,
        )
        shape = retrieve_shape_from_spectrum(
            spectrum=spectrum,
            peaks=peaks,
            n=n,
        )

        # FIXME: Atom's lagacy (never change it!)
        shape = Shape(
            width=shape.width,
            asymmetry=shape.asymmetry,
            ratio=(1 - shape.ratio),
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
    return shape


def retrieve_shapes(
    n_workers: int,
    spectra: Mapping[int, Spectrum],
    progress_callback: AbstractProgressCallback,
) -> Mapping[int, Shape]:

    if n_workers > 1:
        return retrieve_shapes_multiprocess(
            n_workers=n_workers,
            spectra=spectra,
            progress_callback=progress_callback,
        )

    shapes = {}
    for n, spectrum in spectra.items():
        shape = retrieve_shape((n, spectrum))

        shapes[n] = shape
        progress_callback(n=n)

    return shapes


def retrieve_shapes_multiprocess(
    n_workers: int,
    spectra: Mapping[int, Spectrum],
    progress_callback: AbstractProgressCallback,
) -> Mapping[int, Shape]:

    shapes = {}
    with Pool(n_workers) as pool:
        for n, shape in enumerate(pool.imap(
            retrieve_shape,
            [
                (n, spectrum)
                for n, spectrum in spectra.items()
            ],
        )):
            shapes[n] = shape
            progress_callback(n=n)

    return shapes
