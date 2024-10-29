from collections.abc import Sequence
from dataclasses import dataclass

from spectrumlab.spectrum import Spectrum

from src.dto.filepath import AtomFilepath
from src.dto.meta import AtomMeta


@dataclass
class AtomData:
    filepath: AtomFilepath
    meta: AtomMeta
    spectra: Sequence[Spectrum]
