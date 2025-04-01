from plugin.config import (
    PLUGIN_CONFIG,
)
from plugin.exceptions import exception_wrapper
from plugin.managers.data_manager import DataManager
from plugin.managers.report_manager import ReportManager
from plugin.managers.shape_manager import ShapeManager
from plugin.types import XML


def plugin_factory() -> 'Plugin':

    data_manager = DataManager()
    shape_manager = ShapeManager(
        plugin_config=PLUGIN_CONFIG,
    )
    report_manager = ReportManager(
        plugin_config=PLUGIN_CONFIG,
    )

    return Plugin(
        data_manager=data_manager,
        shape_manager=shape_manager,
        report_manager=report_manager,
    )


class Plugin:

    create = plugin_factory

    def __init__(
        self,
        data_manager: DataManager,
        shape_manager: ShapeManager,
        report_manager: ReportManager,
    ) -> None:

        self.data_manager = data_manager
        self.shape_manager = shape_manager
        self.report_manager = report_manager

    @exception_wrapper
    def run(
        self,
        xml: XML,
    ) -> str:

        data = self.data_manager.parse(
            xml=xml,
        )
        shapes = self.shape_manager.retrieve(
            spectra=data.spectra,
        )
        report = self.report_manager.build(
            shapes=shapes,
            dump=True,
        )

        return report
