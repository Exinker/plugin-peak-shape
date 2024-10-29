import logging
import time
from collections.abc import Sequence

from spectrumlab.peak.shape import Shape
from spectrumlab.spectrum import Spectrum

from src.interfaces.callbacks import AbstractCallback
from src.managers.shape_manager.core import restore_shapes


LOGGER = logging.getLogger('app')


class ShapeManager:

    def __init__(
        self,
        default_shape: Shape,
        max_workers: int,
        callback: AbstractCallback,
    ) -> None:
        self.default_shape = default_shape
        self.max_workers = max_workers
        self.pbar = callback

    def restore(
        self,
        spectra: Sequence[Spectrum],
    ):
        started_at = time.perf_counter()

        try:
            shapes = restore_shapes(
                spectra=spectra,
                default_shape=self.default_shape,
                n_workers=self.max_workers,
                callback=self.pbar,
            )
            return shapes
        finally:
            if LOGGER.isEnabledFor(logging.INFO):
                LOGGER.info(
                    'Time elapsed for shapes restoring: {elapsed:.4f}, s'.format(
                        elapsed=time.perf_counter() - started_at,
                    ),
                )
