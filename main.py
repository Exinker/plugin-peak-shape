import logging
import os
import sys

root, _ = os.path.split(__file__)
sys.path.extend([
    os.path.join(root, r'.venv'),
    os.path.join(root, r'.venv\Lib\site-packages'),
    os.path.join(root, r'src'),
])

from plugin.config import DEFAULT_SHAPE, LOGGING_LEVEL, MAX_WORKERS, QUIET
from plugin.interfaces.callbacks import AbstractCallback, NullCallback
from plugin.interfaces.gui import observe
from plugin.loggers import *
from plugin.managers.data_manager import DataManager, DataManagerError
from plugin.managers.report_manager import ReportManager, ReportManagerError
from plugin.managers.shape_manager import ShapeManager, ShapeManagerError
from plugin.types import XML


LOGGER = logging.getLogger('app')
LOGGER.info('DEFAULT_SHAPE: %s', DEFAULT_SHAPE)
LOGGER.info('LOGGING_LEVEL: %s', LOGGING_LEVEL)
LOGGER.info('MAX_WORKERS: %s', MAX_WORKERS)
LOGGER.info('QUIET: %s', QUIET)


def process_xml(config_xml: XML) -> str:

    @observe(quiet=QUIET)
    def wrapped(
        config_xml: XML,
        callback: AbstractCallback | None,
    ) -> str:
        callback = callback or NullCallback()

        try:
            data_manager = DataManager(
                xml=config_xml,
                callback=callback,
            )
            try:
                data = data_manager.parse()
            except DataManagerError:
                return ReportManager.default()

            shape_manager = ShapeManager(
                default_shape=DEFAULT_SHAPE,
                max_workers=MAX_WORKERS,
                callback=callback,
            )
            try:
                shapes = shape_manager.restore(
                    spectra=data.spectra,
                )
            except ShapeManagerError:
                return ReportManager.default()

            report_manager = ReportManager(
                default_shape=DEFAULT_SHAPE,
            )
            try:
                report = report_manager.build(
                    shapes=shapes,
                    dump=True,
                )
            except ReportManagerError:
                return ReportManager.default()

            return report
        finally:
            LOGGER.info('Restoring shapes are completed!')

    return wrapped(config_xml=config_xml)


if __name__ == '__main__':
    result = process_xml(
        config_xml=r'<input>C:\Atom x64 3.3 (2024.03.02)\Temp\py_spe.xml</input>',
    )
    print(result)
