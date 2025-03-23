from collections.abc import Mapping
from dataclasses import dataclass

from plugin.dto.filepath import AtomFilepath
from plugin.dto.meta import AtomMeta
from spectrumlab.spectra import Spectrum


@dataclass
class AtomData:
    filepath: AtomFilepath
    meta: AtomMeta
    spectra: Mapping[int, Spectrum]
