import logging

import plugin
from plugin.config import (
    DEFAULT_SHAPE,
    LOGGING_LEVEL,
    MAX_WORKERS,
    QUIET,
)

LOGGER = logging.getLogger('plugin-peak-shape')
PLUGIN = plugin.plugin_factory()


LOGGER.info('run %r', plugin.__name__)
LOGGER.info('DEFAULT_SHAPE: %s', DEFAULT_SHAPE)
LOGGER.info('LOGGING_LEVEL: %s', LOGGING_LEVEL)
LOGGER.info('MAX_WORKERS: %s', MAX_WORKERS)
LOGGER.info('QUIET: %s', QUIET)


def run(config_xml: str) -> str:

    result = PLUGIN.run(config_xml)
    return result


if __name__ == '__main__':
    result = run(
        config_xml=r'<input>C:\Atom x64 3.3 (2025.02.20)\Temp\py_spe.xml</input>',
    )
    print(result)
