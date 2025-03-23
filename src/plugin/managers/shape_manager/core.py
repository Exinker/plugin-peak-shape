import logging
from collections.abc import Mapping
from multiprocessing import Pool

from plugin.presentation.callbacks import AbstractProgressCallback
from spectrumlab.emulations.noise import Noise
from spectrumlab.peaks.shape import (
    DraftPeakConfig,
    RestoreShapeConfig,
    Shape,
    restore_shape_from_spectrum,
    FIGURES,
    FIGURE,
)
from spectrumlab.spectra import Spectrum

LOGGER = logging.getLogger('plugin-peak-shape')


def restore_shape(__args) -> Shape:
    n, spectrum, draft_peak_config, restore_shape_config = __args

    LOGGER.debug(
        'detector %02d - restore peak\'s shape',
        n,
    )
    try:
        FIGURE.set(FIGURES.get()[n])

        shape = restore_shape_from_spectrum(
            spectrum=spectrum,
            noise=Noise(
                detector=spectrum.detector,
                n_frames=15000,  # TODO: read from xml!
            ),
            draft_peak_config=DraftPeakConfig(**draft_peak_config.model_dump()),
            restore_shape_config=RestoreShapeConfig(**restore_shape_config.model_dump()),
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
    draft_peak_config,
    restore_shape_config,
) -> tuple[Shape]:

    if n_workers > 1:
        return restore_shapes_multiprocess(
            n_workers=n_workers,
            spectra=spectra,
            progress_callback=progress_callback,
            draft_peak_config=draft_peak_config,
            restore_shape_config=restore_shape_config,
        )

    shapes = {}
    for n, spectrum in spectra.items():
        shape = restore_shape((n, spectrum, draft_peak_config, restore_shape_config))

        progress_callback(
            n=n,
            total=len(spectra),
        )
        shapes[n] = shape

    return shapes


def restore_shapes_multiprocess(
    n_workers: int,
    spectra: Mapping[int, Spectrum],
    progress_callback: AbstractProgressCallback,
    draft_peak_config,
    restore_shape_config,
) -> tuple[Shape]:

    shapes = []
    with Pool(n_workers) as pool:
        for shape in pool.imap(
            restore_shape,
            [
                (n, spectrum, draft_peak_config, restore_shape_config)
                for n, spectrum in enumerate(spectra)
            ],
        ):
            shapes.append(shape)

            progress_callback(
                n=len(shapes),
                total=len(spectra),
            )
            shapes.append(shape)

    return tuple(shapes)
