from typing import Dict, List, Tuple, Sequence, Any, TYPE_CHECKING, Optional, Union

import numpy as np
from abc import ABC, abstractmethod
from dataclasses import dataclass

if TYPE_CHECKING:
    from qfit.models.calibration import CaliParamModel, CaliTableRowParam
    from qfit.models.parameter_set import ParamSet


from qfit.models.data_structures import FullExtr


# Extracted points class ----------------------------------------------------
@dataclass
class ExtractedPointsResult:
    """Light-weight container for user-extracted transition points.

    Internally this just wraps a nested ``dict`` with the structure::

        {
            <figure_name>: {
                <transition_name>: {
                    "type"           : <str>,   # Tag.tagType
                    "x"              : <List[float]>,
                    "y"              : <List[float]>,
                    "photons"        : <int | None>,
                    "initial_states" : <Any>,  # usually list or int
                    "final_states"   : <Any>,
                },
                ...
            },
            ...
        }

    The container acts like a read-only mapping but can be converted to a
    regular ``dict`` via :pyfunc:`dict` if desired.
    """

    data: Dict[str, Dict[str, Dict[str, Any]]]

    def __getitem__(self, item):
        return self.data[item]

    def __iter__(self):
        return iter(self.data)

    def __len__(self):
        return len(self.data)

    def __repr__(self):  # pragma: no cover – convenience only
        figs = ", ".join(self.data.keys())
        return f"ExtractedPointsResult(figures=[{figs}])"

    def list_figures(self) -> List[str]:
        """Return a list of all figure names contained in the export."""
        return list(self.data.keys())

    def list_transitions(self, figure: str) -> List[str]:
        """Return transition names present in *figure*.

        Parameters
        ----------
        figure
            Figure key as returned by :pyfunc:`list_figures`.
        """
        if figure not in self.data:
            raise KeyError(
                f"Figure '{figure}' not found. Available: {', '.join(self.data.keys())}"
            )
        return list(self.data[figure].keys())


# Calibration result classes ------------------------------------------------
class CalibrationResult(ABC):
    """Abstract base class encapsulating Y-axis calibration.

    Sub-classes must implement an *X-axis* helper ``get_mapped_sweep_params``.
    """

    def __init__(self, y_slope: float, y_offset: float, raw_y_name: str):
        self.y_slope = y_slope
        self.y_offset = y_offset
        self.raw_y_name = raw_y_name

    def get_mapped_y(self, raw_y: float) -> float:
        """Return mapped-Y value(s) computed via *affine* relation."""
        return self.y_slope * raw_y + self.y_offset

    # subclasses must supply their own X-axis mapping helpers
    @abstractmethod
    def get_mapped_sweep_params(
        self,
        return_dict: bool = False,
        *args,
        **kwargs,
    ) -> "np.ndarray | Dict[str, float]":
        """Return mapped sweep-parameter values for given raw bias(es)."""
        raise NotImplementedError

    def _repr_y(self) -> str:
        return (
            f"y-axis\n"
            f"raw to mapped: mapped_y = y_slope * raw_y + y_offset\n"
            f"raw_y_name: {self.raw_y_name}\n"
            f"--------------------------------\n"
            f"y_slope = {self.y_slope}\n"
            f"y_offset = {self.y_offset}\n"
        )

    def __str__(self) -> str:  # pragma: no cover – convenience
        return self.__repr__()


