import logging
import time
from collections.abc import Mapping, Sequence

from matplotlib.figure import Figure

from plugin.api.callbacks import AbstractProgressCallback, NullProgressCallback
from plugin.api.view import progress_wrapper
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

    @progress_wrapper
    def restore(
        self,
        spectra: Sequence[Spectrum],
        progress_callback: AbstractProgressCallback | None = None,
        figures: Sequence[Mapping[str, Figure]] | None = None,
    ):
        progress_callback = progress_callback or NullProgressCallback()
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
                progress_callback=progress_callback,
                figures=figures,
            )
            return shapes
        finally:
            if LOGGER.isEnabledFor(logging.INFO):
                LOGGER.info(
                    'Time elapsed for shapes restoring: {elapsed:.4f}, s'.format(
                        elapsed=time.perf_counter() - started_at,
                    ),
                )
