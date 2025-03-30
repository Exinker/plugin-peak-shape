import logging
import os
import sys
from pathlib import Path


root = Path(__file__).parent.resolve()
os.chdir(root)
sys.path.extend([
    str(root / '.venv'),
    str(root / '.venv\Lib\site-packages'),
    str(root / 'src'),
])

import plugin
from plugin.config import (
    DRAFT_PEAK_CONFIG,
    PLUGIN_CONFIG,
    RETRIEVE_SHAPE_CONFIG,
)
from plugin.loggers import *
from plugin.types import XML

LOGGER = logging.getLogger('plugin-peak-shape')
PLUGIN = plugin.plugin_factory()


def process_xml(config_xml: XML) -> str:

    LOGGER.info('run %r', plugin.__name__)
    LOGGER.info('DRAFT_PEAK_CONFIG: %s', DRAFT_PEAK_CONFIG)
    LOGGER.info('PLUGIN_CONFIG: %s', PLUGIN_CONFIG)
    LOGGER.info('RETRIEVE_SHAPE_CONFIG: %s', RETRIEVE_SHAPE_CONFIG)

    return PLUGIN.run(config_xml)


if __name__ == '__main__':
    result = process_xml(
        config_xml=r'<input>C:\Atom x64 3.3 (2025.03.18)\Temp\py_spe.xml</input>',
    )
    print(result)
