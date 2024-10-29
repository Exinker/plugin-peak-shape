import logging
import xml.etree.ElementTree as ET  # noqa: N817
from xml.etree.ElementTree import ParseError

from src.dto import AtomFilepath
from src.managers.data_manager.exceptions import (
    ParseFilepathXMLError,
)
from src.types import XML


LOGGER = logging.getLogger('app')


class FilepathParser:

    @classmethod
    def parse(cls, xml: XML) -> AtomFilepath:

        LOGGER.debug('Parse xml with filepath to data.')
        try:
            filepath = cls._parse(xml)
        except ParseFilepathXMLError as error:
            LOGGER.error('%r', error)
            raise

        LOGGER.debug(
            'Filepath to data: %r',
            filepath,
        )
        return filepath

    @staticmethod
    def _parse(xml: XML) -> AtomFilepath:

        try:
            filepath = ET.fromstring(xml).text
        except ParseError as error:
            raise ParseFilepathXMLError('Config xml is not parsed!') from error

        return AtomFilepath(filepath)
