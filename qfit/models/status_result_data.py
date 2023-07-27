from typing import List, Optional, Tuple, Union, Callable
from typing_extensions import Literal

import qfit.io_utils.file_io_serializers as serializers


class Result(serializers.Serializable):
    def __init__(
        self,
    ):
        """
        Store data for results to be displayed in the status area. This class also handles update
        of the UI elements that display the results (after setting up UI callbacks).
        """
        self._previous_mse = None
        self._current_mse = None
        self._status_type = None
        self._status_text = None
        self._mse_change = None

    def setupUISetters(
        self,
        mse_change_ui_setter: Callable,
        status_type_ui_setter: Callable,
        status_text_ui_setter: Callable,
    ):
        self.mse_change_ui_setter = mse_change_ui_setter
        self.status_type_ui_setter = status_type_ui_setter
        self.status_text_ui_setter = status_text_ui_setter

    @property
    def previous_mse(self):
        return self._previous_mse

    @property
    def current_mse(self):
        return self._current_mse

    @property
    def mse_change(self):
        return self._mse_change

    @property
    def status_type(self):
        return self._status_type

    @property
    def status_text(self):
        return self._status_text

    @property
    def displayed_status_type(self):
        if self.status_type is None:
            return "STATUS:  -"
        return f"STATUS:  {self.status_type}"

    @property
    def displayed_MSE(self):
        if self.current_mse is None:
            return "MSE:  -  (- %)"
        plus_minus = "-" if self.mse_change < 0 else "+"
        return (
            f"MSE:  {self.current_mse:.3f} GHz\u00B2  ({plus_minus}{self.mse_change} %)"
        )

    @mse_change.setter
    def mse_change(self, value: float):
        self._mse_change = value
        self.mse_change_ui_setter(value)

    @previous_mse.setter
    def previous_mse(self, value: float):
        # update previous MSE, however, the relative change is not updated here
        self._previous_mse = value

    @current_mse.setter
    def current_mse(self, value: float):
        # update current MSE, update the relative change and trigger the UI update
        self._current_mse = value
        self.mse_change = self._compute_relative_change()

    @status_type.setter
    def status_type(self, value: Literal["SUCCESS", "WARNING", "ERROR", "COMPUTING"]):
        self._status_type = value
        self.status_type_ui_setter(value)

    @status_text.setter
    def status_text(self, value: str):
        self._status_text = value
        self.status_text_ui_setter(value)

    def _compute_relative_change(self):
        """
        Compute the relative change in MSE between the previous and current calculations, shown in percentage.
        """
        if self.previous_mse is None or self.current_mse is None:
            return None
        return (self.current_mse - self.previous_mse) / self.previous_mse * 100.0
