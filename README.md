# spectrumla-line-shape

**spectrumla-line-shape** - библиотека для расчета параметров контура спектральной линии.

## Author Information:
Павел Ващенко (vaschenko@vmk.ru)

[ВМК-Оптоэлектроника](https://www.vmk.ru/), г. Новосибирск 2024 г.


## Installation
Для установки следует выполнить команду `pip install git+https://github.com/Exinker/spectrumlab-spectral-line.git`.


## Usage
Пример использования приложения для расчета контура линии **Zn 328.23** нм:
```python
from spectrumlab.line import Line
from spectrumlab_spectral_line.constants import SIGMA, TAU
from spectrumlab_spectral_line.estimators import LineShapeEstimator, LineShapeEstimatorConfig


estimator = LineShapeEstimator(
    config=LineShapeEstimatorConfig(
        temperature=800,
        buffer='Ne',
        tau=TAU,
        sigma=SIGMA,
    ),
)

shape = estimator.fit(
    line=Line('Zn', 328.23),
    verbose=True,
    show=True,
    save=True,
)

```
<center>
    <figure>
        <img src="./img/Zn 328.23.png" alt="signal-temperature-6bit"/>
        <figcaption>Рис. 1. Контур спектральной линии Zn 328.23: красным - рассчитанный Фойгт, черным - аппроксимация псевдо-Фойгтом
        </figcaption>
    </figure>
</center>
