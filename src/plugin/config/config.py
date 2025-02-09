import os

import dotenv

from plugin.config.parsers import (
    parse_default_shape,
    parse_max_workers,
    parse_quiet,
)


dotenv.load_dotenv(os.path.join('.', '.env'), verbose=True)


# ---------        ENV        ---------
LOGGING_LEVEL = os.getenv('LOGGING_LEVEL') or 'INFO'

MAX_WORKERS = parse_max_workers()
DEFAULT_SHAPE = parse_default_shape()

QUIET = parse_quiet()
