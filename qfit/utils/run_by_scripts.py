from qfit.core.qfit import Fit
import scqubits as scq
import copy
import yaml
from qfit.models.data_structures import (
    MeasRawXYConfig, ParamAttr
)


# load the config file and create the fit
# ==================================================================
def load_config(path: str, config_file: str = "config.yaml"):
    config_path = path + config_file

    # Load the config
    with open(config_path, 'r') as file:
        config = yaml.safe_load(file)

    return config

def create_fit_by_config(
    hilbert_space: scq.HilbertSpace,
    path: str,
    config_file: str = "config.yaml",
    show_window: bool = False,
):
    """
    Create a fit according to the config file. 
    
    It currently won't automatically extract the points from the measurement data,
    and auto-tagging is performed after the manual extraction.
    """
    config = load_config(path, config_file)

    # Extract the config parameters
    file_paths = [path + fp for fp in config["file_paths"]]
    x_axis = config["axes"]["x"]
    y_axis = config["axes"]["y"]
    if not isinstance(x_axis, str):
        raise ValueError(
            "'axes.x' must be a string. Currently running with scripts "
            "does not support crosstalk calibration with multiple x-axes."
        )
    transpose_square_data = config.get("transpose_square_data", False)
    
    # initialize the fit
    hilbert_space = copy.deepcopy(hilbert_space)
    fit = Fit(hilbert_space, file_paths, show=show_window)
    
    # set the x and y axis for each measurement data
    config = MeasRawXYConfig(
        checkedX = [x_axis],
        checkedY = [y_axis],
    )
    fit._measData.storeRawXYConfig(config)
    fit._measDataCtrl.continueToPostImportStages()
    
    # # transpose the square data if specified
    # if transpose_square_data:
    #     for meas_data in fit._measData.fullData:
    #         if meas_data.ambiguousZOrient:
    #             meas_data.transposeZ()
                
    # fit._measData.emitReadyToPlot()
    
    return fit

