import logging
from collections.abc import Mapping, Sequence

from matplotlib.figure import Figure

from plugin.api.callbacks import AbstractProgressCallback
from spectrumlab.emulations.noise import Noise
from spectrumlab.peaks.shape import Shape, restore_shape_from_spectrum
from spectrumlab.spectra import Spectrum

LOGGER = logging.getLogger('plugin-peak-shape')


def restore_shape(
    __args: tuple[int, Spectrum, Shape, Mapping[str, Figure]],
) -> Shape:
    n, spectrum, default_shape, figures = __args

    LOGGER.debug(
        'detector %02d - restore peak\'s shape',
        n,
    )
    try:
        shape = restore_shape_from_spectrum(
            spectrum=spectrum,
            noise=Noise(
                detector=spectrum.detector,
                n_frames=1,  # TODO: read from xml!
            ),
            figures=figures,
        )
        shape = Shape(
            width=shape.width,
            asymmetry=shape.asymmetry,
            ratio=(1 - shape.ratio),
        )  # FIXME: remove Atom's lagacy (never change it!)

    except ValueError as error:
        LOGGER.warning(
            'detector %02d - shape is not restored: %r',
            n,
            error,
        )
        LOGGER.debug(
            'detector %02d - default shape is used: %r',
            n,
            default_shape,
        )
        return default_shape

    LOGGER.debug(
        'Restored peak\'s shape for detector %d: %s',
        n,
        shape,
    )
    return shape


def restore_shapes(
    spectra: Sequence[Spectrum],
    default_shape: Shape,
    n_workers: int,
    progress_callback: AbstractProgressCallback,
    figures: Sequence[Mapping[str, Figure]],
) -> tuple[Shape]:
    assert n_workers == 1, 'Multiprocessing is not supported yet!'

    shapes = []
    for n, spectrum in enumerate(spectra):
        shape = restore_shape((n, spectrum, default_shape, figures[n]))

        progress_callback(n=n)
        shapes.append(shape)

    return tuple(shapes)