class FullCalibrationResult(CalibrationResult):
    def __init__(
        self,
        x_linear: np.ndarray,
        x_offset: np.ndarray,
        raw_dc_biases_names: Tuple[str, ...],
        mapped_sweep_params_names: Tuple[str, ...],
        y_slope: float,
        y_offset: float,
        raw_y_name: str,
    ):
        """
        A class to store the calibration result. The calibration assumes an affine function
        of the raw parameters to the map parameters:
        mapped_sweep_params = x_linear @ raw_dc_bias + x_offset
        mapped_y = y_slope * raw_dc_bias + y_offset

        Parameters
        ----------
        x_linear
            The linear part of the x-axis calibration result.
        x_offset
            The offset of the x-axis calibration result.
        raw_dc_biases_names
            The names of the raw dc bias parameters.
        mapped_sweep_params_names
            The names of the mapped sweep parameters. Each element is a tuple of
            (parent_name, sweep_param_name).
        y_slope
            The slope of the y-axis calibration result.
        y_offset
            The offset of the y-axis calibration result.
        raw_y_name
            The name of the raw y parameter.
        """
        self.x_linear = x_linear
        self.x_offset = x_offset
        self.raw_dc_biases_names = raw_dc_biases_names
        # store *parsed* parent/param pairs internally
        self.mapped_param_names = tuple(
            parseMappedParamName(name) for name in mapped_sweep_params_names
        )
        # initialise Y-axis calibration via super-class
        super().__init__(y_slope=y_slope, y_offset=y_offset, raw_y_name=raw_y_name)
        # convenience: small-formatters for ndarray printing
        self._np_print_opts = dict(precision=6, suppress_small=True)

    def __repr__(self):
        mapped_labels = ", ".join(
            str(mapped_param_name) for mapped_param_name in self.mapped_param_names
        )
        raw_labels = ", ".join(self.raw_dc_biases_names)
        header = "FullCalibrationResult"
        x_linear_str = np.array2string(self.x_linear, **self._np_print_opts)
        x_offset_str = np.array2string(self.x_offset, **self._np_print_opts)

        return (
            f"{header}\n"
            f"--------------------------------\n"
            f"x-axis\n"
            f"raw to mapped: mapped_sweep_params = x_linear @ raw_dc_biases + x_offset\n"
            f"raw_dc_biases_names: {raw_labels}\n"
            f"mapped_sweep_params_names: {mapped_labels}\n"
            f"--------------------------------\n"
            f"x_linear =\n{x_linear_str}\n"
            f"x_offset = {x_offset_str}\n"
            f"--------------------------------\n"
            f"{self._repr_y()}\n"
        )

    def get_mapped_sweep_params(
        self,
        raw_dc_biases: Dict[str, float],
        return_dict: bool = False,
    ) -> "np.ndarray | Dict[str, float]":
        """Return mapped sweep-parameter values for a *raw* dc-bias vector.

        Parameters
        ----------
        raw_dc_biases
            A dictionary mapping raw dc-bias component names to their values.
        return_dict
            If True, a dict mapping a tuple of (parent_name, param_name)
            to float values is returned instead of a bare numpy vector.
        """
        raw_dc_biases_value = np.array(
            [raw_dc_biases[name] for name in self.raw_dc_biases_names]
        )
        mapped = self.x_linear @ raw_dc_biases_value + self.x_offset
        if return_dict:
            return {
                key: float(val) for key, val in zip(self.mapped_param_names, mapped)
            }
        return mapped


