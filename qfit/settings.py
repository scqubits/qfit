from typing import Literal

# execution information
EXECUTED_IN_IPYTHON = False

# color settings
color_dict = {
    "PuOr": {"Cross": "orange", "line": "green", "Scatter": "black"},
    "RdYlBu": {"Cross": "orange", "line": "purple", "Scatter": "black"},
    "bwr": {"Cross": "orange", "line": "purple", "Scatter": "black"},
    "viridis": {"Cross": "red", "line": "purple", "Scatter": "black"},
    "cividis": {"Cross": "red", "line": "green", "Scatter": "black"},
    "gray": {"Cross": "blue", "line": "green", "Scatter": "red"},
}

# plot settings
MARKER_SIZE = 130

# cost function settings
COST_FUNCTION_TYPE: Literal["MSE", "RMSE"] = "RMSE"

# status bar settings
ROOT_DISPLAYED_MSE = True
DISPLAYED_COST_UNIT: Literal["GHz", "MHz"] = "MHz"
DISPLAYED_COST_PRECISION = 2

# numerical model settings
POSSIBLE_INIT_STATE_FREQUENCY = 1   # GHz
