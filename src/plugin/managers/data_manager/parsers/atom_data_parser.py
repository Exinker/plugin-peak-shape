import logging

from plugin.dto import AtomData, AtomFilepath
from plugin.managers.data_manager.exceptions import (
    LoadDataXMLError,
    ParseDataXMLError,
    ParseMetaXMLError,
    ParseSpectraXMLError,
)
from plugin.managers.data_manager.parsers.atom_meta_parser import AtomMetaParser
from plugin.managers.data_manager.parsers.atom_spectra_parser import AtomSpectraParser
from plugin.managers.data_manager.parsers.utils import load_xml
from plugin.types import XML


LOGGER = logging.getLogger('app')


class AtomDataParser:

    @classmethod
    def parse(cls, filepath: AtomFilepath) -> AtomData:

        LOGGER.debug('Load data from: %r', filepath)
        try:
            xml = load_xml(filepath)
        except LoadDataXMLError as error:
            LOGGER.error('%r', error)
            raise

        LOGGER.debug('Parse data from: %r', filepath)
        try:
            data = cls._parse(filepath, xml)
        except ParseDataXMLError as error:
            LOGGER.error('%r', error)
            raise

        LOGGER.debug('Data are parsed successfully!')
        return data

    @staticmethod
    def _parse(filepath: AtomFilepath, xml: XML) -> 'AtomData':

        try:
            meta = AtomMetaParser.parse(xml=xml)
        except Exception as error:
            raise ParseMetaXMLError from error

        try:
            spectra = AtomSpectraParser.from_xml(xml=xml)
        except Exception as error:
            raise ParseSpectraXMLError from error

        return AtomData(
            filepath=filepath,
            meta=meta,
            spectra=spectra,
        )
