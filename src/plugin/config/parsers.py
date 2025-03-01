import logging
import multiprocessing
import os

from spectrumlab.peaks.shape import Shape

LOGGER = logging.getLogger('plugin-peak-shape')

DEFAULT_MAX_WORKERS = 1 or multiprocessing.cpu_count()  # FIXME: change to `multiprocessing.cpu_count()`
DEFAULT_SHAPE = Shape(width=2, asymmetry=0, ratio=.1)
DEFAULT_QUIET = False


def parse_default_shape() -> Shape:

    shape = os.getenv('DEFAULT_SHAPE')
    if shape is None:
        return DEFAULT_SHAPE

    try:
        width, asymmetry, ratio = map(float, shape.split(','))
        shape = Shape(width=width, asymmetry=asymmetry, ratio=ratio)
    except Exception:
        LOGGER.warning(
            'Parse `DEFAULT_SHAPE` is failed!',
        )
        return DEFAULT_SHAPE
    return shape


def parse_max_workers() -> int:

    max_workers = os.getenv('MAX_WORKERS')
    if max_workers is None:
        return DEFAULT_MAX_WORKERS

    try:
        max_workers = int(max_workers)
    except Exception:
        LOGGER.warning(
            'Parse `MAX_WORKERS` is failed!',
        )
        return DEFAULT_MAX_WORKERS
    return max_workers


def parse_quiet() -> bool:

    quiet = os.getenv('QUIET')
    if quiet is None:
        return DEFAULT_QUIET

    try:
        quiet = quiet.lower() == 'true'
    except Exception:
        LOGGER.warning(
            'Parse `QUIET` is failed!',
        )
        return DEFAULT_QUIET
    return quiet
