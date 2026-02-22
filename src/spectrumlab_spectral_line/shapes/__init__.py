from typing import TypeAlias

from .shapes import (
    GaussLineShape,
    PVoigtLineShape,
    SelfReversedPVoigtLineShape,
    SigmoidsLineShape,
    VoigtLineShape,
)


LineShape: TypeAlias = GaussLineShape | VoigtLineShape | PVoigtLineShape | SelfReversedPVoigtLineShape | SigmoidsLineShape


__all__ = [
    GaussLineShape,
    LineShape,
    PVoigtLineShape,
    SelfReversedPVoigtLineShape,
    SigmoidsLineShape,
    VoigtLineShape,
]
