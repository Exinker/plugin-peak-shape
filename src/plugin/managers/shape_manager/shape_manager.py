import logging
import time
from collections.abc import Mapping

from plugin.config import (
    PluginConfig,
)
from plugin.managers.shape_manager.core import retrieve_shapes
from plugin.presentation.callbacks import AbstractProgressCallback, NullProgressCallback
from plugin.presentation.view_model import progress_wrapper
from spectrumlab.shapes import Shape
from spectrumlab.spectra import Spectrum

LOGGER = logging.getLogger('plugin-peak-shape')


class ShapeManager:

    def __init__(
        self,
        plugin_config: PluginConfig,
    ) -> None:

        self.plugin_config = plugin_config

    @progress_wrapper
    def retrieve(
        self,
        spectra: Mapping[int, Spectrum],
        progress_callback: AbstractProgressCallback | None = None,
    ) -> Mapping[int, Shape]:
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
            )
            return shapes
        finally:
            if LOGGER.isEnabledFor(logging.INFO):
                LOGGER.info(
                    'Time elapsed for shapes restoring: {elapsed:.4f}, s'.format(
                        elapsed=time.perf_counter() - started_at,
                    ),
                )
