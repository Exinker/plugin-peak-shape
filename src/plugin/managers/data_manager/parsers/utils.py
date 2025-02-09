import xml.etree.ElementTree as ElementTree

from plugin.dto import AtomFilepath
from plugin.managers.data_manager.exceptions import LoadDataXMLError
from plugin.types import XML


def load_xml(__filepath: AtomFilepath) -> XML | None:
    """Load `xml` element object from file for a given `filepath`."""

    try:
        tree = ElementTree.parse(__filepath)
    except FileNotFoundError as error:
        raise LoadDataXMLError('File not found: {!r}!'.format(__filepath)) from error

    xml = tree.getroot()
    return xml
