import multiprocessing
import os

from dotenv import load_dotenv

from spectrumlab.peak.shape import Shape


load_dotenv(os.path.join('.', '.env'), verbose=True)


def parse_default_shape() -> Shape:
    default_shape = Shape(width=2, asymmetry=0, ratio=.1)

    shape = os.getenv('DEFAULT_SHAPE')
    if shape is None:
        return default_shape

    try:
        width, asymmetry, ratio = map(float, shape.split(','))
        shape = Shape(width=width, asymmetry=asymmetry, ratio=ratio)
    except Exception:
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
        return default_max_workers
    return max_workers


def parse_quiet() -> bool:
    default_quiet = False

    quiet = os.getenv('QUIET')
    if quiet is None:
        return default_quiet

    try:
        quiet = bool(quiet)
    except Exception:
        return default_quiet
    return quiet


LOGGING_LEVEL = os.getenv('LOGGING_LEVEL') or 'INFO'

MAX_WORKERS = parse_max_workers()
DEFAULT_SHAPE = parse_default_shape()
QUIET = parse_quiet()
