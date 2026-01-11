from collections.abc import Mapping, Sequence
from typing import Any, NewType

from plugin.config import PluginConfig
from spectrumlab.peaks.analyte_peaks.shapes import PeakShape
from spectrumlab.peaks.analyte_peaks.shapes.retrieve_shape import RETRIEVE_SHAPE_CONFIG

T = NewType('T', Mapping[str, Any])


REPORT_PREFIX = '<?xml version="1.0" encoding="UTF-8"?>'


class ReportManager:

    def __init__(
        self,
        plugin_config: PluginConfig,
    ) -> None:

        self.plugin_config = plugin_config

    def build(
        self,
        shapes: Sequence[PeakShape],
        dump: bool = False,
    ) -> str:

        results = []
        for detector_id, shape in shapes.items():
            is_default = shape == RETRIEVE_SHAPE_CONFIG.default_shape

            result = dict(
                index=detector_id,
                result=not is_default,
                width=shape.width,
                asymmetry=shape.asymmetry,
                ratio=shape.ratio,
            )
            results.append(result)

        report = '{prefix}<shapes>{results}</shapes>'.format(
            prefix=REPORT_PREFIX,
            results=wrap(results),
        )

        if dump:
            self.dump(
                report=report,
            )

        return report

    @classmethod
    def default(cls) -> str:
        return '{prefix}{message}'.format(
            prefix=REPORT_PREFIX,
            message=wrap({'message': '\n'.join([
                'Restoring shapes is failed!',
                'Open `${ATOM_PATH}/Data/.log` to more information.',
            ])}),
        )

    def dump(
        self,
        report: str,
        filename: str | None = None,
    ) -> None:
        filename = filename or 'results'

        filepath = f'{filename}.xml'
        with open(filepath, 'w') as file:
            file.write(report)


def wrap(__object: T | Sequence[T]) -> str:
    xml = ''

    if isinstance(__object, Mapping):
        for key, value in __object.items():
            xml += f'<{key}>{value}</{key}>'

    if isinstance(__object, Sequence):
        for item in __object:
            xml += f'<shape>{wrap(item)}</shape>'

    return xml
