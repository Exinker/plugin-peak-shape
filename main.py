import logging
import sys
from functools import wraps
from pathlib import Path

root = Path(__file__).parent.resolve()
sys.path.extend([
    str(root / '.venv'),
    str(root / '.venv\Lib\site-packages'),
    str(root / 'src'),
])

from plugin.config import DEFAULT_SHAPE, LOGGING_LEVEL, MAX_WORKERS, QUIET
from plugin.interfaces.callbacks import AbstractCallback, NullCallback
from plugin.interfaces.gui import progress_wrapper
from plugin.loggers import *
from plugin.managers.data_manager import DataManager
from plugin.managers.report_manager import ReportManager
from plugin.managers.shape_manager import ShapeManager
from plugin.types import XML


LOGGER = logging.getLogger('app')
LOGGER.info('DEFAULT_SHAPE: %s', DEFAULT_SHAPE)
LOGGER.info('LOGGING_LEVEL: %s', LOGGING_LEVEL)
LOGGER.info('MAX_WORKERS: %s', MAX_WORKERS)
LOGGER.info('QUIET: %s', QUIET)


def get_initial_exception(error: Exception) -> Exception:

    parent = error.__cause__ or error.__context__
    if parent is None:
        return error

    return get_initial_exception(parent)


def exception_wrapper(func):

    @wraps(func)
    def wrapped(*args, **kwargs):

        try:
            result = func(*args, **kwargs)

        except Exception as error:
            LOGGER.error('Restoring shapes ware not completed successfully!')
            raise get_initial_exception(error)

        else:
            LOGGER.info('Restoring shapes are completed!')
            return result

    return wrapped


def process_xml(config_xml: XML) -> str:

    @exception_wrapper
    @progress_wrapper(quiet=QUIET)
    def wrapped(
        config_xml: XML,
        callback: AbstractCallback | None,
    ) -> str:
        callback = callback or NullCallback()

        data_manager = DataManager(
            xml=config_xml,
        )
        data = data_manager.parse()

        shape_manager = ShapeManager(
            default_shape=DEFAULT_SHAPE,
            max_workers=MAX_WORKERS,
            callback=callback,
        )
        shapes = shape_manager.restore(
            spectra=data.spectra,
        )

        report_manager = ReportManager(
            default_shape=DEFAULT_SHAPE,
        )
        report = report_manager.build(
            shapes=shapes,
            dump=True,
        )

        return report

    return wrapped(config_xml=config_xml)


if __name__ == '__main__':
    result = process_xml(
        config_xml=r'<input>C:\Atom x64 3.3 (2025.02.20)\Temp\py_spe.xml</input>',
    )
    print(result)
