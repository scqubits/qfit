import yaml
from qfit.models.data_structures import (
    MeasRawXYConfig, ParamAttr, Tag, SliderParam
)
from qfit.widgets.validated_line_edits import (
    MultiIntsLineEdit,
    MultiIntTuplesLineEdit,
)
from qfit.models.parameter_set import HSParamSet, SweepParamSet
import os
import warnings

from typing import Dict, List, Any, TYPE_CHECKING
if TYPE_CHECKING:
    from qfit.core.qfit import Fit
    from scqubits.core.hilbert_space import HilbertSpace


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
    
    # hand pick the parameter names
    voltageNames = fit._caliParamModel._rawXVecNameList
    fluxNames = [
        name
        for name in list(fit._caliParamModel["X1"].keys())
        if name not in voltageNames and name != "DATA<br>SOURCE"
    ]
    fluxNamesNoBr = [name.replace("<br>", "") for name in fluxNames]
    numX = len([key for key in fit._caliParamModel.keys() if key.startswith("X")])
    
    # print(f"\nNote: Calibrating parameters must be provided in the following format:")
    # print(f"voltage_flux_conversion: ")
    # for idx in range(numX):
    #     print(f"  " + ", ".join(voltageNames) + ": " + ", ".join(fluxNamesNoBr))

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

def _tagByDict(tagDict):
    """
    Convert a tag dictionary (from the config file) into a Tag object.
    """
    kwargs = {}
    for fieldName, fieldValue in tagDict.items():
        if fieldName == "tagType":
            kwargs[fieldName] = fieldValue
        elif tagDict["tagType"] == "DISPERSIVE_BARE" and fieldName in ["initial", "final"]:
            kwargs[fieldName] = MultiIntTuplesLineEdit.strToTuples(str(fieldValue))
        elif tagDict["tagType"] == "DISPERSIVE_DRESSED" and fieldName in ["initial", "final"]:
            kwargs[fieldName] = MultiIntsLineEdit.strToInts(str(fieldValue))
        else:
            # photons
            kwargs[fieldName] = fieldValue
        
    return Tag(**kwargs)

def applyExtraction(
    fit: "Fit",
    fileAndTransDict: Dict[str, Dict[str, Any]],
):
    """Switch to extraction page (stub for future extraction logic)."""
    fit._pageView.switchToPage("extract")
    
    # for each file, create and label the transitions
    for fileName, configTransDict in fileAndTransDict.items():
        _, fileStr = os.path.split(fileName)
        if configTransDict is None:
            continue
        
        # get the extracted transitions
        extractedTransitions = fit._allDatasets._fullSpectra[fileStr]
        extractedName = [transition.name for transition in extractedTransitions]
        
        # compare extracted_name with config_trans_dict.keys() and create the transitions
        for transitionName in configTransDict.keys():
            if transitionName not in extractedName:
                # create an empty transition
                fit._allDatasets.newRow(transitionName)
                
        # label the transitions
        for transition in extractedTransitions:
            if transition.name in configTransDict.keys():
                tag = _tagByDict(configTransDict[transition.name])
                transition.tag = tag
            else:
                warnings.warn(
                    f"Transition '{transition.name}' is not tagged in config file"
                )
    
    # update the currently visible transition's tag
    activeDataset = fit._extractingCtrl.activeDataset
    activeDataset.dataSwitched.emit(activeDataset._transition)
    
    return fit 


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
    
    # copy the initial parameters to the fit parameters
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
                    value=initParam * (1 + param),
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
    fileAndTransDict = yamlDict["file_paths"]
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

    applyImport(
        fit, 
        xAxis, 
        yAxis, 
        transposeSquareData,
    )
    applyFilters(
        fit, 
        filterConfig,
    )
    numX, fluxNames = applyCalibration(
        fit, 
        xAxis, 
        yAxis, 
        voltageFluxConversion, 
        freqUnit,
    )
    applyExtraction(
        fit,
        fileAndTransDict,
    )
    applyPrefit(
        fit, 
        initParameters,
    )
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


