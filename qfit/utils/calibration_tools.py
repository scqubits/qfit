"""
Utility helpers for exporting calibration results in a compact, stage-independent way.

The functions here do *not* depend on Qt, signals, or other GUI concepts.
They only need a reference to an already-initialised ``CaliParamModel`` so
that they can read the calibration table that the user (or the fit
routine) has populated.

The main public helpers are

* ``full_x_matrix`` return (M, b, raw_names, map_names) for the *full*
  calibration case where map_vec = M @ raw_vec + b.
* ``y_linear_params`` return (offset, slope) for Y-axis calibration.
* ``partial_x_pairs`` for the *partial* calibration case return, for
  every figure, the two raw/mapped vectors that were specified.
"""

from typing import Dict, List, Tuple, Sequence, Any, TYPE_CHECKING, Optional

import numpy as np

if TYPE_CHECKING:
    from qfit.models.calibration import CaliParamModel, CaliTableRowParam
    from qfit.models.parameter_set import ParamSet

# -----------------------------------------------------------------------------
# Helper – internal
# -----------------------------------------------------------------------------


def _augmented_raw_matrix(
    row_names: Sequence[str],
    raw_names: Sequence[str],
    table: Dict[str, Dict[str, Any]],
) -> np.ndarray:
    """Build the (L+1) x (L+1) augmented raw matrix [1, raw_vec]."""
    raw_dim = len(raw_names)
    A = np.ones((len(row_names), raw_dim + 1))
    for r, row in enumerate(row_names):
        for j, rname in enumerate(raw_names, start=1):
            A[r, j] = table[row][rname].value
    return A


# -----------------------------------------------------------------------------
# Public helpers
# -----------------------------------------------------------------------------


def _mapped_value(
    row: str,
    col_name: str,
    cali_model: "CaliParamModel",
    param_set: Optional["ParamSet"] = None,
):
    """Return the mapped parameter value from *param_set* if provided,
    otherwise from the calibration table itself."""
    if (
        param_set is not None
        and row in param_set.parameters
        and col_name in param_set[row]
    ):
        return param_set[row][col_name].value
    # fallback to the live table
    return cali_model.parameters[row][col_name].value


def full_x_matrix(
    cali_model: "CaliParamModel",
    param_set: Optional["ParamSet"] = None,
) -> Tuple[np.ndarray, np.ndarray, Tuple[str, ...], Tuple[str, ...]]:
    """Return the full-calibration matrix and offset.

    Parameters
    ----------
    cali_model
        The *current* ``CaliParamModel`` instance whose ``parameters`` field
        contains the calibration table values.  It must represent a *full*
        calibration (``cali_model.isFullCalibration`` must be *True*).

    Returns
    -------
    M, b, raw_names, map_names
        *M* shape = (N_mapped, N_raw)
        *b* shape = (N_mapped,)
    """
    if not cali_model.isFullCalibration:
        raise ValueError("CaliParamModel is not in *full* calibration mode.")

    raw_names = tuple(cali_model._rawXVecNameList)  # e.g. ("V1", "V2", ...)
    row_names = tuple(cali_model._caliTableXRowIdxList)  # ("X1", "X2", ...)

    A = _augmented_raw_matrix(row_names, raw_names, cali_model.parameters)

    offsets: List[float] = []
    slopes: List[List[float]] = []
    map_names: List[str] = []

    for parent_name, param_dict in cali_model._sweepParamSet.items():
        for param_name, _param in param_dict.items():
            col_name = f"{param_name}<br>({parent_name})"
            y = np.array(
                [
                    _mapped_value(row, col_name, cali_model, param_set)
                    for row in row_names
                ]
            )
            alpha = np.linalg.solve(A, y)  # first element offset, rest slopes
            offsets.append(alpha[0])
            slopes.append(alpha[1:].tolist())
            map_names.append(col_name)

    M = np.asarray(slopes)  # (N_mapped × N_raw)
    b = np.asarray(offsets)
    return M, b, raw_names, tuple(map_names)


def y_linear_params(
    cali_model: "CaliParamModel",
    param_set: Optional["ParamSet"] = None,
) -> Tuple[float, float]:
    """Return (offset, slope) for the Y-axis calibration line."""
    # Build matrix and vector manually to allow substitution of mappedY values
    raw_vals = []
    map_vals = []
    for row in ["Y1", "Y2"]:
        raw_vals.append(cali_model.parameters[row][cali_model._rawYName].value)
        map_col = "mappedY"
        map_vals.append(_mapped_value(row, map_col, cali_model, param_set))

    aug = np.vstack([np.ones(2), np.array(raw_vals)]).T  # 2x2
    alpha_vec: np.ndarray
    try:
        alpha_vec = np.linalg.solve(aug, np.array(map_vals))
    except np.linalg.LinAlgError:
        raise ValueError("Invalid Y calibration parameters.")

    if alpha_vec is False:
        raise ValueError("Y calibration parameters are not valid.")
    return float(alpha_vec[0]), float(alpha_vec[1])


def partial_x_pairs(
    cali_model: "CaliParamModel",
    param_set: Optional["ParamSet"] = None,
) -> Dict[str, Tuple[Tuple[np.ndarray, np.ndarray], Tuple[np.ndarray, np.ndarray]]]:
    """Return the two raw/mapped vectors used in *partial* calibration.

    Returns
    -------
    Dict[fig_name, ((raw1, map1), (raw2, map2))]
        *rawN* and *mapN* are 1-D *numpy* arrays of length *raw_dim* and
        *map_dim* respectively.
    """
    if cali_model.isFullCalibration:
        raise ValueError(
            "Model is in *full* calibration mode; no partial pairs available."
        )

    # raw_dim and map_dim not strictly needed here, keep for clarity if needed

    result: Dict[
        str, Tuple[Tuple[np.ndarray, np.ndarray], Tuple[np.ndarray, np.ndarray]]
    ] = {}

    for fig in cali_model._figNames:
        rows = cali_model._xRowIdxBySourceDict[fig]  # e.g. ['X1', 'X2']
        raw_vecs, map_vecs = [], []
        for row in rows:
            raw_v = np.array(
                [
                    _mapped_value(row, rn, cali_model, param_set)
                    for rn in cali_model._rawXVecNameList
                ]
            )
            mv = []
            for parent_name, param_dict in cali_model._sweepParamSet.items():
                for param_name, _param in param_dict.items():
                    col_name = f"{param_name}<br>({parent_name})"
                    mv.append(_mapped_value(row, col_name, cali_model, param_set))
            map_v = np.array(mv)
            raw_vecs.append(raw_v)
            map_vecs.append(map_v)
        result[fig] = ((raw_vecs[0], map_vecs[0]), (raw_vecs[1], map_vecs[1]))

    return result
