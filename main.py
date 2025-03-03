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
from plugin.config import CONFIG
from plugin.loggers import *
from plugin.types import XML

LOGGER = logging.getLogger('plugin-peak-shape')
PLUGIN = plugin.plugin_factory()


def process_xml(config_xml: XML) -> str:

    LOGGER.info('run %r', plugin.__name__)
    LOGGER.info('DEFAULT_SHAPE: %s', CONFIG.default_shape)
    LOGGER.info('LOGGING_LEVEL: %s', CONFIG.logging_level.value)
    LOGGER.info('MAX_WORKERS: %s', CONFIG.max_workers)

    return PLUGIN.run(config_xml)


if __name__ == '__main__':
    result = process_xml(
        config_xml=r'<input>C:\Atom x64 3.3 (2025.02.20)\Temp\py_spe.xml</input>',
    )
    print(result)
