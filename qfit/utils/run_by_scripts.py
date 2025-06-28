import yaml
from qfit.models.data_structures import (
    MeasRawXYConfig, ParamAttr
)
import os

from typing import Dict, List, Any, TYPE_CHECKING
if TYPE_CHECKING:
    from qfit.core.qfit import Fit


# load the config file and create the fit
# ==================================================================
def _splitStr(string: str) -> List[str]:
    return [item.strip() for item in string.split(",")]

def _convertFloatingList(string: str) -> List[float]:
    strList = _splitStr(string)
    return [float(item) for item in strList]

def _loadYaml(yamlPath: str) -> Dict:
    with open(yamlPath, 'r') as file:
        yamlDict = yaml.safe_load(file)
    return yamlDict

def dataPathsFromYaml(yamlFile: str) -> List[str]:
    path = os.path.dirname(yamlFile)
    yamlDict = _loadYaml(yamlFile)
    filePaths = [path + fp for fp in yamlDict["file_paths"]]
    return filePaths


# apply the config to the fit
# ==================================================================
def applyImport(
    fit: "Fit",
    xAxis: List[str],
    yAxis: List[str],
    transposeSquareData: bool,
):
    """Apply the import configuration to the fit."""
    # set the x and y axis for each measurement data
    yamlDict = MeasRawXYConfig(
        checkedX = xAxis,
        checkedY = yAxis,
    )
    fit._measData.storeRawXYConfig(yamlDict)
    if not fit._measData._rawXYIsValid():
        raise ValueError(
            "The selected x and y axes are not valid. "
            "Please check the config file and the measurement data."
        )
    fit._measDataCtrl.continueToPostImportStages()
    
    # transpose the square data if specified
    if transposeSquareData:
        for meas_data in fit._measData.fullData:
            if meas_data.ambiguousZOrient:
                meas_data.transposeZ()
                
    fit._measData.emitReadyToPlot()
    
    return fit


def applyFilters(
    fit: "Fit",
    filterConfig: Dict[str, Any],
):
    """Apply filter configuration to measurement data."""
    if filterConfig is not None:
        for meas_data in fit._measData.fullData:
            current_filter = meas_data.getFilter()
            for field_name, field_value in filterConfig.items():
                setattr(current_filter, field_name, field_value)
            meas_data.setFilter(current_filter)
    fit._measData.emitReadyToPlot()


def applyCalibration(
    fit: "Fit",
    xAxis: List[str],
    yAxis: List[str],
    voltageFluxConversion: Dict[str, str],
    freqUnit: str,
):
    """Apply calibration parameters to the fit."""
    fit._pageView.switchToPage("calibrate")
    voltageNames = fit._caliParamModel._rawXVecNameList
    fluxNames = [
        name
        for name in list(fit._caliParamModel["X1"].keys())
        if name not in xAxis and name != "DATA<br>SOURCE"
    ]
    fluxNamesNoBr = [name.replace("<br>", "") for name in fluxNames]
    numX = len([key for key in fit._caliParamModel.keys() if key.startswith("X")])
    print(f"\nNote: Calibrating parameters must be provided in the following format:")
    print(f"voltage_flux_conversion: ")
    for idx in range(numX):
        print(f"  " + ", ".join(voltageNames) + ": " + ", ".join(fluxNamesNoBr))

    for idx, (voltages, fluxes) in enumerate(voltageFluxConversion.items()):
        fluxes = _convertFloatingList(str(fluxes))
        voltages = _convertFloatingList(str(voltages))
        assert len(voltages) == len(voltageNames), "When providing voltage-flux pairs, " \
            "the voltage list must have the same length as the x axis"
        parentName = f"X{idx+1}"
        for voltage, x_name in zip(voltages, voltageNames):
            vParam = ParamAttr(
                parentName=parentName,
                name=x_name,
                attr="value",
                value=f"{voltage:.6f}",
            )
            fit._caliParamModel.storeParamAttr(vParam)
        for flux, fluxName in zip(fluxes, fluxNames):
            fParam = ParamAttr(
                parentName=parentName,
                name=fluxName,
                attr="value",
                value=f"{flux:.6f}",
            )
            fit._caliParamModel.storeParamAttr(fParam)
        fit._caliParamModel.emitUpdateBox()
    if freqUnit == "MHz":
        rawParam = ParamAttr(
            parentName=f"Y2",
            name=yAxis[0],
            attr="value",
            value=f"1000",
        )
        calibParam = ParamAttr(
            parentName=f"Y2",
            name="mappedY",
            attr="value",
            value="1",
        )
        fit._caliParamModel.storeParamAttr(rawParam)
        fit._caliParamModel.storeParamAttr(calibParam)
        fit._caliParamModel.emitUpdateBox()
    elif freqUnit == "GHz":
        pass
    else:
        raise ValueError(f"Unit {freqUnit} not supported")
    return numX, fluxNames