class PartialCalibrationResult(CalibrationResult):
    """Container for *partial* X-axis calibration (figure-specific linear maps).

    Parameters
    ----------
    data_dict: Dict[str, Tuple[Tuple[np.ndarray, np.ndarray], Tuple[np.ndarray, np.ndarray]]]
        key: figure name
        value: ((raw_vec1, map_vec1), (raw_vec2, map_vec2))
    raw_param_names: Tuple[str, ...]
        The names of the raw components used in the calibration.
    mapped_param_names: Tuple[str, ...]
        The names of the mapped sweep parameters used in the calibration.
    y_slope
        The slope of the y-axis calibration result.
    y_offset
        The offset of the y-axis calibration result.
    raw_y_name
        The name of the raw y parameter.
    """

    def __init__(
        self,
        data_dict: Dict[
            str, Tuple[Tuple[np.ndarray, np.ndarray], Tuple[np.ndarray, np.ndarray]]
        ],
        raw_dc_biases_names: Tuple[str, ...],
        mapped_sweep_params_names: Tuple[str, ...],
        y_slope: float,
        y_offset: float,
        raw_y_name: str,
    ):
        self._data = data_dict
        self.raw_dc_biases_names = raw_dc_biases_names
        # store *parsed* parent/param pairs internally
        self.mapped_sweep_params_names = tuple(
            parseMappedParamName(name) for name in mapped_sweep_params_names
        )
        # store Y-axis calibration using base-class
        super().__init__(y_slope=y_slope, y_offset=y_offset, raw_y_name=raw_y_name)

    def get_mapped_sweep_params(
        self,
        raw_dc_bias: Dict[str, float],
        figure: str,
        return_dict: bool = False,
    ) -> Dict[Tuple[str, str], float]:
        """Return mapped sweep-parameter values for *partial* calibration.

        Parameters
        ----------
        raw_dc_bias
            A dictionary mapping a raw dc-bias component name to its value.
            Only one dictionary entry is allowed.
        figure
            Name of the figure whose two-point calibration should be used.
        return_dict
            If *True* return a ``dict`` keyed by compact labels; otherwise a
            1-D *numpy* array ordered as ``self.mapped_sweep_params_names``.
        """
        if figure not in self._data:
            raise KeyError(f"Figure '{figure}' not found in partial calibration data.")

        ((raw1, map1), (raw2, map2)) = self._data[figure]
        if len(raw_dc_bias) != 1:
            raise ValueError(
                "Only one raw dc-bias component is allowed for partial calibration."
            )
        raw_dc_bias_name = list(raw_dc_bias.keys())[0]
        raw_dc_bias_value = raw_dc_bias[raw_dc_bias_name]

        idx_raw = self.raw_dc_biases_names.index(raw_dc_bias_name)
        r1 = raw1[idx_raw]
        r2 = raw2[idx_raw]
        if r1 == r2:
            raise ValueError(
                "Selected raw parameter does not vary between the two calibration points."
            )

        slopes = (map2 - map1) / (r2 - r1)
        offsets = map1 - slopes * r1

        mapped_vals = slopes * raw_dc_bias_value + offsets

        if return_dict:
            return {
                key: float(val)
                for key, val in zip(self.mapped_sweep_params_names, mapped_vals)
            }
        return mapped_vals

    def __repr__(self):
        header = "PartialCalibrationResult"
        raw_labels = ", ".join(self.raw_dc_biases_names)
        mapped_labels = ", ".join(
            str(mapped_param_name) for mapped_param_name in self.mapped_params_names
        )

        lines: List[str] = [
            header,
            "--------------------------------",
            f"x-axis\n"
            f"raw_dc_biases_names: {raw_labels}\n"
            f"mapped_sweep_params_names: {mapped_labels}\n"
            "--------------------------------",
        ]

        for fig, ((raw1, map1), (raw2, map2)) in self._data.items():
            lines.append(f"Figure: {fig}")
            # raw sweeps
            for rn, v1, v2 in zip(self.raw_dc_biases_names, raw1, raw2):
                lines.append(f"  raw {rn}: {v1:.6g} → {v2:.6g}")
            # mapped sweeps
            for pair, m1, m2 in zip(self.mapped_sweep_params_names, map1, map2):
                lines.append(f"  mapped {pair}: {m1:.6g} → {m2:.6g}")
            lines.append("")

        lines.append(self._repr_y())

        return "\n".join(lines)


# Extracted points export ----------------------------------------------------
def getExtractedPoints(
    full_extr: FullExtr,
) -> ExtractedPointsResult:
    """Convert an internal :class:`~qfit.models.data_structures.FullExtr` object
    into a plain Python representation.

    Parameters
    ----------
    full_extr
        The :class:`~qfit.models.data_structures.FullExtr` instance that stores
        all user-extracted transition data.

    Returns
    -------
    ExtractedPointsResult
        A wrapper around a nested dictionary where each transition dictionary
        may contain the following keys (depending on the *include_* flags):

        ``x``        : dict mapping *raw axis name* → vector
        ``y``        : vector of mapped Y values
        ``type``     : transition type
        ``photons``  : number of photons
        ``initial_states`` : initial states
        ``final_states``   : final states
    """

    export_dict: Dict[str, Dict[str, Dict[str, Any]]] = {}

    for fig_name, spectra in full_extr.items():
        fig_dict: Dict[str, Dict[str, Any]] = {}
        for transition in spectra:
            if transition.count() == 0:
                continue  # skip empty transitions

            # mandatory fields
            trans_dict: Dict[str, Any] = {
                "type": transition.tag.tagType,
                "photons": transition.tag.photons,
                "initial_states": transition.tag.initial,
                "final_states": transition.tag.final,
            }

            # principal raw X and raw Y
            y_vals = transition.data[1]
            trans_dict["y"] = y_vals

            # additional raw X components
            raw_dict: Dict[str, Any] = {}
            for raw_key, raw_vec in transition.rawX.items():
                raw_dict[raw_key] = raw_vec
            trans_dict["x"] = raw_dict

            fig_dict[transition.name or f"Transition_{id(transition)}"] = trans_dict

        export_dict[fig_name] = fig_dict

    return ExtractedPointsResult(export_dict)


# Circuit parameters export --------------------------------------------------
def getCircuitParametersFromParamset(
    param_set: "ParamSet",
) -> Dict[Tuple[str, str], float]:
    """
    Export the circuit parameters from the parameter set.

    Parameters
    ----------
    param_set: ParamSet
        The parameter set to export.

    Returns
    -------
    Dict[Tuple[str, str], float]
        The exported circuit parameters.
    """
    flat = param_set.getFlattenedAttrDict("value")

    conv: Dict[Tuple[str, str], float] = {}
    for key, val in flat.items():
        parent, param = parseMappedParamName(key)
        conv[(parent, param)] = val
    return conv


