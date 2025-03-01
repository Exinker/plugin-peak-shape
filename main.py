import logging
import sys
from pathlib import Path

root = Path(__file__).parent.resolve()
sys.path.extend([
    str(root / '.venv'),
    str(root / '.venv\Lib\site-packages'),
    str(root / 'src'),
])

import plugin
from plugin.config import DEFAULT_SHAPE, LOGGING_LEVEL, MAX_WORKERS, QUIET
from plugin.loggers import *
from plugin.types import XML

LOGGER = logging.getLogger('plugin-peak-shape')
PLUGIN = plugin.plugin_factory()


def process_xml(config_xml: XML) -> str:

    LOGGER.info('run %r', plugin.__name__)
    LOGGER.info('DEFAULT_SHAPE: %s', DEFAULT_SHAPE)
    LOGGER.info('LOGGING_LEVEL: %s', LOGGING_LEVEL)
    LOGGER.info('MAX_WORKERS: %s', MAX_WORKERS)
    LOGGER.info('QUIET: %s', QUIET)

    return PLUGIN.run(config_xml)


if __name__ == '__main__':
    result = process_xml(
        config_xml=r'<input>C:\Atom x64 3.3 (2025.02.20)\Temp\py_spe.xml</input>',
    )
    print(result)
