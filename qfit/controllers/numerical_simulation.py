
from PySide6.QtCore import (
    QObject,
    Slot,
)

class NumericalCtrl(QObject):
    def __init__(
        self,
        # UI:
        # sliders, slider ranges, options, run fit, auto-run, param to fit
        # model:
        # parameters, quantum model, spectrum, result
        *args,
        **kwargs,
    ):
        pass