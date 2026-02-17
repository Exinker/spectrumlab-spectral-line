from dataclasses import dataclass, field

from spectrumlab.elements import PeriodicTable
from spectrumlab.lines import Line
from spectrumlab.lines.utils import (
    calculate_width_collision,
    calculate_width_doppler,
    calculate_width_natural,
)
from spectrumlab.types import Kelvin, Meter, Second, Symbol

from spectrumlab_line_shape.shapes.shapes import (
    PVoigtLineShape,
    VoigtLineShape,
)
from spectrumlab_line_shape.utils import transform


PERIODIC_TABLE = PeriodicTable()


@dataclass(frozen=True, slots=True)
class LineShapeEstimatorConfig:

    temperature: Kelvin
    buffer: Symbol
    tau: Second = field(default=1e-8)  # lifetime [s]
    sigma: Meter = field(default=2*1e-18)  # collisional cross-section [m^2]


class LineShapeEstimator:

    def __init__(
        self,
        config: LineShapeEstimatorConfig,
    ) -> None:

        self.config = config

    def fit(
        self,
        line: Line,
        verbose: bool = False,
        show: bool = False,
        save: bool = False,
    ) -> PVoigtLineShape:

        width_natural = calculate_width_natural(
            line,
            tau=self.config.tau,
        )
        width_doppler = calculate_width_doppler(
            line,
            temperature=self.config.temperature,
        )
        width_collision = calculate_width_collision(
            line,
            buffer=PERIODIC_TABLE[self.config.buffer],
            temperature=self.config.temperature,
            sigma=self.config.sigma,
        )

        shape = VoigtLineShape(
            g=width_doppler,
            l=width_collision,
        )

        if verbose:
            content = '\n'.join([
                f'{line}:',
                f'\tNatural broadening: {width_natural:.3f} [pm]',
                f'\tDoppler broadening: {width_doppler:.3f} [pm]',
                f'\tCollision broadening: {width_collision:.3f} [pm]',
                f'\tFWHM of the shape (by formula): {shape.fwhm:.4f} [pm].',
            ])
            print(content)

        return transform(
            line=line,
            shape=shape,
            show=show,
            save=save,
        )

    def __repr__(self) -> str:
        cls = self.__class__

        return f'{cls.__name__}(config={self.config})'