def applyExtraction(
    fit: "Fit",
):
    """Switch to extraction page (stub for future extraction logic)."""
    fit._pageView.switchToPage("extract")
    # ... not yet implemented


def applyPrefit(
    fit: "Fit",
    initParameters: Dict[str, Dict[str, float]],
):
    """Set the qubit-resonator parameters for prefit."""
    fit._pageView.switchToPage("prefit")
    for parentName, paramDictByParent in initParameters.items():
        for paramName, param in paramDictByParent.items():
            paramAttr = ParamAttr(
                parentName=parentName,
                name=paramName,
                attr="value",
                value=f"{param:.6f}",
            )
            fit._prefitHSParams.storeParamAttr(paramAttr)
    fit._prefitHSParams.emitUpdateBox()
    fit._prefitHSParams.updateParamForHS()


def applyFit(
    fit: "Fit",
    initParameters: Dict[str, Dict[str, float]],
    parameterBounds: Dict[str, Dict[str, Any]],
    optimizeCalibration: bool,
    numX: int,
    fluxNames: List[str],
    optimizer: str,
):
    """Set up the fit parameters, bounds, optimizer, and save/close if needed."""
    fit._fitCtrl._prefitToFit()
    fit._pageView.switchToPage("fit")
    
    for parentName, paramDictByParent in parameterBounds.items():
        for paramName, param in paramDictByParent.items():
            if isinstance(param, float):
                initParam = initParameters[parentName][paramName]
                paramAttr = ParamAttr(
                    parentName=parentName,
                    name=paramName,
                    attr="min",
                    value=initParam * (1 - param),
                )
                fit._fitHSParams.storeParamAttr(paramAttr)
                paramAttr = ParamAttr(
                    parentName=parentName,
                    name=paramName,
                    attr="max",
                    value=initParam
                )
                fit._fitHSParams.storeParamAttr(paramAttr)
            elif isinstance(param, str) and param == "fixed":
                paramAttr = ParamAttr(
                    parentName=parentName,
                    name=paramName,
                    attr="isFixed",
                    value=True,
                )
                fit._fitHSParams.storeParamAttr(paramAttr)
            elif isinstance(param, str):
                param = _convertFloatingList(param)
                assert len(param) == 2, "Parameter bound must be a list of two numbers"
                paramAttr = ParamAttr(
                    parentName=parentName,
                    name=paramName,
                    attr="min",
                    value=param[0],
                )
                fit._fitHSParams.storeParamAttr(paramAttr)
                paramAttr = ParamAttr(
                    parentName=parentName,
                    name=paramName,
                    attr="max",
                    value=param[1],
                )
                fit._fitHSParams.storeParamAttr(paramAttr)
            else:
                raise ValueError(f"Parameter bound {paramName} = {param} not supported")
    fit._fitHSParams.emitUpdateBox()
    if optimizeCalibration:
        for parentName in [f"X{idx+1}" for idx in range(numX)]:
            for fluxName in fluxNames:
                paramAttr = ParamAttr(
                    parentName=parentName,
                    name=fluxName,
                    attr="isFixed",
                    value=False,
                )
                fit._fitCaliParams.storeParamAttr(paramAttr)
    fit._fitCaliParams.emitUpdateBox()
    fit._fitView.optimizerComboBox.setCurrentText(optimizer)
    fit._fitModel.updateOptimizer(optimizer)


def applyConfigYaml(
    fit: "Fit",
    yamlFile: str = "config.yaml",
) -> "Fit":
    """
    Apply the config to the fit by calling the separated steps.
    """
    path = os.path.dirname(yamlFile)
    yamlDict = _loadYaml(yamlFile)
    xAxis = _splitStr(yamlDict["axes"]["x"])
    yAxis = _splitStr(yamlDict["axes"]["y"])
    transposeSquareData = yamlDict.get("transpose_square_data", False)
    assert len(yAxis) == 1, "There should only be one y axis"
    voltageFluxConversion = yamlDict["voltage_flux_conversion"]
    initParameters = yamlDict["init_parameters"]
    optimizeCalibration = yamlDict.get("optimize_calibration", False)
    try:
        savePath = path + yamlDict["save_path"]
    except KeyError:
        savePath = None
    freqUnit = yamlDict.get("freq_unit", "GHz")
    filterConfig = yamlDict.get("filter", None)
    optimizer = yamlDict.get("optimizer", "L-BFGS-B")
    parameterBounds = yamlDict.get("parameter_bounds", {})

    applyImport(fit, xAxis, yAxis, transposeSquareData)
    applyFilters(fit, filterConfig)
    numX, fluxNames = applyCalibration(fit, xAxis, yAxis, voltageFluxConversion, freqUnit)
    applyExtraction(fit)
    applyPrefit(fit, initParameters)
    applyFit(
        fit,
        initParameters,
        parameterBounds,
        optimizeCalibration,
        numX,
        fluxNames,
        optimizer,
    )
    
    if savePath is not None:
        fit._ioCtrl.forceSaveAs(savePath)
        
    return fit