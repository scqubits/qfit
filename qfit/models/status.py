import numpy as np
from typing import List, Optional, Tuple, Union, Callable, Literal

from PySide6.QtCore import QObject, Signal, Slot

from qfit.models.data_structures import Status
import qfit.settings as settings

DEFAULT_STATUS = Status(
    statusSource=None,
    statusType="ready",
    message="No computation carried out yet.",
    cost=None,
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
        - for prefit result, fit computing and fit result, receive cost function and compute its change
        - compile message and send to UI for display  
            - for errors, add the (<source of error>) in the front of the message
            - add current time in the front of the message
            - for prefit result, fit computing and fit result, generate message based on the cost function change
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
        self.oldCostForComputingDelta: Optional[float] = None
        self.newCostForComputingDelta: Optional[float] = None
        self._updateCostForComputingDelta()

    @property
    def deltaCost(self) -> Union[float, None]:
        if (
            self.oldCostForComputingDelta is None
            or self.newCostForComputingDelta is None
        ):
            return None
        
        return (
            (self.newCostForComputingDelta - self.oldCostForComputingDelta)
            / self.oldCostForComputingDelta
            * 100.0
        )
    
    @property
    def deltaCostStr(self) -> str:
        value = self.deltaCost
        # store the string version of the value
        if value is None:
            return "-"
        else:
            if value < 0:
                _costChangeSign = ""
            else:
                _costChangeSign = "+"
            return _costChangeSign + f"{value:.2f}"

    @property
    def displayedStatusText(self) -> str:
        """
        The status text to be displayed in the status bar.
        """
        if self.statusStrForView is None:
            return "-"
        return self.statusStrForView
    
    def _costString(self, cost: float | None) -> str:
        # get the cost name and unit
        if settings.COST_FUNCTION_TYPE == "MSE":
            if settings.ROOT_DISPLAYED_MSE:
                unitStr = settings.DISPLAYED_COST_UNIT
                costName = "root mean square error"
            else:
                unitStr = settings.DISPLAYED_COST_UNIT + "\u00B2"
                costName = "mean square error"
        elif settings.COST_FUNCTION_TYPE in ["RMSE", "_RMSE_FIG", "_MAE"]:
            unitStr = settings.DISPLAYED_COST_UNIT
            costName = "root mean square error"
        else:
            raise ValueError(f"Invalid cost function type: {settings.COST_FUNCTION_TYPE}")
        
        # unit conversion and display
        if cost is None:
            costValStr = "-"
        elif np.isnan(cost):
            costValStr = "-"
        else: 
            # cost function returns a float, process value
            if settings.COST_FUNCTION_TYPE == "MSE":
                if settings.DISPLAYED_COST_UNIT == "GHz":
                    pass
                elif settings.DISPLAYED_COST_UNIT == "MHz":
                    cost = cost * 1e6
                else:
                    raise ValueError(f"Invalid cost function unit: {settings.DISPLAYED_COST_UNIT}")
                
                if settings.ROOT_DISPLAYED_MSE:
                    cost = np.sqrt(cost)
                
            elif settings.COST_FUNCTION_TYPE in ["RMSE", "_RMSE_FIG", "_MAE"]:
                if settings.DISPLAYED_COST_UNIT == "GHz":
                    pass
                elif settings.DISPLAYED_COST_UNIT == "MHz":
                    cost = cost * 1e3
                else:
                    raise ValueError(f"Invalid cost function unit: {settings.DISPLAYED_COST_UNIT}")
                
            else:
                raise ValueError(f"Invalid cost function type: {settings.COST_FUNCTION_TYPE}")
                
        costValStr = f"{cost:.{settings.DISPLAYED_COST_PRECISION}f} {unitStr}"  
        
        return costName + ": " + costValStr
    
    @property
    def displayedCost(self) -> str:
        """
        The cost function value to be displayed in the status bar, along with the change in cost function.
        """
        if self.newCostForComputingDelta is None:
            return f"{self._costString(None)}  (- %)"
        elif self.oldCostForComputingDelta is None:
            return f"{self._costString(self.newCostForComputingDelta)}  (- %)"
        else:
            plus_minus = "-" if self.deltaCost < 0 else "+"
            return f"{self._costString(self.newCostForComputingDelta)}  ({plus_minus}{self.deltaCost:.2f} %)"

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
            finalCost = self.currentNormalStatus.cost
            successMessage = self.currentNormalStatus.message

            if finalCost is None:
                self.statusStrForView += f"SUCCESS: {successMessage}. "
            else:
                self._updateCostForComputingDelta()
                self.statusStrForView += f"SUCCESS: "
                self.statusStrForView += f"{self._costString(finalCost)} ({self.deltaCostStr} %). "
                self.statusStrForView += f"     |     "
                self.statusStrForView += f"MESSAGE: {successMessage}"

        elif self.currentNormalStatus.statusType == "warning":
            warningMessage = self.currentNormalStatus.message
            if self.currentNormalStatus.statusSource in ["fit", "prefit"]:
                finalCost = self.currentNormalStatus.cost
                self._updateCostForComputingDelta()
                self.statusStrForView += f"WARNING: "
                self.statusStrForView += f"{self._costString(finalCost)} ({self.deltaCostStr} %). "
                self.statusStrForView += f"     |     "
                self.statusStrForView += f"MESSAGE: {warningMessage}"
            else:
                self.statusStrForView += f"WARNING: {warningMessage}"

        elif self.currentNormalStatus.statusType == "computing":
            if self.currentNormalStatus.statusSource == "fit":
                computingCost = self.currentNormalStatus.cost
                self._updateCostForComputingDelta()
                self.statusStrForView += f"COMPUTING: {self._costString(computingCost)} ({self.deltaCostStr} %). "
            elif self.currentNormalStatus.statusSource == "prefit":
                self.statusStrForView += f"COMPUTING: "

        elif self.currentNormalStatus.statusType == "initializing":
            initialCost = self.currentNormalStatus.cost
            self._updateCostForComputingDelta()
            self.statusStrForView += (
                f"INITIALIZE FITTING: {self._costString(initialCost)}"
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

    def _updateCostForComputingDelta(self):
        """
        Updates the previous cost function and the change in cost function.

        This function should only be used when an update to the cost function is expected.
        For instance, during the 'prefit' stage when the status is 'computing',
        the cost function value is set to None and should not be updated.
        Conversely, during the 'fit' stage when the status is
        'computing', the cost function should be updated.
        """
        # erase the previous cost function value if the source is changed
        if self.sourceChanged:
            self.oldCostForComputingDelta = None
        else:
            # if the information is from prefit, update the old cost function for computing delta
            if self.currentNormalStatus.statusSource == "prefit":
                self.oldCostForComputingDelta = self.newCostForComputingDelta
            # if the information is from fit, depend on the previous status
            elif self.currentNormalStatus.statusSource in ["fit", "fit-result"]:
                # only if the previous status is initializing, store the previous cost function
                # otherwise, the previous cost function stays the same (which is the initialized cost function)
                if self.previousNormalStatus.statusType == "initializing":
                    self.oldCostForComputingDelta = self.newCostForComputingDelta
        self.newCostForComputingDelta = self.currentNormalStatus.cost

    def _updateCurrentPreviousNormalStatus(self, status: Status):
        """
        Update the current and previous normal status.

        Parameters
        ----------
        status: Status
        """
        self.previousNormalStatus = self.currentNormalStatus
        self.currentNormalStatus = status
