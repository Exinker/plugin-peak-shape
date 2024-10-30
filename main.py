import logging
import os
import sys
root, _ = os.path.split(__file__)
sys.path.extend([
    os.path.join(root, r'env'),
    os.path.join(root, r'env\Lib\site-packages'),
])

from src.config import DEFAULT_SHAPE, MAX_WORKERS, QUIET
from src.interfaces.callbacks import AbstractCallback, NullCallback
from src.interfaces.gui import observe
from src.logger import *
from src.managers.data_manager import DataManager, DataManagerError
from src.managers.report_manager import ReportManager, ReportManagerError
from src.managers.shape_manager import ShapeManager, ShapeManagerError
from src.types import XML


LOGGER = logging.getLogger('app')


@observe(quiet=False)  # FIXME: не подгружается переменная
def process_xml(
    config_xml: XML,
    callback: AbstractCallback | None = None,
) -> str:
    callback = callback or NullCallback()

    data_manager = DataManager(
        xml=config_xml,
        callback=callback,
    )
    try:
        data = data_manager.parse()
    except DataManagerError:
        return ''

    shape_manager = ShapeManager(
        default_shape=DEFAULT_SHAPE,
        max_workers=MAX_WORKERS,
        callback=callback,
    )
    try:
        shapes = shape_manager.restore(
            spectra=data.spectra,
        )
    except ShapeManagerError:
        return ''

    report_manager = ReportManager(
        default_shape=DEFAULT_SHAPE,
    )
    try:
        report = report_manager.build(
            shapes=shapes,
            dump=True,
        )
    except ReportManagerError:
        return ''

    return report


if __name__ == '__main__':
    result = process_xml(
        config_xml=r'<input>C:\Atom x64 3.3 (2024.03.02)\Temp\py_spe.xml</input>',
    )
    print(result)
