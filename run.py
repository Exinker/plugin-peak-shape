import logging
from argparse import ArgumentParser

import plugin
from plugin import Plugin
from plugin.config import PLUGIN_CONFIG
from plugin.loggers import *
from plugin.types import XML
from spectrumlab.peaks.analyte_peaks.shapes.retrieve_shape import RETRIEVE_SHAPE_CONFIG
from spectrumlab.peaks.blink_peaks.draft_blinks import DRAFT_BLINKS_CONFIG


LOGGER = logging.getLogger('plugin-peak-shape')
PLUGIN = Plugin.create()


def process_xml(config_xml: XML) -> str:

    LOGGER.info('run %r', plugin.__name__)
    LOGGER.info('DRAFT_BLINKS_CONFIG: %s', DRAFT_BLINKS_CONFIG)
    LOGGER.info('PLUGIN_CONFIG: %s', PLUGIN_CONFIG)
    LOGGER.info('RETRIEVE_SHAPE_CONFIG: %s', RETRIEVE_SHAPE_CONFIG)

    return PLUGIN.run(config_xml)


if __name__ == '__main__':

    parser = ArgumentParser()
    parser.add_argument(
        '--config',
        help='XML with config',
        default=r'<input>C:\Atom x64 3.3 (2025.11.15)\Temp\py_spe.xml</input>',
    )
    args = parser.parse_args()

    result = process_xml(
        config_xml=args.config,
    )
    print(result)