def getCalibrationResultFromParamset(
    cali_model: "CaliParamModel", param_set: "ParamSet"
) -> "CalibrationResult":

    # Y calibration (always linear)
    y_slope, y_offset = returnPrecursorFullYCalibration(cali_model, param_set)
    raw_y_name = cali_model._rawYName

    if cali_model.isFullCalibration:
        # FULL calibration
        M, b, rawNames, mapNames = returnPrecursorFullXCalibration(
            cali_model, param_set
        )
        return FullCalibrationResult(
            x_linear=M,
            x_offset=b,
            raw_dc_biases_names=rawNames,
            mapped_sweep_params_names=mapNames,
            y_slope=y_slope,
            y_offset=y_offset,
            raw_y_name=raw_y_name,
        )
    else:
        # PARTIAL calibration
        dataDict, rawNames, mapNames = returnPrecursorPartialXCalibration(
            cali_model, param_set
        )
        return PartialCalibrationResult(
            data_dict=dataDict,
            raw_dc_biases_names=rawNames,
            mapped_sweep_params_names=mapNames,
            y_slope=y_slope,
            y_offset=y_offset,
            raw_y_name=raw_y_name,
        )


# Helper functions ----------------------------------------------------------
def _getVal(
    row: str,
    col: str,
    param_dict: Dict[str, Dict[str, Any]],
) -> float:
    return param_dict[row][col].value


def parseMappedParamName(mapped_param_name: str) -> Tuple[str, str]:
    """
    Parse the mapped parameter name into parent name and parameter name.
    The mapped parameter name is of the form "param_name<br>(parent_name)".
    This function returns a tuple of (parent_name, param_name).

    Parameters
    ----------
    mapped_param_name
        The name of the mapped parameter.

    Returns
    -------
    Tuple[str, str]
        The parent name and parameter name.
    """
    param_name, parent_name = mapped_param_name.split("<br>")
    parent_name = parent_name.strip("(").strip(")")
    return parent_name, param_name


def augmented_raw_matrix(
    row_names: Sequence[str],
    raw_names: Sequence[str],
    param_dict: Dict[str, Dict[str, Any]],
) -> np.ndarray:
    """
    Build the augmented raw matrix. The augmented raw matrix is a matrix of shape
    (len(row_names), len(raw_names) + 1), where the first column is all 1s, and
    for the remaining matrix, each row is a vector of the raw parameters.

    Parameters
    ----------
    row_names
        The names of the rows of the calibration table.
    raw_names
        The names of the raw parameters.
    param_dict
        The dictionary of parameters.
    """
    aug_raw_matrix = np.ones((len(row_names), len(raw_names) + 1))
    for idx_row, row in enumerate(row_names):
        for idx_col, raw_name in enumerate(raw_names, start=1):
            aug_raw_matrix[idx_row, idx_col] = param_dict[row][raw_name].value
    return aug_raw_matrix


def returnPrecursorFullXCalibration(
    cali_param_model: "CaliParamModel",
    param_set: Optional["ParamSet"] = None,
) -> Tuple[np.ndarray, np.ndarray, Tuple[str, ...], Tuple[str, ...]]:
    """
    Return the full-calibration matrix and offset, based on the supplied parameter set.

    Parameters
    ----------
    cali_param_model
        The CaliParamModel instance.
    param_set
        The parameter set to use for the calibration. If not provided, the
        parameter set from the cali_param_model will be used.

    Returns
    -------
    linear_part, offset, raw_dc_bias_names, mapped_sweep_param_names
        linear_part: shape = (N_mapped, N_raw)
        offset: shape = (N_mapped,)
        raw_dc_bias_names: shape = (N_raw,)
        mapped_sweep_param_names: shape = (N_mapped,)
    """
    if not cali_param_model.isFullCalibration:
        raise ValueError("CaliParamModel is not in *full* calibration mode.")

    raw_param_names = tuple(cali_param_model._rawXVecNameList)  # e.g. ("V1", "V2", ...)
    row_names = tuple(cali_param_model._caliTableXRowIdxList)  # ("X1", "X2", ...)

    mapped_param_source = cali_param_model.parameters
    if param_set is not None:
        mapped_param_source = param_set.parameters
    raw_param_source = cali_param_model.parameters

    # Build augmented raw matrix from *raw* components stored in the live table
    aug_raw_matrix = augmented_raw_matrix(row_names, raw_param_names, raw_param_source)

    offsets: List[float] = []
    slopes: List[List[float]] = []
    mapped_param_names: List[str] = []

    # Loop over all mapped sweep parameters
    for parent_name, param_dict in cali_param_model._sweepParamSet.items():
        for param_name, _param in param_dict.items():
            col_name = f"{param_name}<br>({parent_name})"

            y = np.array([_getVal(r, col_name, mapped_param_source) for r in row_names])

            try:
                alpha = np.linalg.solve(aug_raw_matrix, y)
            except np.linalg.LinAlgError as exc:
                raise ValueError(
                    "Singular matrix while solving for calibration."
                ) from exc

            offsets.append(alpha[0])
            slopes.append(alpha[1:].tolist())
            mapped_param_names.append(col_name)

    x_linear = np.asarray(slopes)  # shape (N_mapped, N_raw)
    x_offset = np.asarray(offsets)  # shape (N_mapped,)
    return x_linear, x_offset, raw_param_names, tuple(mapped_param_names)


