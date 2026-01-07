"""Atom plugin to retrieve peak's shape."""

from datetime import datetime

import pkg_resources

from .plugin import Plugin


distribution = pkg_resources.get_distribution('peak_shape_plugin')
__name__ = 'peak-shape-plugin'
__version__ = distribution.version
__author__ = 'Pavel Vaschenko'
__email__ = 'vaschenko@vmk.ru'
__organization__ = 'VMK-Optoelektronika'
__license__ = 'MIT'
__copyright__ = 'Copyright {}, {}'.format(datetime.now().year, __organization__)

__all__ = [
    Plugin,
]
