import logging
from collections.abc import Sequence
from multiprocessing import Pool

from spectrumlab.noise import Noise
from spectrumlab.peak.shape import Shape, restore_shape_from_spectrum
from spectrumlab.spectrum import Spectrum

from src.interfaces.callbacks import AbstractCallback


LOGGER = logging.getLogger('app')


def restore_shape(__args: tuple[int, Spectrum, Shape]) -> Shape:
    n, spectrum, default_shape = __args

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
    callback: AbstractCallback,
) -> tuple[Shape]:
    n_shapes = len(spectra)

    n, total = 1, n_shapes
    callback(
        progress=100*n/total,
        info='<strong>PLEASE, WAIT!</strong>',
        message='SHAPE ESTIMATION: {n}/{total} is complited!'.format(
            n=n,
            total=total,
        ),
    )

    shapes = []
    with Pool(n_workers) as pool:
        for shape in pool.imap(
            restore_shape,
            [
                (n, spectrum, default_shape)
                for n, spectrum in enumerate(spectra)
            ],
        ):  # TODO: проверить в тестах, что очередь сохраняется!
            shapes.append(shape)

            n, total = len(shapes), n_shapes
            callback(
                progress=100*n/total,
                info='<strong>PLEASE, WAIT!</strong>',
                message='SHAPE ESTIMATION: {n}/{total} is complited!'.format(
                    n=n,
                    total=total,
                ),
            )

    return tuple(shapes)
