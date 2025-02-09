import logging
import os
import sys
root, _ = os.path.split(__file__)
sys.path.extend([
    os.path.join(root, r'.venv'),
    os.path.join(root, r'.venv\Lib\site-packages'),
])

from PySide6 import QtWidgets

from plugin.config.config import DEFAULT_SHAPE, MAX_WORKERS, QUIET
from plugin.interfaces.callbacks import NullCallback
# from plugin.interfaces.gui import observe
from plugin.interfaces.gui.windows import ProgressWindow
from plugin.loggers import *
from plugin.managers.data_manager import DataManager, DataManagerError
from plugin.managers.report_manager import ReportManager, ReportManagerError
from plugin.managers.shape_manager import ShapeManager, ShapeManagerError
from plugin.types import XML


LOGGER = logging.getLogger('app')


try:
    app = QtWidgets.QApplication()
    window = ProgressWindow()
    window.show()
    CALLBACK = window.update
except Exception as error:
    LOGGER.warning(
        'GUI initialization is failed: %s',
        repr(error),
    )
    CALLBACK = NullCallback()
else:
    LOGGER.debug(
        'GUI is initializated',
    )


# @observe(quiet=QUIET)  # FIXME: не подгружается переменная
def process_xml(config_xml: XML) -> str:  # TODO: добавить в сигнатуру передачу переменной `callback`;

    try:
        data_manager = DataManager(
            xml=config_xml,
            callback=CALLBACK,
        )
        try:
            data = data_manager.parse()
        except DataManagerError:
            return ''

        shape_manager = ShapeManager(
            default_shape=DEFAULT_SHAPE,
            max_workers=MAX_WORKERS,
            callback=CALLBACK,
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
    finally:
        app = QtWidgets.QApplication.instance()
        if app:
            app.quit()


if __name__ == '__main__':
    result = process_xml(
        config_xml=r'<input>C:\Atom x64 3.3 (2024.03.02)\Temp\py_spe.xml</input>',
    )
    print(result)
