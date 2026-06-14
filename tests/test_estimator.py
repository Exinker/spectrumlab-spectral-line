import numpy as np
import pytest

from spectrumlab.lines import Line
from spectrumlab.types import PicoMeter

from spectrumlab_spectral_line.constants import SIGMA, TAU
from spectrumlab_spectral_line.estimators import LineShapeEstimator, LineShapeEstimatorConfig


@pytest.mark.parametrize(
    ['config', 'line', 'expected'],
    [
        (LineShapeEstimatorConfig(temperature=800, buffer='Ne', tau=TAU, sigma=SIGMA), Line('Zn', 328.23), 2.4810),
        (LineShapeEstimatorConfig(temperature=2400 + 273.15, buffer='Ar', tau=TAU, sigma=SIGMA), Line('Ag', 338.289), 1.7709),
    ],
)
def test_estimated_pvoight_line_shape_fwhm(
    config: LineShapeEstimatorConfig,
    line: Line,
    expected: PicoMeter,
):

    estimator = LineShapeEstimator(
        config=config,
    )
    shape = estimator.fit(
        line=line,
    )

    assert np.isclose(shape.fwhm, expected, atol=1e-3)
