from typing import Dict, List, Tuple, Sequence, Any, TYPE_CHECKING, Optional, Union

import numpy as np
from abc import ABC, abstractmethod

if TYPE_CHECKING:
    from qfit.models.calibration import CaliParamModel, CaliTableRowParam
    from qfit.models.parameter_set import ParamSet


def format_mapped_param_key(pair: Tuple[str, str]) -> str:
    """Return a compact label such as ``Q1.EJ`` for a mapped parameter."""
    return f"{pair[0]}.{pair[1]}"


def export_circuit_parameters_from_paramset(
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
        parent, param = parse_mapped_param_name(key)
        conv[(parent, param)] = val
    return conv


def export_calibration_result_from_paramset(
    cali_model: "CaliParamModel", param_set: "ParamSet"
) -> Union["FullCalibrationResult", "PartialCalibrationResult"]:

    # Y calibration (always linear)
    y_slope, y_offset = full_y_calibration(cali_model, param_set)
    raw_y_name = cali_model._rawYName

    if cali_model.isFullCalibration:
        # FULL calibration
        M, b, raw_names, map_names = full_x_calibration(cali_model, param_set)
        return FullCalibrationResult(
            x_linear_part=M,
            x_offset=b,
            raw_dc_bias_names=raw_names,
            mapped_sweep_param_names=map_names,
            y_slope=y_slope,
            y_offset=y_offset,
            raw_y_name=raw_y_name,
        )
    else:
        # PARTIAL calibration
        data_dict, raw_names, map_names = partial_x_calibration(cali_model, param_set)
        return PartialCalibrationResult(
            data_dict=data_dict,
            raw_param_names=raw_names,
            mapped_param_names=map_names,
            y_slope=y_slope,
            y_offset=y_offset,
            raw_y_name=raw_y_name,
        )


class CalibrationResult(ABC):
    """Abstract base class encapsulating Y-axis calibration.

    Sub-classes must implement an *X-axis* helper ``get_mapped_sweep_param``.
    """

    def __init__(self, y_slope: float, y_offset: float, raw_y_name: str):
        self.y_slope = y_slope
        self.y_offset = y_offset
        self.raw_y_name = raw_y_name

    # ------------------------------------------------------------------
    # public – Y calibration
    # ------------------------------------------------------------------
    def get_mapped_y(self, raw_y: np.ndarray) -> np.ndarray:
        """Return mapped-Y value(s) computed via *affine* relation."""
        return self.y_slope * raw_y + self.y_offset

    # subclasses must supply their own X-axis mapping helpers
    @abstractmethod
    def get_mapped_sweep_param(self, *args, **kwargs):
        """Return mapped sweep-parameter values for given raw bias(es)."""
        raise NotImplementedError

    # ------------------------------------------------------------------
    # helpers – representation
    # ------------------------------------------------------------------
    def _repr_y(self) -> str:
        return (
            f"y-axis\n"
            f"raw to mapped: mapped_y = {self.y_slope} * raw_y + {self.y_offset}\n"
            f"raw_y_name   : {self.raw_y_name}\n"
        )

    def __str__(self) -> str:  # pragma: no cover – convenience
        return self.__repr__()


class FullCalibrationResult(CalibrationResult):
    def __init__(
        self,
        x_linear_part: np.ndarray,
        x_offset: np.ndarray,
        raw_dc_bias_names: Tuple[str, ...],
        mapped_sweep_param_names: Tuple[str, ...],
        y_slope: float,
        y_offset: float,
        raw_y_name: str,
    ):
        """
        A class to store the calibration result. The calibration assumes an affine function
        of the raw parameters to the map parameters:
        mapped_sweep_param = x_linear_part @ raw_dc_bias + x_offset
        mapped_y = y_slope * raw_dc_bias + y_offset

        Parameters
        ----------
        x_linear_part
            The linear part of the x-axis calibration result.
        x_offset
            The offset of the x-axis calibration result.
        raw_dc_bias_names
            The names of the raw dc bias parameters.
        mapped_sweep_param_names
            The names of the mapped sweep parameters. Each element is a tuple of
            (parent_name, sweep_param_name).
        y_slope
            The slope of the y-axis calibration result.
        y_offset
            The offset of the y-axis calibration result.
        raw_y_name
            The name of the raw y parameter.
        """
        self.x_linear_part = x_linear_part
        self.x_offset = x_offset
        self.raw_dc_bias_names = raw_dc_bias_names
        # store *parsed* parent/param pairs internally
        self._mapped_param_pairs = tuple(
            parse_mapped_param_name(name) for name in mapped_sweep_param_names
        )
        # initialise Y-axis calibration via super-class
        super().__init__(y_slope=y_slope, y_offset=y_offset, raw_y_name=raw_y_name)
        # convenience: small-formatters for ndarray printing
        self._np_print_opts = dict(precision=6, suppress_small=True)

    def __repr__(self):
        mapped_labels = ", ".join(self.mapped_param_names)
        raw_labels = ", ".join(self.raw_dc_bias_names)
        header = "FullCalibrationResult"
        x_linear_part_str = np.array2string(self.x_linear_part, **self._np_print_opts)
        x_offset_str = np.array2string(self.x_offset, **self._np_print_opts)

        return (
            f"{header}\n"
            f"--------------------------------\n"
            f"x-axis\n"
            f"raw to mapped: mapped_sweep_param = x_linear_part @ raw_dc_bias + x_offset\n"
            f"raw names    : {raw_labels}\n"
            f"mapped names : {mapped_labels}\n"
            f"--------------------------------\n"
            f"x_linear_part =\n{x_linear_part_str}\n"
            f"x_offset = {x_offset_str}\n"
            f"--------------------------------\n"
            f"{self._repr_y()}\n"
        )

    def get_mapped_sweep_param(
        self,
        raw_dc_bias: np.ndarray,
        return_dict: bool = False,
    ) -> "np.ndarray | Dict[str, float]":
        """Return mapped sweep-parameter values for a *raw* dc-bias vector.

        Parameters
        ----------
        raw_dc_bias
            1-D array of length ``N_raw``.
        return_dict
            If *True* a ``dict`` mapping compact labels (e.g. ``Q1.EJ``)
            to float values is returned instead of a bare ``numpy`` vector.
        """
        mapped = self.x_linear_part @ raw_dc_bias + self.x_offset
        if return_dict:
            return {
                key: float(val) for key, val in zip(self.mapped_param_names, mapped)
            }
        return mapped

    # public ----------------------------------------------------------------
    @property
    def mapped_param_names(self) -> Tuple[str, ...]:
        """Human-readable mapped sweep-parameter names."""
        return tuple(format_mapped_param_key(p) for p in self._mapped_param_pairs)


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
        raw_param_names: Tuple[str, ...],
        mapped_param_names: Tuple[str, ...],
        y_slope: float,
        y_offset: float,
        raw_y_name: str,
    ):
        self._data = data_dict
        self.raw_param_names = raw_param_names
        # store *parsed* parent/param pairs internally
        self._mapped_param_pairs = tuple(
            parse_mapped_param_name(name) for name in mapped_param_names
        )
        # store Y-axis calibration using base-class
        super().__init__(y_slope=y_slope, y_offset=y_offset, raw_y_name=raw_y_name)

    # ------------------------------------------------------------------
    # public helpers
    # ------------------------------------------------------------------
    def get_mapped_sweep_param(
        self,
        raw_dc_bias_name: str,
        raw_dc_bias_value: float,
        figure: str,
        return_dict: bool = False,
    ) -> "Dict[str, float] | np.ndarray":
        """Return mapped sweep-parameter values for *partial* calibration.

        Parameters
        ----------
        raw_dc_bias_name
            Which raw dc-bias component to vary (must be in
            ``self.raw_param_names``).
        raw_dc_bias_value
            Value to plug into the linear interpolation/extrapolation.
        figure
            Name of the figure whose two-point calibration should be used.
        return_dict
            If *True* return a ``dict`` keyed by compact labels; otherwise a
            1-D *numpy* array ordered as ``self.mapped_param_names``.
        """
        if figure not in self._data:
            raise KeyError(f"Figure '{figure}' not found in partial calibration data.")

        ((raw1, map1), (raw2, map2)) = self._data[figure]

        # compute per mapped param slope & offset using raw_param_name
        if raw_dc_bias_name not in self.raw_param_names:
            raise KeyError(f"Unknown raw parameter '{raw_dc_bias_name}'.")

        idx_raw = self.raw_param_names.index(raw_dc_bias_name)
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
                for key, val in zip(self.mapped_param_names, mapped_vals)
            }
        return mapped_vals

    def __repr__(self):
        header = "PartialCalibrationResult"
        raw_labels = ", ".join(self.raw_param_names)
        mapped_labels = ", ".join(self.mapped_param_names)

        lines: List[str] = [
            header,
            "--------------------------------",
            f"x-axis\n"
            f"raw names    : {raw_labels}\n"
            f"mapped names : {mapped_labels}\n"
            "--------------------------------",
        ]

        for fig, ((raw1, map1), (raw2, map2)) in self._data.items():
            lines.append(f"Figure: {fig}")
            # raw sweeps
            for rn, v1, v2 in zip(self.raw_param_names, raw1, raw2):
                lines.append(f"  raw {rn}: {v1:.6g} → {v2:.6g}")
            # mapped sweeps
            for pair, m1, m2 in zip(self._mapped_param_pairs, map1, map2):
                lines.append(
                    f"  mapped {format_mapped_param_key(pair)}: {m1:.6g} → {m2:.6g}"
                )
            lines.append("")

        lines.append(self._repr_y())

        return "\n".join(lines)

    # public ----------------------------------------------------------------
    @property
    def mapped_param_names(self) -> Tuple[str, ...]:
        """Human-readable mapped sweep-parameter names."""
        return tuple(format_mapped_param_key(p) for p in self._mapped_param_pairs)


