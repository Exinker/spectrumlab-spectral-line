from dataclasses import dataclass
from typing import overload

import matplotlib.pyplot as plt
import numpy as np

from spectrumlab.picture.colors import COLOR
from spectrumlab.types import Array, PicoMeter

from spectrumlab_line_shape.shapes import LineShape


@dataclass(frozen=True)
class Line:
    """
    Interface for any line's shape.

    Author: Vaschenko Pavel
     Email: vaschenko@vmk.ru
      Date: 2013.04.12
    """
    shape: LineShape

    @overload
    def __call__(self, x: PicoMeter, position: PicoMeter, intensity: float) -> Array[float]: ...
    @overload
    def __call__(self, x: Array[PicoMeter], position: PicoMeter, intensity: float) -> Array[float]: ...
    def __call__(self, x, position, intensity):
        return self.shape(x, position, intensity)

    def show(self, position: PicoMeter, intensity: float, rx: PicoMeter = 100, dx: PicoMeter = .01) -> None:
        """Show line profile's shape at the range rx with step dx."""

        #
        fig, ax = plt.subplots(figsize=(6, 4), tight_layout=True)

        x = np.linspace(-rx, +rx, 2*int(rx/dx) + 1)
        y = self(x=x, position=position, intensity=intensity)
        plt.plot(
            x, y,
            color=COLOR['blue'],
            label=r'${I}(x)$',
        )

        plt.xlabel(r'$x, \mu$')
        plt.ylabel(r'$I(x)$')

        plt.grid(color='grey', linestyle=':')
        plt.legend()
        plt.show()


if __name__ == '__main__':
    from spectrumlab_line_shape.shapes import PVoigtLineShape

    line = Line(
        shape=PVoigtLineShape(width=25, asymmetry=0, ratio=.1),
    )
    line.show(position=0, intensity=1)