def generate_yaml_template(
    hilbertspace: "HilbertSpace",
    file_path: str | None = None,
    num_voltages: int = 1,
):
    """
    Generate a template for the configuration file to initialize QFit by 
    calling Fit.new_by_yaml().

    Parameters
    ----------
    hilbertspace: HilbertSpace
        The HilbertSpace object for the fit.
    file_path: str, optional
        The path to save the configuration file. If None, print to the 
        console.
    num_voltages: int, optional
        The number of voltage sources for the calibration. Default is 1.
    """
    # grab the parameters from the HilbertSpace object
    paramsToExclude = ["cutoff", "truncated_dim", "l_osc"]
    sweepParams = ["flux", "ng"]
    circuitParams = HSParamSet(SliderParam)
    circuitParams.dynamicalInit(
        hilbertspace, 
        excluded_parameter_type=paramsToExclude + sweepParams,
    )
    sweepParams = SweepParamSet.initByHS(hilbertspace)

    # create the init_parameters string
    initParamsStr = ""
    for parentName, paramDictByParent in circuitParams.items():
        initParamsStr += f"  {parentName}:\n"
        for paramName, param in paramDictByParent.items():
            initParamsStr += f"    {paramName}: {param.value:.4f}\n"
    initParamsStr = initParamsStr.strip("\n")

    # create the parameter_bounds string
    paramBoundsStr = ""
    for parentName, paramDictByParent in circuitParams.items():
        paramBoundsStr += f"  {parentName}:\n"
        for paramName, param in paramDictByParent.items():
            paramBoundsStr += f"    {paramName}: 0.1\n"
    paramBoundsStr = paramBoundsStr.strip("\n")
    
    # create the sweep_parameters string
    sweepParamsStrs = []
    for parentName, paramDictByParent in sweepParams.items():
        for paramName, param in paramDictByParent.items():
            paramStr = f"{paramName}({parentName})"
            sweepParamsStrs.append(paramStr)

    # create the calibration string
    pointsRequired = num_voltages + 1
    numSweepParams = len(sweepParams)

    calibStr = f"""# Example for {num_voltages} voltage source(s) and {numSweepParams} control parameter(s) ({", ".join(sweepParamsStrs)}).
# For a full calibration, provide {pointsRequired} data points (pairs of voltage and control parameter values).
voltage_flux_conversion:
"""
    for i in range(pointsRequired):
        voltagePlaceholders = ", ".join(
            f"<voltage{j+1}_{i+1}>" for j in range(num_voltages)
        )
        controlPlaceholders = ", ".join(
            f"<{sweepParam}_{i+1}>" for sweepParam in sweepParamsStrs
        )
        calibStr += f'  {voltagePlaceholders}: {controlPlaceholders}\n'

    calibStr = calibStr.strip()

    template = f"""# This is a template for the configuration file for initializing QFit.
# Entries wrapped in < > are placeholders that you should replace with your own values.

# =================================================================================
# Required entries
# =================================================================================

# Measurement data files and their corresponding transitions.
# For each file, you can specify transitions and their labels to create an empty transition. 
file_paths:
  <path/to/your/data1>:
    # No transitions are specified for this file.
  <path/to/your/data2>:
    <transition_name_1>:
      tagType: DISPERSIVE_BARE  # can be DISPERSIVE_BARE or DISPERSIVE_DRESSED 
      # For DISPERSIVE_BARE, provide initial and final states as tuples of integers.
      initial: <e.g., 0,0>
      final: <e.g., 0,1>
      photons: <e.g., 1>
    <transition_name_2>:
      tagType: DISPERSIVE_DRESSED
      # For DISPERSIVE_DRESSED, provide initial and final states as integers.
      initial: <e.g., 0>
      final: <e.g., 1>
      photons: <e.g., 1>

# Axes configuration, names must match the data in the file
axes:
  x: <name_of_x_axis_from_data_file>
  y: <name_of_y_axis_from_data_file>

# Calibrate X axis: Voltage-flux conversion.
{calibStr}

# Initial parameters for the fit.
# The structure is generated based on the HilbertSpace object.
# Replace the values with your initial guesses for prefit and fit.
init_parameters:
{initParamsStr}

# =================================================================================
# Optional entries
# =================================================================================

# Frequency unit for the y-axis.
freq_unit: GHz  # available options: MHz, GHz

# Transpose the data if x and y axes are swappable.
transpose_square_data: false

# Optimizer for the fit.
# Options: L-BFGS-B, Nelder-Mead, Powell, shgo, differential_evolution
optimizer: L-BFGS-B

# Optimization bounds. For each parameter, providing: 
# - A float (e.g., 0.1) sets a relative bound of +/- 10% around the initial value.
# - A list of two floats (e.g., [min, max]) sets an absolute value bound.
# - A string "fixed" prevents the parameter from being varied during optimization.
parameter_bounds:
{paramBoundsStr}

# Whether to optimize the voltage-flux conversion parameters.
optimize_calibration: false

# Measurement data's filter settings.
filter:
  topHat: false
  wavelet: false
  edge: false
  bgndX: false
  bgndY: false
  log: false
  min: 0
  max: 100
  color: PuOr

# Path to save the fit results. If not provided, the results will not be saved automatically.
# save_path: <path/to/save/results.qfit>
"""
    if file_path:
        with open(file_path, "w") as f:
            f.write(template)
        print(f"Configuration template saved to {file_path}")
    else:
        print(template)