def returnPrecursorPartialXCalibration(
    cali_param_model: "CaliParamModel",
    param_set: Optional["ParamSet"] = None,
) -> Tuple[
    Dict[str, Tuple[Tuple[np.ndarray, np.ndarray], Tuple[np.ndarray, np.ndarray]]],
    Tuple[str, ...],
    Tuple[str, ...],
]:
    """Return raw/mapped point pairs used for *partial* calibration.

    Returns
    -------
    data_dict, raw_param_names, mapped_param_names

    data_dict : dict
        key   = figure name
        value = ((raw_vec1, map_vec1), (raw_vec2, map_vec2))
    """

    if cali_param_model.isFullCalibration:
        raise ValueError("Model is in full calibration mode; partial expected.")

    raw_param_names = tuple(cali_param_model._rawXVecNameList)
    mapped_param_names: List[str] = []
    # create order list once
    for parent_name, param_dict in cali_param_model._sweepParamSet.items():
        for param_name in param_dict:
            mapped_param_names.append(f"{param_name}<br>({parent_name})")

    data_dict: Dict[
        str, Tuple[Tuple[np.ndarray, np.ndarray], Tuple[np.ndarray, np.ndarray]]
    ] = {}

    mapped_param_source = cali_param_model.parameters
    if param_set is not None:
        mapped_param_source = param_set.parameters
    raw_param_source = cali_param_model.parameters

    for fig in cali_param_model._figNames:
        rows = cali_param_model._xRowIdxBySourceDict[fig]
        if len(rows) != 2:
            raise ValueError(
                "Each figure in partial calibration must have exactly two points."
            )

        raw_vecs, map_vecs = [], []
        for row in rows:
            raw_vec = np.array(
                [_getVal(row, rn, raw_param_source) for rn in raw_param_names]
            )
            map_vec = np.array(
                [_getVal(row, mn, mapped_param_source) for mn in mapped_param_names]
            )
            raw_vecs.append(raw_vec)
            map_vecs.append(map_vec)

        data_dict[fig] = ((raw_vecs[0], map_vecs[0]), (raw_vecs[1], map_vecs[1]))

    return data_dict, raw_param_names, tuple(mapped_param_names)


def returnPrecursorFullYCalibration(
    cali_model: "CaliParamModel",
    param_set: Optional["ParamSet"] = None,
) -> Tuple[float, float]:
    """Return (offset, slope) for the Y-axis calibration line."""
    # Build matrix and vector manually to allow substitution of mappedY values
    raw_vals = []
    map_vals = []

    raw_param_source = cali_model.parameters
    mapped_param_source = cali_model.parameters
    if param_set is not None:
        mapped_param_source = param_set.parameters

    for row in ["Y1", "Y2"]:
        raw_vals.append(_getVal(row, cali_model._rawYName, raw_param_source))
        map_col = "mappedY"
        map_vals.append(_getVal(row, map_col, mapped_param_source))

    aug = np.vstack([np.ones(2), np.array(raw_vals)]).T  # 2x2
    alpha_vec: np.ndarray
    try:
        alpha_vec = np.linalg.solve(aug, np.array(map_vals))
    except np.linalg.LinAlgError:
        raise ValueError("Invalid Y calibration parameters.")

    if alpha_vec is False:
        raise ValueError("Y calibration parameters are not valid.")
    return float(alpha_vec[1]), float(alpha_vec[0])
