from collections.abc import Mapping, Sequence
from typing import Any, NewType

from spectrumlab.peaks.shape import Shape


T = NewType('T', Mapping[str, Any])


class ReportManager:

    def __init__(
        self,
        default_shape: Shape,
    ):
        self.default_shape = default_shape

    def build(
        self,
        shapes: Sequence[Shape],
        dump: bool = False,
    ) -> 'ReportManager':

        results = []
        for i, shape in enumerate(shapes):
            is_default = shape == self.default_shape

            result = dict(
                index=i,
                result=not is_default,
                width=shape.width,
                asymmetry=shape.asymmetry,
                ratio=shape.ratio,
            )
            results.append(result)

        report = '{prefix}<shapes>{results}</shapes>'.format(
            prefix='<?xml version="1.0" encoding="UTF-8"?>',
            results=wrap(results),
        )

        if dump:
            self.dump(
                report=report,
            )

        return report

    @staticmethod
    def dump(
        report: str,
        filename: str | None = None,
    ) -> None:
        filename = filename or 'results'

        filepath = f'./{filename}.xml'
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
