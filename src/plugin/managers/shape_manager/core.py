import logging
from collections.abc import Mapping
from multiprocessing import Pool

from plugin.presentation.callbacks import AbstractProgressCallback
from spectrumlab.peaks import (
    draft_peaks,
)
from spectrumlab.shapes import (
    Shape,
    retrieve_shape_from_spectrum,
)
from spectrumlab.spectra import Spectrum

LOGGER = logging.getLogger('plugin-peak-shape')


def restore_shape(__args) -> Shape:
    n, spectrum  = __args

    LOGGER.debug(
        'detector %02d - restore peak\'s shape',
        n,
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

    except ValueError as error:
        LOGGER.warning(
            'detector %02d - shape is not restored: %r',
            n,
            error,
        )
        LOGGER.debug(
            'detector %02d - default shape is used: %r',
            n,
            restore_shape_config.default_shape,
        )
        return restore_shape_config.default_shape

    LOGGER.debug(
        'Restored peak\'s shape for detector %d: %s',
        n,
        shape,
    )
    return shape


def restore_shapes(
    n_workers: int,
    spectra: Mapping[int, Spectrum],
    progress_callback: AbstractProgressCallback,
) -> Mapping[int, Shape]:

    if n_workers > 1:
        return restore_shapes_multiprocess(
            n_workers=n_workers,
            spectra=spectra,
            progress_callback=progress_callback,
        )

    shapes = {}
    for n, spectrum in spectra.items():
        shape = restore_shape((n, spectrum))

        progress_callback(
            n=n,
        )
        shapes[n] = shape

    return shapes


def restore_shapes_multiprocess(
    n_workers: int,
    spectra: Mapping[int, Spectrum],
    progress_callback: AbstractProgressCallback,
) -> Mapping[int, Shape]:

    shapes = {}
    with Pool(n_workers) as pool:
        for n, shape in enumerate(pool.imap(
            restore_shape,
            [
                (n, spectrum)
                for n, spectrum in spectra.items()
            ],
        )):
            shapes[n] = shape

            progress_callback(
                n=len(shapes)
            )

    return shapes
