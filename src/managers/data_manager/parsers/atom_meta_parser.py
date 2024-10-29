import logging

from src.dto import AtomMeta
from src.types import XML


LOGGER = logging.getLogger('app')


class AtomMetaParser:

    @classmethod
    def parse(cls, xml: XML) -> AtomMeta:
        titul = xml.find('titul')

        return AtomMeta(
            organization_name=titul.find('organization').text,
            device_name=titul.find('device').text,
            user_name=titul.find('user').text,
            analysis_name=titul.find('aname').text,
        )
