import numpy as np
from typing import List, Optional, Tuple, Union, Callable, Literal

from PySide6.QtCore import QObject, Signal, Slot

from qfit.models.data_structures import Status
import qfit.settings as settings

DEFAULT_STATUS = Status(
    statusSource=None,
    statusType="ready",
    message="No computation carried out yet.",
    mse=None,
)


class StatusModel(QObject):
    """
    Store and manage the status of the application. The status is divided into
    two types:
        - normal status: the status of the application, which is displayed in the
        status bar. It is updated by the prefit and fit models.
        - temporary status: the status of the application, which is displayed in the
        temporary status bar. It is updated by the prefit and fit models.
        (currently not implemented)

    The model's main function:
        - receives status type ("ready", "error", "success", "warning", 
        "computing", "initializing") and status message
        - for prefit result, fit computing and fit result, receive MSE and compute its change
        - compile message and send to UI for display  
            - for errors, add the (<source of error>) in the front of the message
            - add current time in the front of the message
            - for prefit result, fit computing and fit result, generate message based on the MSE change
                (i.e. prefit and fit model does not provide these messages)

    Parameters
    ----------
    parent : QObject
        The parent QObject.
    """

    normalStatusChanged = Signal(str)
    tempStatusChanged = Signal(str, float)

    def __init__(
        self,
        parent: QObject,
    ):
        super().__init__(parent)
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
        Assign deltaMse value and automatically compute the sign of the change
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

    @property
    def displayedStatusText(self) -> str:
        """
        The status text to be displayed in the status bar.
        """
        if self.statusStrForView is None:
            return "-"
        return self.statusStrForView
    
    def _MSEString(self, mse: float | None) -> str:
        if settings.ROOT_MSE:
            unit = settings.MSE_UNIT
            mse_name = "root mean square error"
        else:
            unit = settings.MSE_UNIT + "\u00B2"
            mse_name = "mean square error"
        
        if mse is None:
            mse_str = "-"
        elif np.isnan(mse):
            mse_str = "-"
        else: # mse is a float, process value
            if settings.MSE_UNIT == "GHz":
                pass
            elif settings.MSE_UNIT == "MHz":
                mse = mse * 1e6
            else:
                raise ValueError(f"Invalid MSE unit: {settings.MSE_UNIT}")
                
            if settings.ROOT_MSE:
                mse = np.sqrt(mse)
                
            mse_str = f"{mse:.{settings.MSE_DISPLAY_PRECISION}f} {unit}"
        
        return mse_name + ": " + mse_str
    
    @property
    def displayedMSE(self) -> str:
        """
        The MSE to be displayed in the status bar, along with the change in MSE.
        """
        if self.newMseForComputingDelta is None:
            return f"{self._MSEString(None)}  (- %)"
        elif self.oldMseForComputingDelta is None:
            return f"{self._MSEString(self.newMseForComputingDelta)}  (- %)"
        else:
            plus_minus = "-" if self.deltaMse < 0 else "+"
            return f"{self._MSEString(self.newMseForComputingDelta)}  ({plus_minus}{self.deltaMse:.2f} %)"

    @property
    def sourceChanged(self) -> bool:
        """
        Check if the source of the status is changed.

        Note: it treat fit/fit-result as the same source
        """
        if self.currentNormalStatus.statusSource in [
            "fit",
            "fit-result",
        ] and self.previousNormalStatus.statusSource in ["fit", "fit-result"]:
            return False

        _sourceChanged = (
            self.currentNormalStatus.statusSource
            is not self.previousNormalStatus.statusSource
        )
        return _sourceChanged

    @Slot(Status)
    def updateNormalStatus(
        self,
        status: Status,
    ):
        """
        Receive a normal status and send signal to the UI for display.

        Parameters
        ----------
        status: Status
        """
        # update the status of the message
        self._updateCurrentPreviousNormalStatus(status)

        # get the date and time stamp for the current status
        dateTime = self.currentNormalStatus.timestamp.strftime("%H:%M:%S")
        self.statusStrForView = f"{dateTime}    "

        # add the source of the status
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
            successMessage = self.currentNormalStatus.message

            if finalMse is None:
                self.statusStrForView += f"SUCCESS: {successMessage}. "
            else:
                self._updateMseForComputingDelta()
                self.statusStrForView += f"SUCCESS: "
                self.statusStrForView += f"{self._MSEString(finalMse)} ({self.deltaMseStr} %). "
                self.statusStrForView += f"     |     "
                self.statusStrForView += f"MESSAGE: {successMessage}"

        elif self.currentNormalStatus.statusType == "warning":
            warningMessage = self.currentNormalStatus.message
            if self.currentNormalStatus.statusSource in ["fit", "prefit"]:
                finalMse = self.currentNormalStatus.mse
                self._updateMseForComputingDelta()
                self.statusStrForView += f"WARNING: "
                self.statusStrForView += f"{self._MSEString(finalMse)} ({self.deltaMseStr} %). "
                self.statusStrForView += f"     |     "
                self.statusStrForView += f"MESSAGE: {warningMessage}"
            else:
                self.statusStrForView += f"WARNING: {warningMessage}"

        elif self.currentNormalStatus.statusType == "computing":
            if self.currentNormalStatus.statusSource == "fit":
                computingMse = self.currentNormalStatus.mse
                self._updateMseForComputingDelta()
                self.statusStrForView += f"COMPUTING: {self._MSEString(computingMse)} ({self.deltaMseStr} %). "
            elif self.currentNormalStatus.statusSource == "prefit":
                self.statusStrForView += f"COMPUTING: "

        elif self.currentNormalStatus.statusType == "initializing":
            initial_mse = self.currentNormalStatus.mse
            self._updateMseForComputingDelta()
            self.statusStrForView += (
                f"INITIALIZE FITTING: {self._MSEString(initial_mse)}"
            )

        # emit the signal indicating the status is changed
        self.normalStatusChanged.emit(self.statusStrForView)

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
        Updates the previous Mean Squared Error (MSE) and the change in MSE.

        This function should only be used when an update to the MSE is expected.
        For instance, during the 'prefit' stage when the status is 'computing',
        the MSE is set to None and should not be updated.
        Conversely, during the 'fit' stage when the status is
        'computing', the MSE should be updated.
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
        """
        Update the current and previous normal status.

        Parameters
        ----------
        status: Status
        """
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
