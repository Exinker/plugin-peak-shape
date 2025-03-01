import logging
from base64 import b64decode

import numpy as np

from plugin.managers.data_manager.exceptions import InvalidDetectorTypeError
from plugin.types import XML
from spectrumlab.emulations.detectors import Detector
from spectrumlab.emulations.noise import Noise
from spectrumlab.spectra import Spectrum
from spectrumlab.types import Array


LOGGER = logging.getLogger('app')


class AtomSpectraParser:

    @classmethod
    def from_xml(cls, xml: XML) -> tuple[Spectrum]:

        spectrum = []
        for probe in xml.find('probes').findall('probe'):
            is_not_empty = len(probe.findall('spe')) > 0
            if is_not_empty:

                n_detectors = parse_n_detectors(probe)
                n_numbers = parse_n_numbers(probe)
                wavelength = parse_wavelength(probe)
                intensity = parse_intensity(probe)

                detector = get_detector(n_numbers)
                noise = Noise(
                    detector=detector,
                    n_frames=1,  # TODO: read from xml!
                )

                for i in range(n_detectors):
                    number = np.arange(n_numbers * i, n_numbers * (i + 1))

                    spe = Spectrum(
                        intensity=intensity[number],
                        wavelength=wavelength[number],
                        number=np.arange(n_numbers),
                        deviation=noise(intensity[number]),
                        clipped=np.full(n_numbers, False),  # TODO: read from xml!
                        detector=detector,  # TODO: read from xml!
                    )
                    spectrum.append(spe)

        return tuple(spectrum)


def numpy_array_from_b64(buffer: str) -> Array[float]:
    return np.frombuffer(b64decode(buffer.strip()), dtype=np.double)


def parse_n_detectors(__probe: XML) -> int:
    xpath = 'spe/info/hardware/assemblage/crystals'

    try:
        return int(__probe.find(xpath).text)
    except Exception:
        LOGGER.error("Parse `n_detectors` is failed. Check xpath: %r", xpath)
        raise


def parse_n_numbers(__probe: XML) -> int:
    xpath = 'spe/info/hardware/assemblage/crystal/diodes'

    try:
        return int(__probe.find(xpath).text)
    except Exception:
        LOGGER.error("Parse `n_numbers` is failed. Check xpath: %r", xpath)
        raise


def parse_wavelength(__probe: XML) -> Array[float]:
    xpath = 'spe/data/xvals'

    try:
        return numpy_array_from_b64(__probe.find(xpath).text)
    except Exception:
        LOGGER.error("Parse `wavelength` is failed. Check xpath: %r", xpath)
        raise


def parse_intensity(__probe: XML) -> Array[float]:
    xpath = 'spe/data/yvals'

    try:
        return numpy_array_from_b64(__probe.find(xpath).text)
    except Exception:
        LOGGER.error("Parse `intensity` is failed. Check xpath: %r", xpath)
        raise


def get_detector(__n_numbers: int) -> Detector:

    match __n_numbers:
        case 2048:
            return Detector.BLPP2000
        case 4096:
            return Detector.BLPP4000

    LOGGER.error("Detector with %s cells is not supported yet!", __n_numbers)

    message = 'Форма контура может быть рассчитана только по спектрам полученным с использованием линейных детекторов БЛПП-2000 и БЛПП-4000!'
    raise InvalidDetectorTypeError(message)
