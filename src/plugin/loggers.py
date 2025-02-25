import logging
import logging.config

from plugin.config import LOGGING_LEVEL, PLUGIN_PATH


def setdefault_logger():
    config = dict(
        version=1,
        disable_existing_loggers=False,

        formatters=dict(
            formatter={
                'datefmt': '%Y-%m-%d %H:%M:%S',
                'format': '[%(asctime)s.%(msecs)04d] %(levelname)-8s - %(message)s',
            },
        ),

        handlers=dict(
            stream_handler={
                'class': 'logging.StreamHandler',
                'level': logging.DEBUG,
                'formatter': 'formatter',
            },
            file_handler={
                'class': 'logging.FileHandler',
                'level': LOGGING_LEVEL,
                'filename': PLUGIN_PATH / '.log',
                'mode': 'a',
                'formatter': 'formatter',
                'encoding': 'utf-8',
            },
        ),

        loggers=dict(
            app={
                'level': LOGGING_LEVEL,
                'handlers': ['file_handler', 'stream_handler'],
                'propagate': False,
            },
        ),
    )

    logging.config.dictConfig(config)


setdefault_logger()
