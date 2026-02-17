from typing import TypeAlias

from .estimator import (
    LineShapeEstimator,
    LineShapeEstimatorConfig,
)
from .shapes import (
    PVoigtLineShape,
    VoigtLineShape,
)


LineShape: TypeAlias = VoigtLineShape | PVoigtLineShape


__all__ = [
    LineShape,
    LineShapeEstimator,
    LineShapeEstimatorConfig,
    PVoigtLineShape,
    VoigtLineShape,
]