def _get_val(
    row: str,
    col: str,
    param_dict: Dict[str, Dict[str, Any]],
) -> float:
    return param_dict[row][col].value


def parse_mapped_param_name(mapped_param_name: str) -> Tuple[str, str]:
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


def full_x_calibration(
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

            y = np.array(
                [_get_val(r, col_name, mapped_param_source) for r in row_names]
            )

            try:
                alpha = np.linalg.solve(aug_raw_matrix, y)
            except np.linalg.LinAlgError as exc:
                raise ValueError(
                    "Singular matrix while solving for calibration."
                ) from exc

            offsets.append(alpha[0])
            slopes.append(alpha[1:].tolist())
            mapped_param_names.append(col_name)

    x_linear_part = np.asarray(slopes)  # shape (N_mapped, N_raw)
    x_offset = np.asarray(offsets)  # shape (N_mapped,)
    return x_linear_part, x_offset, raw_param_names, tuple(mapped_param_names)


def partial_x_calibration(
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
                [_get_val(row, rn, raw_param_source) for rn in raw_param_names]
            )
            map_vec = np.array(
                [_get_val(row, mn, mapped_param_source) for mn in mapped_param_names]
            )
            raw_vecs.append(raw_vec)
            map_vecs.append(map_vec)

        data_dict[fig] = ((raw_vecs[0], map_vecs[0]), (raw_vecs[1], map_vecs[1]))

    return data_dict, raw_param_names, tuple(mapped_param_names)


def full_y_calibration(
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
        raw_vals.append(_get_val(row, cali_model._rawYName, raw_param_source))
        map_col = "mappedY"
        map_vals.append(_get_val(row, map_col, mapped_param_source))

    aug = np.vstack([np.ones(2), np.array(raw_vals)]).T  # 2x2
    alpha_vec: np.ndarray
    try:
        alpha_vec = np.linalg.solve(aug, np.array(map_vals))
    except np.linalg.LinAlgError:
        raise ValueError("Invalid Y calibration parameters.")

    if alpha_vec is False:
        raise ValueError("Y calibration parameters are not valid.")
    return float(alpha_vec[1]), float(alpha_vec[0])
