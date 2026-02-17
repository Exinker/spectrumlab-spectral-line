import numpy as np
import pytest

from spectrumlab.lines import Line
from spectrumlab.types import PicoMeter

from spectrumlab_line_shape.shapes.estimator import LineShapeEstimator, LineShapeEstimatorConfig


TAU = 1e-8  # lifetime [s]
SIGMA = 2*1e-18  # collisional cross-section [m^2]


@pytest.mark.parametrize(
    ['config', 'line', 'expected'],
    [
        (LineShapeEstimatorConfig(temperature=800, buffer='Ne', tau=TAU, sigma=SIGMA), Line('Zn', 328.23), 2.4810),
        (LineShapeEstimatorConfig(temperature=2400 + 273.15, buffer='Ar', tau=TAU, sigma=SIGMA), Line('Ag', 338.289), 1.7709),
    ],
)
def test_estimated_shape_fwhm(
    config: LineShapeEstimatorConfig,
    line: Line,
    expected: PicoMeter,
):
    tollerance = 1e-3

    estimator = LineShapeEstimator(
        config=config,
    )
    shape = estimator.fit(
        line=line,
    )

    assert np.abs(shape.fwhm - expected) < tollerance
