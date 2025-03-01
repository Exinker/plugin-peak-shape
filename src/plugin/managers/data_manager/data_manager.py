import logging
import time

from plugin.dto import AtomData
from plugin.managers.data_manager.exceptions import (
    DataManagerError,
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
    ) -> None:
        self.xml = xml

    def parse(self) -> AtomData:

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

        started_at = time.perf_counter()
        try:
            data = AtomDataParser.parse(filepath)
            return data
        except (LoadDataXMLError, ParseDataXMLError) as error:
            raise DataManagerError from error
        finally:
            if LOGGER.isEnabledFor(logging.INFO):
                LOGGER.info(
                    'Time elapsed for data parsing: {elapsed:.4f}, s'.format(
                        elapsed=time.perf_counter() - started_at,
                    ),
                )
