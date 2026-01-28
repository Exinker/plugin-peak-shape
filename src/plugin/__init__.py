"""Atom plugin to retrieve peak's shape."""

from datetime import datetime
from importlib.metadata import version


from .plugin import Plugin


__name__ = 'peak-shape-plugin'
__version__ = version('plugin')
__author__ = 'Pavel Vaschenko'
__email__ = 'vaschenko@vmk.ru'
__organization__ = 'VMK-Optoelektronika'
__license__ = 'MIT'
__copyright__ = 'Copyright {}, {}'.format(datetime.now().year, __organization__)

__all__ = [
    Plugin,
]
