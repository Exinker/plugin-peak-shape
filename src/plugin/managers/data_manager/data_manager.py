import logging
import time

from plugin.dto import AtomData
from plugin.interfaces.callbacks import AbstractCallback
from plugin.managers.data_manager.exceptions import (
    LoadDataXMLError,
    ParseDataXMLError,
    ParseFilepathXMLError,
)
from plugin.managers.data_manager.parsers import (
    AtomDataParser,
    FilepathParser,
)
from plugin.types import XML


LOGGER = logging.getLogger('app')


class DataManager:

    def __init__(
        self,
        xml: XML,
        callback: AbstractCallback,
    ) -> None:
        self.xml = xml
        self.callback = callback

    def parse(self) -> AtomData:
        n, total = 0, 2
        self.callback(
            progress=100 * n / total,
            info='<strong>PLEASE, WAIT!</strong>',
            message='DATA PARSING: {n}/{total} is complited!'.format(
                n=n,
                total=total,
            ),
        )

        started_at = time.perf_counter()
        try:
            filepath = FilepathParser.parse(self.xml)
        except ParseFilepathXMLError as error:
            LOGGER.error('%r', error)
            raise
        else:
            LOGGER.info('Filepath to data: %r', filepath)
        finally:
            if LOGGER.isEnabledFor(logging.INFO):
                LOGGER.info(
                    'Time elapsed for filepath parsing: {elapsed:.4f}, s'.format(
                        elapsed=time.perf_counter() - started_at,
                    ),
                )

        n, total = 1, 2
        self.callback(
            progress=100 * n / total,
            info='<strong>PLEASE, WAIT!</strong>',
            message='DATA PARSING: {n}/{total} is complited!'.format(
                n=n,
                total=total,
            ),
        )
        started_at = time.perf_counter()
        try:
            data = AtomDataParser.parse(filepath)
            return data
        except (LoadDataXMLError, ParseDataXMLError):
            return ''
        finally:
            if LOGGER.isEnabledFor(logging.INFO):
                LOGGER.info(
                    'Time elapsed for data parsing: {elapsed:.4f}, s'.format(
                        elapsed=time.perf_counter() - started_at,
                    ),
                )

            n, total = 2, 2
            self.callback(
                progress=100 * n / total,
                info='<strong>PLEASE, WAIT!</strong>',
                message='DATA PARSING: {n}/{total} is complited!'.format(
                    n=n,
                    total=total,
                ),
            )
