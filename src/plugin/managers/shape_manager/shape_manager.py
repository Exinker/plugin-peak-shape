import logging
import time
from collections.abc import Sequence

from plugin.interfaces.callbacks import AbstractProgressCallback
from plugin.managers.shape_manager.core import restore_shapes
from spectrumlab.peaks.shape import Shape
from spectrumlab.spectra import Spectrum

LOGGER = logging.getLogger('plugin-peak-shape')


class ShapeManager:

    def __init__(
        self,
        default_shape: Shape,
        max_workers: int,
    ) -> None:
        self.default_shape = default_shape
        self.max_workers = max_workers

    def restore(
        self,
        spectra: Sequence[Spectrum],
        progress_callback: AbstractProgressCallback,
    ):
        started_at = time.perf_counter()

        LOGGER.debug(
            'Start to restoring %s shapes...',
            len(spectra),
        )
        try:
            shapes = restore_shapes(
                spectra=spectra,
                default_shape=self.default_shape,
                n_workers=self.max_workers,
                callback=progress_callback,
            )
            return shapes
        finally:
            if LOGGER.isEnabledFor(logging.INFO):
                LOGGER.info(
                    'Time elapsed for shapes restoring: {elapsed:.4f}, s'.format(
                        elapsed=time.perf_counter() - started_at,
                    ),
                )
