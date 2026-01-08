import logging
import time
from collections.abc import Mapping
from multiprocessing import Queue

from plugin.config import PluginConfig
from plugin.managers.shape_manager.core import retrieve_shapes
from plugin.presentation.callbacks import (
    NullProgressCallback,
    ProgressCallbackABC,
)
from plugin.presentation.view_model import progress_create
from spectrumlab.peaks.analyte_peaks.shapes import PeakShape
from spectrumlab.spectra import Spectrum

LOGGER = logging.getLogger('plugin-peak-shape')


class ShapeManager:

    def __init__(
        self,
        plugin_config: PluginConfig,
    ) -> None:

        self.plugin_config = plugin_config

    @progress_create
    def retrieve(
        self,
        spectra: Mapping[int, Spectrum],
        progress_callback: ProgressCallbackABC | None = None,
        progress_queue: Queue = None,
    ) -> Mapping[int, PeakShape]:
        progress_callback = progress_callback or NullProgressCallback()
        started_at = time.perf_counter()

        LOGGER.debug(
            'Start to restoring %s shapes...',
            len(spectra),
        )
        try:
            shapes = retrieve_shapes(
                n_workers=self.plugin_config.max_workers,
                spectra=spectra,
                progress_callback=progress_callback,
                progress_queue=progress_queue,
            )
            return shapes

        finally:
            if LOGGER.isEnabledFor(logging.INFO):
                LOGGER.info(
                    'Time elapsed for shapes restoring: {elapsed:.4f}, s'.format(
                        elapsed=time.perf_counter() - started_at,
                    ),
                )
