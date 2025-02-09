import os
from pathlib import Path

import dotenv

from plugin.config.parsers import (
    parse_default_shape,
    parse_max_workers,
    parse_quiet,
)


dotenv.load_dotenv(Path(__file__).parents[3] / '.env', verbose=True)


LOGGING_LEVEL = os.getenv('LOGGING_LEVEL') or 'INFO'
DEFAULT_SHAPE = parse_default_shape()
MAX_WORKERS = parse_max_workers()
QUIET = parse_quiet()
