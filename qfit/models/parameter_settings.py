from scqubits import (
    Transmon,
    TunableTransmon,
    Fluxonium,
    FluxQubit,
    Cos2PhiQubit,
    Oscillator,
    KerrOscillator,
    GenericQubit,
)

from typing import Literal

ParameterType = Literal[
    "EC",
    "EJ",
    "EL",
    "E_osc",
    "l_osc",
    "ng",
    "flux",
    "cutoff",
    "interaction_strength",
    "truncated_dim",
    "raw_X_vec_component",
    "raw_Y",
    "data_source",
]

# default ranges for different types of parameters
# DEFAULT_PARAM_MINMAX = {
#     "EJ": {"min": 1e-5, "max": 50.0},
#     "EC": {"min": 1e-5, "max": 5.0},
#     "EL": {"min": 1e-5, "max": 5.0},
#     "E_osc": {"min": 1e-5, "max": 20.0},
#     "l_osc": {"min": 1e-5, "max": 10.0},
#     "K": {"min": 1e-5, "max": 1.0},
#     "disorder": {"min": -1 + 1e-5, "max": 1 - 1e-5},
#     "ng": {"min": 0.0, "max": 1.0},
#     "flux": {"min": 0.0, "max": 1.0},
#     "cutoff": {"min": 10, "max": 50},
#     "interaction_strength": {"min": -1.0, "max": 1.0},
#     "truncated_dim": {"min": 1, "max": 30},
# }

# for showcasing fluxonium fitting...
DEFAULT_PARAM_MINMAX = {
    "EJ": {"min": 3.0, "max": 10.0},
    "EC": {"min": 0.2, "max": 2.0},
    "EL": {"min": 0.1, "max": 1.0},
    "E_osc": {"min": 4, "max": 8.0},
    "E": {"min": 1e-5, "max": 10.0},
    "l_osc": {"min": 1e-5, "max": 1.0},
    "K": {"min": 1e-5, "max": 1.0},
    "disorder": {"min": -1 + 1e-5, "max": 1 - 1e-5},
    "ng": {"min": 0.0, "max": 1.0},
    "flux": {"min": 0.0, "max": 1.0},
    "cutoff": {"min": 10, "max": 50},
    "interaction_strength": {"min": -1, "max": 1},
    "truncated_dim": {"min": 1, "max": 30},
}

QSYS_PARAM_NAMES = {
    Transmon: {
        "EJ": ["EJ"],
        "EC": ["EC"],
        "ng": ["ng"],
        "cutoff": ["ncut"],
        "truncated_dim": ["truncated_dim"],
    },
    TunableTransmon: {
        "EJ": ["EJmax"],
        "EC": ["EC"],
        "disorder": ["d"],
        "ng": ["ng"],
        "flux": ["flux"],
        "cutoff": ["ncut"],
        "truncated_dim": ["truncated_dim"],
    },
    Fluxonium: {
        "EJ": ["EJ"],
        "EC": ["EC"],
        "EL": ["EL"],
        "flux": ["flux"],
        "cutoff": ["ncut"],
        "truncated_dim": ["truncated_dim"],
    },
    FluxQubit: {
        "EJ": ["EJ1", "EJ2", "EJ3"],
        "EC": ["ECJ1", "ECJ2", "ECJ3", "ECg1", "ECg2"],
        "ng": ["ng1", "ng2"],
        "flux": ["flux"],
        "cutoff": ["ncut"],
        "truncated_dim": ["truncated_dim"],
    },
    Cos2PhiQubit: {
        "EJ": ["EJ"],
        "EC": ["EC", "ECJ"],
        "EL": ["EL"],
        "disorder": ["dCJ", "dEJ", "dL"],
        "flux": ["flux"],
        "ng": ["ng"],
        "cutoff": ["ncut", "phi_cut", "zeta_cut"],
        "truncated_dim": ["truncated_dim"],
    },
    Oscillator: {
        "E_osc": ["E_osc"],
        "l_osc": ["l_osc"],
        "truncated_dim": ["truncated_dim"],
    },
    KerrOscillator: {
        "E_osc": ["E_osc"],
        "l_osc": ["l_osc"],
        "K": ["K"],
        "truncated_dim": ["truncated_dim"],
    },
    GenericQubit: {
        "E": ["E"],
    },
}


# include FluxoniumHiHarm (not in scqubits main branch)
try:
    from scqubits import FluxoniumHiHarm    
    DEFAULT_PARAM_MINMAX.update({
        "EJ2": {"min": -0.5, "max": 0.5},  
    })
    QSYS_PARAM_NAMES.update({
        FluxoniumHiHarm: {
            "EJ": ["EJ"],
            "EJ2": ["EJ2"],
            "EC": ["EC"],
            "EL": ["EL"],
            "flux": ["flux"],
            "cutoff": ["ncut"],
            "truncated_dim": ["truncated_dim"],
        },
    })
except ImportError:
    pass