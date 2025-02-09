"""Atom plugin for peak's shape estimation."""

from datetime import datetime

import dotenv
import pkg_resources


distribution = pkg_resources.get_distribution('peak_shape_plugin')
__name__ = 'Peak Shape Plugin'
__version__ = distribution.version
__author__ = 'Pavel Vaschenko'
__email__ = 'vaschenko@vmk.ru'
__organization__ = 'VMK-Optoelektronika'
__license__ = 'MIT'
__copyright__ = 'Copyright {}, {}'.format(datetime.now().year, __organization__)