# apply the config to the fit
# ==================================================================
def apply_config(
    fit: Fit,
    path: str,
    config_file: str = "config.yaml",
    save_and_close: bool = True,
):
    """
    Apply the config to the fit.
    """
    config = load_config(path, config_file)
    
    x_axis = config["axes"]["x"]
    y_axis = config["axes"]["y"]
    voltage_by_flux = config["voltage_by_flux"]
    init_parameters = config["init_parameters"]
    optimize_calibration = config.get("optimize_calibration", False)
    save_path = path + config["save_path"]
    freq_unit = config.get("freq_unit", "GHz")
    filter_config = config.get("filter", None)
    optimizer = config.get("optimizer", "L-BFGS-B")
    parameter_bounds = config.get("parameter_bounds", {})
    
    # apply the filter
    if filter_config is not None:
        for meas_data in fit._measData.fullData:
            current_filter = meas_data.getFilter()
            for field_name, field_value in filter_config.items():
                setattr(current_filter, field_name, field_value)
            meas_data.setFilter(current_filter)
    fit._measData.emitReadyToPlot()
    
    # calibrate the flux-voltage relationship
    fit._pageView.switchToPage("calibrate")

    for idx, (flux, voltage) in enumerate(voltage_by_flux.items()):
        v_param = ParamAttr(
            parentName = f"X{idx+1}",
            name = x_axis,
            attr = "value",
            value = f"{voltage:.6f}",
        )
        fit._caliParamModel.storeParamAttr(v_param)
        f_param = ParamAttr(
            parentName = f"X{idx+1}",
            name = "flux<br>(Fluxonium)",
            attr = "value",
            value = f"{flux:.6f}",
        )
        fit._caliParamModel.storeParamAttr(f_param)
        fit._caliParamModel.emitUpdateBox()
            
    if freq_unit == "MHz":
        raw_param = ParamAttr(
            parentName = f"Y2",
            name = y_axis,
            attr = "value",
            value = f"1000",
        )
        calib_param = ParamAttr(
            parentName = f"Y2",
            name = "mappedY",
            attr = "value",
            value = "1",
        )
        fit._caliParamModel.storeParamAttr(raw_param)
        fit._caliParamModel.storeParamAttr(calib_param)
        # fit._prefitCaliParams.storeParamAttr(raw_param)
        # fit._prefitCaliParams.storeParamAttr(calib_param)
        fit._caliParamModel.emitUpdateBox()
        
    elif freq_unit == "GHz":
        pass
    else:
        raise ValueError(f"Unit {freq_unit} not supported")
        
    # extract: extract the data points
    fit._pageView.switchToPage("extract")
    # ... not yet implemented
    
    # prefit: set the qubit-resonator parameters
    fit._pageView.switchToPage("prefit")
        
    for parentName, paramDictByParent in init_parameters.items():
        for paramName, param in paramDictByParent.items():
            paramAttr = ParamAttr(
                parentName = parentName,
                name = paramName,
                attr = "value",
                value = f"{param:.6f}",
            )
            fit._prefitHSParams.storeParamAttr(paramAttr)            
    fit._prefitHSParams.emitUpdateBox()
    fit._prefitHSParams.updateParamForHS()

    # fit: 
    # set up the fitting initial parameters
    fit._fitCtrl._prefitToFit()
    # fit._pageView.switchToPage("fit")
    
    # set up the range of the fitting parameters
    for parentName, paramDictByParent in parameter_bounds.items():
        for paramName, param in paramDictByParent.items():
            # if param is a float, set the relative bound
            if isinstance(param, float):
                init_param = init_parameters[parentName][paramName]
                paramAttr = ParamAttr(
                    parentName = parentName,
                    name = paramName,
                    attr = "min",
                    value = init_param * (1 - param),
                )
                fit._fitHSParams.storeParamAttr(paramAttr)
                paramAttr = ParamAttr(
                    parentName = parentName,
                    name = paramName,
                    attr = "max",
                    value = init_param * (1 + param),
                )
                fit._fitHSParams.storeParamAttr(paramAttr)
                
            # if param is a string "fixed", fix the parameter
            elif isinstance(param, str) and param == "fixed":
                paramAttr = ParamAttr(
                    parentName = parentName,
                    name = paramName,
                    attr = "isFixed",
                    value = True,
                )
                fit._fitHSParams.storeParamAttr(paramAttr)
                
            # if param is a list, set the absolute bound
            elif isinstance(param, list):
                paramAttr = ParamAttr(
                    parentName = parentName,
                    name = paramName,
                    attr = "min",
                    value = param[0],
                )
                fit._fitHSParams.storeParamAttr(paramAttr)
                paramAttr = ParamAttr(
                    parentName = parentName,
                    name = paramName,
                    attr = "max",
                    value = param[1],
                )
                fit._fitHSParams.storeParamAttr(paramAttr)
                
            else:
                raise ValueError(f"Parameter bound {paramName} = {param} not supported")
    fit._fitHSParams.emitUpdateBox()
            
    # unfix the flux calibration parameters
    if optimize_calibration:
        for parentName in ["X1", "X2"]:
            paramAttr = ParamAttr(
                parentName = parentName,
                name = "flux<br>(Fluxonium)",
                attr = "isFixed",
                value = False,
            )
            fit._fitCaliParams.storeParamAttr(paramAttr)
    fit._fitCaliParams.emitUpdateBox()
    
    # set the optimizer
    fit._fitView.optimizerComboBox.setCurrentText(optimizer)
    fit._fitModel.updateOptimizer(optimizer)

    # we don't fit in this run
    # fit._fitCtrl.optimizeParams()

    # save
    if save_and_close:
        fit._ioCtrl.forceSaveAs(save_path)
        fit.close()
    
    return fit

def load_fit_by_config(path, config_file: str = "config.yaml", show_window: bool = True):
    config = load_config(path, config_file)
    save_path = path + config["save_path"]
    fit = Fit.open(save_path, show=show_window, deepcopy=True)
    return fit
