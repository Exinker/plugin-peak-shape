import logging
from base64 import b64decode

import numpy as np

from spectrumlab.emulations.detectors import Detector
from spectrumlab.emulations.noise import Noise
from spectrumlab.spectra import Spectrum
from spectrumlab.types import Array

from plugin.types import XML


LOGGER = logging.getLogger('app')


def numpy_array_from_b64(buffer: str) -> Array[float]:
    return np.frombuffer(b64decode(buffer.strip()), dtype=np.double)


class AtomSpectraParser:

    @classmethod
    def from_xml(cls, xml: XML) -> tuple[Spectrum]:

        spectrum = []
        for probe in xml.find('probes').findall('probe'):
            is_not_empty = len(probe.findall('spe')) > 0
            if is_not_empty:
                n_detectors = int(probe.find('spe/info/hardware/assemblage/crystals').text)
                n_numbers = int(probe.find('spe/info/hardware/assemblage/crystal/diodes').text)

                data = probe.find('spe').find('data')
                wavelength = numpy_array_from_b64(data.find('xvals').text)
                intensity = numpy_array_from_b64(data.find('yvals').text)
                detector = {
                    2048: Detector.BLPP2000,
                    4096: Detector.BLPP4000,
                }[n_numbers]
                noise = Noise(
                    detector=detector,
                    n_frames=1,
                )

                for i in range(n_detectors):
                    number = np.arange(n_numbers*i, n_numbers*(i+1))

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
