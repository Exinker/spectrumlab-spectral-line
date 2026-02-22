from dataclasses import dataclass, field
from typing import overload

import numpy as np
from scipy import integrate

from spectrumlab.curves import gauss, pvoigt, voigt
from spectrumlab.grids import Grid
from spectrumlab.grids.utils import estimate_fwhm
from spectrumlab.types import Array, PicoMeter


@dataclass(frozen=True)
class GaussLineShape:
    """Gauss (or normal) line profile's shape."""
    width: PicoMeter

    @overload
    def __call__(self, x: PicoMeter, position: PicoMeter, intensity: float) -> Array[float]: ...
    @overload
    def __call__(self, x: Array[PicoMeter], position: PicoMeter, intensity: float) -> Array[float]: ...
    def __call__(self, x, position, intensity):
        f = intensity*gauss(x, x0=position, w=self.width)

        return f


@dataclass(frozen=True, slots=True)
class VoigtLineShape:
    """Voigt line shape."""
    g: PicoMeter  # fwhm of gauss profile shape (doppler broadening)
    l: PicoMeter  # fwhm of lorents profile shape (collisional broadening)

    @property
    def sigma(self) -> PicoMeter:
        return self.g / np.sqrt(8 * np.log(2))

    @property
    def gamma(self) -> PicoMeter:
        return self.l / 2

    @property
    def fwhm(self) -> PicoMeter:
        """Calculate FWHM of the shape [by formula](https://en.wikipedia.org/wiki/Voigt_profile#The_width_of_the_Voigt_profile)."""  # noqa: 501
        return self.l/2 + np.sqrt((self.l/2)**2 + self.g**2)

    @overload
    def __call__(self, x: PicoMeter, position: PicoMeter, intensity: float) -> Array[float]: ...
    @overload
    def __call__(self, x: Array[PicoMeter], position: PicoMeter, intensity: float) -> Array[float]: ...
    def __call__(self, x, position, intensity):
        f = intensity*voigt(x, x0=position, sigma=self.sigma, gamma=self.gamma)

        return f


@dataclass(frozen=True)
class PVoigtLineShape:
    """
    A simple asymmetric line shape profile for fitting infrared absorption spectra.
    Aaron L. Stancik, Eric B. Brauns
    https://www.sciencedirect.com/science/article/abs/pii/S0924203108000453
    """
    width: PicoMeter
    asymmetry: float = field(default=0)  # non asymmetric default
    ratio: float = field(default=0)  # gauss shape default

    @property
    def fwhm(self, dx: PicoMeter = 1e-2, rx: PicoMeter = 100) -> PicoMeter:
        """Estimate FWHM of the shape"""
        x = np.linspace(-rx, +rx, 2*int(rx/dx) + 1)
        y = self(x, 0, 1)

        fwhm = estimate_fwhm(
            grid=Grid(x, y),
            pitch=1,
        )

        return fwhm

    @overload
    def __call__(self, x: PicoMeter, position: PicoMeter, intensity: float) -> Array[float]: ...
    @overload
    def __call__(self, x: Array[PicoMeter], position: PicoMeter, intensity: float) -> Array[float]: ...
    def __call__(self, x, position, intensity):
        f = intensity*pvoigt(x, x0=position, w=self.width, a=self.asymmetry, r=self.ratio)

        return f


@dataclass(frozen=True)
class SelfReversedPVoigtLineShape:
    """Self-reversed voigt line profile's shape with self-absorption"""
    width: PicoMeter
    asymmetry: float
    ratio: float
    absorbance: float

    @overload
    def __call__(self, x: PicoMeter, position: PicoMeter, intensity: float) -> Array[float]: ...
    @overload
    def __call__(self, x: Array[PicoMeter], position: PicoMeter, intensity: float) -> Array[float]: ...
    def __call__(self, x, position, intensity):
        voigt = pvoigt(x, x0=position, w=self.width, a=self.asymmetry, r=self.ratio)
        f = intensity*voigt*10**(-self.absorbance*voigt)

        return f


@dataclass(frozen=True)
class SigmoidsLineShape:
    """Time distribution."""
    width: tuple[float, float]
    power: float

    @overload
    def __call__(self, x: PicoMeter, position: PicoMeter, intensity: float) -> Array[float]: ...
    @overload
    def __call__(self, x: Array[PicoMeter], position: PicoMeter, intensity: float) -> Array[float]: ...
    def __call__(self, x, position, intensity):
        w = self.width
        p = self.power

        sigmoid = lambda x: ((4/np.pi) * (np.arctan(-w[0]*(x - position)) + np.pi/2) * (1/(1 + np.exp(-w[1]*(x - position)))))**p  # noqa: E501, E731
        f = intensity*sigmoid(x)/integrate.quad(sigmoid, a=position-1e+3, b=position+1e+3)[0]

        return f
