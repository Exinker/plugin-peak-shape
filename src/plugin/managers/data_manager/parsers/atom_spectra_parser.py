import logging
from base64 import b64decode
from collections.abc import Mapping

import numpy as np

from plugin.config import PLUGIN_CONFIG
from plugin.managers.data_manager.exceptions import InvalidDetectorTypeError
from plugin.types import XML
from spectrumlab.detectors import Detector
from spectrumlab.noise import Noise
from spectrumlab.spectra import Spectrum
from spectrumlab.types import Array

LOGGER = logging.getLogger('plugin-peak-shape')


class AtomSpectraParser:

    @classmethod
    def from_xml(cls, xml: XML) -> Mapping[int, Spectrum]:

        spectra = []
        for probe in xml.find('probes').findall('probe'):
            is_not_empty = len(probe.findall('spe')) > 0
            if is_not_empty:

                n_detectors = parse_n_detectors(probe)
                detector_size = parse_detector_size(probe)

                n_numbers = detector_size * n_detectors
                n_frames = parse_n_frames(probe)

                wavelength = parse_wavelength(probe)
                intensity = parse_intensity(probe)
                detector_size = parse_detector_size(probe)
                clipped = parse_clipped(probe, n_numbers=n_numbers)

                detector = get_detector(detector_size)
                noise = Noise(
                    detector=detector,
                    n_frames=n_frames,
                )

                for i in range(n_detectors):
                    number = np.arange(detector_size * i, detector_size * (i + 1))

                    spe = Spectrum(
                        intensity=intensity[number],
                        wavelength=wavelength[number],
                        clipped=clipped[number],
                        number=np.arange(detector_size),
                        deviation=noise(intensity[number]),
                        detector=detector,  # TODO: read from xml!
                    )
                    spectra.append(spe)

        return {
            i: spectrum
            for i, spectrum in enumerate(spectra)
        }


def numpy_array_from_b64(buffer: str, dtype: type) -> Array[float]:
    return np.frombuffer(b64decode(buffer.strip()), dtype=dtype)


def parse_n_detectors(__probe: XML) -> int:
    xpath = 'spe/info/hardware/assemblage/crystals'

    try:
        return int(__probe.find(xpath).text)
    except Exception:
        LOGGER.error("Parse `n_detectors` is failed. Check xpath: %r", xpath)
        raise


def parse_detector_size(__probe: XML) -> int:
    xpath = 'spe/info/hardware/assemblage/crystal/diodes'

    try:
        return int(__probe.find(xpath).text)
    except Exception:
        LOGGER.error("Parse `detector_size` is failed. Check xpath: %r", xpath)
        raise


def parse_n_frames(__probe: XML) -> int:
    xpath = 'spe/info/measurement/expositionN'

    try:
        return int(__probe.find(xpath).text)
    except Exception:
        LOGGER.error("Parse `detector_size` is failed. Check xpath: %r", xpath)

        if PLUGIN_CONFIG.skip_data_exceptions:
            return 1
        raise


def parse_wavelength(__probe: XML) -> Array[float]:
    xpath = 'spe/data/xvals'

    try:
        return numpy_array_from_b64(__probe.find(xpath).text, dtype=np.double)
    except Exception:
        LOGGER.error("Parse `wavelength` is failed. Check xpath: %r", xpath)
        raise


def parse_intensity(__probe: XML) -> Array[float]:
    xpath = 'spe/data/yvals'

    try:
        return numpy_array_from_b64(__probe.find(xpath).text, dtype=np.double)
    except Exception:
        LOGGER.error("Parse `intensity` is failed. Check xpath: %r", xpath)
        raise


def parse_clipped(__probe: XML, n_numbers: int) -> Array[bool]:
    xpath = 'spe/data/ovl'

    mask = np.full(n_numbers, False)
    try:
        mask[numpy_array_from_b64(__probe.find(xpath).text, dtype=np.int32)] = True
        return mask
    except Exception:
        LOGGER.error("Parse `intensity` is failed. Check xpath: %r", xpath)

        if PLUGIN_CONFIG.skip_data_exceptions:
            return mask
        raise


def get_detector(detector_size: int) -> Detector:

    match detector_size:
        case 2048:
            return Detector.BLPP2000
        case 4096:
            return Detector.BLPP4000

    LOGGER.error("Detector with %s cells is not supported yet!", detector_size)

    message = 'Форма контура может быть рассчитана только по спектрам полученным с использованием линейных детекторов БЛПП-2000 и БЛПП-4000!'
    raise InvalidDetectorTypeError(message)
