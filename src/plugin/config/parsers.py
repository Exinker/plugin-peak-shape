import logging
import multiprocessing
import os

from spectrumlab.peaks.shape import Shape


LOGGER = logging.getLogger('app')


def parse_default_shape() -> Shape:
    default_shape = Shape(width=2, asymmetry=0, ratio=.1)

    shape = os.getenv('DEFAULT_SHAPE')
    if shape is None:
        return default_shape

    try:
        width, asymmetry, ratio = map(float, shape.split(','))
        shape = Shape(width=width, asymmetry=asymmetry, ratio=ratio)
    except Exception:
        LOGGER.warning(
            'Parse `DEFAULT_SHAPE` is failed!',
        )
        return default_shape
    return shape


def parse_max_workers() -> int:
    default_max_workers = multiprocessing.cpu_count()

    max_workers = os.getenv('MAX_WORKERS')
    if max_workers is None:
        return default_max_workers

    try:
        max_workers = int(max_workers)
    except Exception:
        LOGGER.warning(
            'Parse `MAX_WORKERS` is failed!',
        )
        return default_max_workers
    return max_workers


def parse_quiet() -> bool:
    default_quiet = False

    quiet = os.getenv('QUIET')
    if quiet is None:
        return default_quiet

    try:
        quiet = quiet == 'True'
    except Exception:
        LOGGER.warning(
            'Parse `QUIET` is failed!',
        )
        return default_quiet
    return quiet
