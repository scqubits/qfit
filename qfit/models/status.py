from typing import List, Optional, Tuple, Union, Callable, Literal

from PySide6.QtCore import QObject, Signal, Slot

from qfit.models.data_structures import Status

DEFAULT_STATUS = Status(
    statusSource=None,
    statusType="ready",
    message="No computation carried out yet.",
    mse=None,
)


class StatusModel(QObject):
    mse_change_ui_setter: Callable
    status_type_ui_setter: Callable
    status_text_ui_setter: Callable
    normalStatusChanged = Signal(str)
    tempStatusChanged = Signal(str, float)

    def __init__(
        self,
        *args,
        **kwargs,
    ):
        """
        This model:
        - receives status type (success, warning, error, computing) and status message
        - for prefit result, fit computing and fit result, receive MSE and compute its change
        - compile message and send to UI for display
          * for errors, add the (<source of error>) in the front of the message
          * add current time in the front of the message
          * for prefit result, fit computing and fit result, generate message based on the MSE change
            (i.e. prefit and fit model does not provide these messages)

        Signals:
        - status_changed: emitted when the status type and message are updated, once emitted, the UI
          will be updated accordingly

        Slots:
        - update_status: receive the signal from prefit model when status is changed, the signal contains
          a Status object.
        """
        super().__init__(*args, **kwargs)
        self.statusStrForView: Optional[str] = None
        self.previousNormalStatus: Status = DEFAULT_STATUS
        self.currentNormalStatus: Status = DEFAULT_STATUS
        self.updateNormalStatus(DEFAULT_STATUS)
        self.oldMseForComputingDelta: Optional[float] = None
        self.newMseForComputingDelta: Optional[float] = None
        self._updateMseForComputingDelta()

    @property
    def deltaMse(self) -> Union[float, None]:
        return self._deltaMse

    @deltaMse.setter
    def deltaMse(self, value: Union[float, None]):
        """
        assign delta_mse value and automatically compute the sign of the change
        to be displayed in the UI.
        """
        self._deltaMse = value
        if self._deltaMse is None:
            self._mseChangeSign = None
        else:
            if self._deltaMse < 0:
                self._mseChangeSign = ""
            else:
                self._mseChangeSign = "+"

    # # to be deleted
    # @property
    # def displayed_status_type(self):
    #     if self.current_status_type is None:
    #         return "STATUS:  -"
    #     return f"STATUS:  {self.status_type}"

    @property
    def displayed_status_text(self):
        if self.statusStrForView is None:
            return "-"
        return self.statusStrForView

    @property
    def displayed_MSE(self):
        if self.newMseForComputingDelta is None:
            return "MSE:  -  (- %)"
        elif self.oldMseForComputingDelta is None:
            return f"MSE:  {self.newMseForComputingDelta:.3f} GHz\u00B2  (- %)"
        else:
            plus_minus = "-" if self.deltaMse < 0 else "+"
            return f"MSE:  {self.newMseForComputingDelta:.4f} GHz\u00B2  ({plus_minus}{self.deltaMse:.2f} %)"

    @property
    def sourceChanged(self):
        # treat fit/fit-result as the same source
        # first rule out the case when the source is None
        if (self.currentNormalStatus.statusSource is not None) and (
            self.previousNormalStatus.statusSource is not None
        ):
            if (self.currentNormalStatus.statusSource == "fit") and (
                self.currentNormalStatus.statusSource == "fit-result"
            ):
                return False
            elif (self.currentNormalStatus.statusSource == "fit-result") and (
                self.currentNormalStatus.statusSource == "fit"
            ):
                return False
        _sourceChanged = (
            self.currentNormalStatus.statusSource
            is not self.previousNormalStatus.statusSource
        )
        return _sourceChanged

    def setupUISetters(
        self,
        mseChangeUISetter: Callable,
        status_type_ui_setter: Callable,
        status_text_ui_setter: Callable,
    ):
        self.mse_change_ui_setter = mseChangeUISetter
        self.status_type_ui_setter = status_type_ui_setter
        self.status_text_ui_setter = status_text_ui_setter

    @Slot(Status)
    def updateNormalStatus(
        self,
        status: Status,
    ):
        """
        Update a normal status and send signal to the UI for display.

        Parameters
        ----------
        status: Status
        """
        # update the status of the message
        self._updateCurrentPreviousNormalStatus(status)
        # get the date and time stamp for the current status
        dateTime = self.currentNormalStatus.timestamp.strftime("%H:%M:%S")
        self.statusStrForView = f"{dateTime}    "
        if self.currentNormalStatus.statusSource is not None:
            statusSource = self.currentNormalStatus.statusSource
            if statusSource == "fit-result":
                statusSource = "fit"
            statusSource = statusSource.upper()
            self.statusStrForView += f"({statusSource}) "
        # parse and generate the message
        if self.currentNormalStatus.statusType == "ready":
            self.statusStrForView += f"{self.currentNormalStatus.message}"
        elif self.currentNormalStatus.statusType == "error":
            self.statusStrForView += f"ERROR: {self.currentNormalStatus.message}"
        elif self.currentNormalStatus.statusType == "success":
            finalMse = self.currentNormalStatus.mse
            self._updateMseForComputingDelta()
            self.statusStrForView += (
                f"SUCCESS: MSE = {finalMse:.4f} GHz\u00B2 ({self.deltaMseStr} %)"
            )
        elif self.currentNormalStatus.statusType == "warning":
            warningMessage = self.currentNormalStatus.message
            if self.currentNormalStatus.statusSource in ["fit", "prefit"]:
                finalMse = self.currentNormalStatus.mse
                self._updateMseForComputingDelta()
                self.statusStrForView += f"WARNING: MSE = {finalMse:.4f} GHz\u00B2 ({self.deltaMseStr} %)  |  {warningMessage}"
            else:
                self.statusStrForView += f"WARNING: {warningMessage}"
        elif self.currentNormalStatus.statusType == "computing":
            if self.currentNormalStatus.statusSource == "fit":
                computingMse = self.currentNormalStatus.mse
                self._updateMseForComputingDelta()
                self.statusStrForView += f"COMPUTING: MSE = {computingMse:.4f} GHz\u00B2 ({self.deltaMseStr} %)"
            elif self.currentNormalStatus.statusSource == "prefit":
                self.statusStrForView += f"COMPUTING"
        elif self.currentNormalStatus.statusType == "initializing":
            initial_mse = self.currentNormalStatus.mse
            self._updateMseForComputingDelta()
            self.statusStrForView += (
                f"INITIALIZE FITTING: MSE = {initial_mse:.4f} GHz\u00B2"
            )
        # emit the signal indicating the status is changed
        self.normalStatusChanged.emit(self.statusStrForView)
        print(self.statusStrForView)

    # @Slot(Status)
    # def updateTempStatus(
    #     self,
    #     status: Status,
    # ):
    #     """
    #     Receives a temp status and send signal to the UI for display.

    #     Parameters
    #     ----------
    #     status: Status
    #     """
    #     # get the date and time stamp for the current status
    #     self.latestTempStatus = status
    #     dateTime = self.currentNormalStatus.timestamp.strftime("%H:%M:%S")
    #     self.statusStrForView = f"{dateTime} "
    #     self.statusStrForView += status.message
    #     self.tempStatusChanged.emit(self.statusStrForView, status.messageTime)

    def _updateMseForComputingDelta(self):
        """
        function that updates the previous MSE and the MSE change. Only use when the MSE is supposed to be
        updated, for example, when the status is computing in the prefit stage, the MSE is NONE and should
        not be updated, however when the status is computing in the fit stage, the MSE should be updated.
        """
        # erase the previous MSE if the source is changed
        if self.sourceChanged:
            self.oldMseForComputingDelta = None
        else:
            # if the information is from prefit, update the old MSE for computing delta
            if self.currentNormalStatus.statusSource == "prefit":
                self.oldMseForComputingDelta = self.newMseForComputingDelta
            # if the information is from fit, depend on the previous status
            elif self.currentNormalStatus.statusSource in ["fit", "fit-result"]:
                # only if the previous status is initializing, store the previous MSE
                # otherwise, the previous MSE stays the same (which is the initialized MSE)
                if self.previousNormalStatus.statusType == "initializing":
                    self.oldMseForComputingDelta = self.newMseForComputingDelta
        self.newMseForComputingDelta = self.currentNormalStatus.mse
        self.deltaMse = self._computeDeltaMse()
        if self.deltaMse is None:
            self.deltaMseStr = "-"
        else:
            self.deltaMseStr = self._mseChangeSign + f"{self.deltaMse:.2f}"

    def _updateCurrentPreviousNormalStatus(self, status: Status):
        self.previousNormalStatus = self.currentNormalStatus
        self.currentNormalStatus = status

    def _computeDeltaMse(self):
        """
        Compute the relative change in MSE between the previous and current calculations, shown in percentage.
        """
        if self.oldMseForComputingDelta is None or self.newMseForComputingDelta is None:
            return None
        return (
            (self.newMseForComputingDelta - self.oldMseForComputingDelta)
            / self.oldMseForComputingDelta
            * 100.0
        )
