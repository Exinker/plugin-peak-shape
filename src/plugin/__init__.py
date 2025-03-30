"""Atom plugin to retrieve peak's shape."""

import os
from datetime import datetime
from pathlib import Path

import pkg_resources

from .plugin import plugin_factory


root = Path(__file__).parents[2].resolve()
os.chdir(root)


distribution = pkg_resources.get_distribution('peak_shape_plugin')
__name__ = 'peak-shape-plugin'
__version__ = distribution.version
__author__ = 'Pavel Vaschenko'
__email__ = 'vaschenko@vmk.ru'
__organization__ = 'VMK-Optoelektronika'
__license__ = 'MIT'
__copyright__ = 'Copyright {}, {}'.format(datetime.now().year, __organization__)

__all__ = [
    plugin_factory,
]
