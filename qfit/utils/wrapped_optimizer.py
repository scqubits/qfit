import warnings
import os
import copy 
from typing import Callable, Dict, List, Any, overload, Union

import numpy as np
import matplotlib.pyplot as plt
from scipy.optimize import (
    minimize,
    differential_evolution,
    shgo,
)

from qfit.utils.helpers import (
    Cmap,
    filter,
    # save_variable_list_dict, 
    # load_variable_list_dict, 
    # save_variable_dict,
    # load_variable_dict,
)

from scqubits.utils.cpu_switch import get_map_method


# ##############################################################################
TARGET_NORMALIZE = 1

def nan_2_flat_val(full_variables, possible_nan_value):
    """
    The full_variables should contain "kappa_s" and "disp"
    """
    if np.isnan(possible_nan_value):
        return (full_variables["disp"])**2 * full_variables["kappa_s"]
    else:
        return possible_nan_value


# def nan_2_constr(full_variables, possible_nan_value):
#     """
#     The full_variables should contain "disp", "kappa_s", "g_sa", 
#     "min_detuning", "detuning_lower_bound", "constr_amp"
#     """
#     if np.isnan(possible_nan_value):
#         base_val = (full_variables["disp"])**2 * full_variables["kappa_s"]
#         val = base_val + manual_constr(**full_variables)
#         return val
#     else:
#         return possible_nan_value

# ##############################################################################
class OptTraj():
    """
    A record of the optimization trajectory, includes the parameters, target, and constraints
    at each iteration. You can save and load it using a csv file.
    """
    def __init__(
        self,
        para_name: List[str],
        para_traj: np.ndarray,
        target_traj: np.ndarray,
        fixed_para: Dict[str, float] = {},
    ):
        """
        Parameters
        ----------
        para_name : List[str]
            The name of the parameters that changes during the optimization.
        para_traj : np.ndarray
            The trajectory of the parameters. The shape should be (iteration, para_num).
        target_traj : np.ndarray
            The trajectory of the target function evaluations. 
            The shape should be (iteration, ).
        fixed_para : Dict[str, float], optional
            The parameters that are fixed during the optimization. Should be specified by
            a dictionary with name and value pairs, by default {}. 
        """
        self.para_name = para_name
        self.para_traj = para_traj
        self.target_traj = target_traj

        self.length = self.para_traj.shape[0]

        self.fixed_para = fixed_para

    @classmethod
    def from_file(cls, file_name, fixed_para_file_name = None):
        """
        Load a OptTraj object from a csv file, which comes from the save method of the
        OptTraj object.
        
        If the fixed_para_file_name is not None,
        the fixed_para will be loaded from the file. Otherwise, the fixed_para will be
        an empty dictionary.
        """
        traj_dict = load_variable_list_dict(file_name, throw_nan=False)

        para_name = [name for name in traj_dict.keys() if name not in [
            "target"]]

        para_shape = [len(traj_dict[para_name[0]]), len(para_name)]
        para_traj = np.zeros(para_shape)
        for idx, name in enumerate(para_name):
            para_traj[:, idx] = traj_dict[name]

        if fixed_para_file_name is not None:
            fixed_para = load_variable_dict(fixed_para_file_name)
        else:
            fixed_para = {}

        instance = cls(
            para_name,
            para_traj,
            traj_dict["target"],
            fixed_para
        )

        return instance

    def __getitem__(self, name) -> np.ndarray:
        if name == "target":
            return self.target_traj
        else:
            idx = self.para_name.index(name)
            return self.para_traj[:, idx]

    def _x_arr_2_dict(self, x: Union[np.ndarray, List]):
        return dict(zip(self.para_name, x))

    def _x_dict_2_arr(self, x: dict):
        return [x[name] for name in self.para_name]

    @property
    def final_para(self) -> Dict[str, float]:
        """The final free parameters of the optimization, in the form of a dictionary."""
        return self._x_arr_2_dict(self.para_traj[-1, :])

    @property
    def final_full_para(self) -> Dict[str, float]:
        """
        The final full parameters of the optimization, including the free and fixed parameters,
        in the form of a dictionary.
        """
        return self.fixed_para | self.final_para
    
    @property
    def final_target(self) -> float:
        """The final target function value of the optimization."""
        return self.target_traj[-1]

    @property
    def init_para(self) -> Dict[str, float]:
        """The initial free parameters of the optimization, in the form of a dictionary."""
        return self._x_arr_2_dict(self.para_traj[0, :])

    @property
    def init_full_para(self) -> Dict[str, float]:
        """
        The initial full parameters of the optimization, including the free and fixed parameters,
        in the form of a dictionary.
        """
        return self.fixed_para | self.init_para

    @property
    def init_target(self) -> float:
        """The initial target function value of the optimization."""
        return self.target_traj[0]
    
    def _best_target_idx(self):
        return np.argmin(self.target_traj)
    
    @property
    def best_para(self) -> Dict[str, float]:
        """The free parameters that gives the best target function value."""
        idx = self._best_target_idx()
        return self._x_arr_2_dict(self.para_traj[idx, :])
    
    @property
    def best_full_para(self) -> Dict[str, float]:
        """
        The full parameters that gives the best target function value, including the free and
        fixed parameters.
        """
        return self.fixed_para | self.best_para
    
    @property
    def best_target(self) -> float:
        """The best target function value."""
        idx = self._best_target_idx()
        return self.target_traj[idx]

    def copy(self) -> "OptTraj":
        """Return a copy of the OptTraj object."""
        new_result = OptTraj(
            self.para_name,
            self.para_traj.copy(),
            self.target_traj.copy(),
            self.fixed_para.copy(),
        )
        return new_result

    def append(self, para_dict: Dict[str, float], target: float) -> None:
        """
        Append a record from a new iteration to the OptTraj object.

        Parameters
        ----------
        para_dict : Dict[str, float]
            The free parameters of the new iteration, in the form of a dictionary.
        target : float
            The target function value of the new iteration.
        """
        para_arr = self._x_dict_2_arr(para_dict)
        self.para_traj = np.append(self.para_traj, [para_arr], axis=0)
        self.target_traj = np.append(self.target_traj, target)
        self.length += 1

    def to_dict(self) -> Dict:
        """
        Returns a dictionary containing all the parameters, target, and constraints of the
        optimization trajectory. 

        Returns
        -------
        Dict
            The dictionary contains the following keys:
            - "target": the target function trajectory
            - "constr": the constraint function trajectory
            - the name of the free parameters: the free parameter trajectory
        """
        traj_dict = {}
        for idx, key in enumerate(self.para_name):
            traj_dict[key] = self.para_traj[:, idx]
        traj_dict["target"] = self.target_traj
        return traj_dict

    def _normalize_para(self, para_range_dict: dict = {}) -> np.ndarray:
        new_var = self.para_traj.copy()

        for var, (low, high) in para_range_dict.items():
            idx = self.para_name.index(var)
            new_var[:, idx] = (new_var[:, idx] - low) / (high - low)

        return new_var
    
    def store_optimizer_result(self, opt_result) -> None:
        """
        Usually a result object will be given by the optimizer. This method will store the
        result in the OptTraj object.
        """
        self.opt_result = opt_result

    def plot(self, para_range_dict: dict = {}, ax = None) -> None:
        """
        Plot the optimization trajectory. With x axis as the iteration number, and y axis
        as the normalized parameters, target.
        """
        # need further updating: use twin y axis for the target_traj
        normalized_para = self._normalize_para(para_range_dict)
        max_target = np.max(self.target_traj)

        need_show = False
        if ax is None:
            fig, ax = plt.subplots(1, 1, figsize=(3, 2.5), dpi=150)
            need_show = True

        ax.plot(range(self.length), normalized_para, label=self.para_name)
        ax.plot(range(self.length), self.target_traj /
            max_target, label="normed_target")
        ax.legend()
        ax.set_xlabel("Iterations")
        ax.set_ylabel("Normalized Parameters")

        if need_show:
            plt.show()

    def plot_2d(
        self, 
        ax, 
        x_name,
        y_name,
        c: str = "white",
        destination_only: bool = True, 
        background_interp: Union[Callable, None] = None,
    ) -> None:
        """
        Plot the optimization trajectory in 2D. With x axis as the normalized x parameter,
        and y axis as the normalized y parameter. The color of the trajectory is specified
        by the parameter c.

        Parameters
        ----------
        ax: matplotlib.axes.Axes
            The axes to plot the trajectory.
        x_name: str
            The name of the x parameter.
        y_name: str
            The name of the y parameter.
        c: str, optional
            The color of the trajectory, by default "white".
        destination_only: bool, optional
            Whether to only plot the destination point, by default True.
        background_interp: Callable, optional
            The function to evaluate the a number (which is usually the background of the
            2D plot). The function should take the x and y parameter as input, and return
            a number. The number will be used as the text of the destination point.
        """
        x = self[x_name]
        y = self[y_name]

        if not destination_only:
            ax.plot(x, y, c=c, alpha=0.3)
        ax.scatter(x[-1], y[-1], c=c, s=8)

        if background_interp is not None:
            val = background_interp(x[-1], y[-1])
            if np.abs(val) >= 1e-2 and np.abs(val) < 1e2: 
                text = f"  {val:.3f}"
            else:
                text = f"  {val:.1e}"
            ax.text(x[-1], y[-1], text, ha="left", va="center", c=c, fontsize=7)

    def save(self, file_name, fixed_para_file_name = None):
        """
        Save the OptTraj object to a csv file. Can be loaded using the OptTraj.from_file() 
        class method.

        Parameters
        ----------
        file_name : str
            The file name to save the OptTraj object.
        fixed_para_file_name : str, optional
            The file name to save the fixed_para dictionary, by default None.
        """
        save_variable_list_dict(file_name, self.to_dict())
        if fixed_para_file_name is not None:
            save_variable_dict(fixed_para_file_name, self.fixed_para)


class MultiTraj():
    """
    A class that stores multiple OptTraj objects. It usually comes from running the optimization
    multiple times.

    You can save and load it using a folder. 
    """
    def __init__(
        self,
    ):
        """
        An empty MultiTraj object.
        """
        self.traj_list: List[OptTraj] = []
        self.length = 0

    @classmethod
    def from_list(
        cls,
        traj_list: List[OptTraj],
    ) -> "MultiTraj":
        """
        Create a MultiTraj object from a list of OptTraj objects.
        """
        new_list = cls()
        for traj in traj_list:
            new_list.append(traj)
        return new_list

    @classmethod
    def from_folder(
        cls,
        path,
        with_fixed = True,
    ) -> "MultiTraj":
        """
        Load a MultiTraj object from a folder. The folder should contain a list of csv files,
        each of which is an OptTraj object. The file name should be in the form of "0.csv",
        "1.csv", "2.csv", etc. It's acceptable if there are some missing files with certain
        index.

        If with_fixed is True, the folder should also contain a file named "fixed.csv", which
        contains the fixed_para dictionary of the OptTraj objects.
        """
        multi_traj = cls()

        path = os.path.normpath(path)
        if not os.path.exists(path):    # check path exists
            raise FileNotFoundError(f"Path {path} doesn't exist.")

        if with_fixed:
            fixed_path = f"{path}/fixed.csv"
        else:
            fixed_path = None

        idx = 0
        missing_in_a_row = 0        # count the number of missing files in a row
        while True:
            try:
                traj_path = f"{path}/{idx}.csv"

                traj = OptTraj.from_file(traj_path, fixed_path)
                multi_traj.append(traj)
                idx += 1
            except FileNotFoundError:
                missing_in_a_row += 1
                idx += 1
                if missing_in_a_row > 20:
                    break

        return multi_traj
            
    @overload
    def __getitem__(
        self, 
        idx: int,
    ) -> OptTraj:
        ...

    @overload
    def __getitem__(
        self,
        idx: slice,
    ) -> "MultiTraj":
        ...
    
    def __getitem__(
        self,
        idx: Union[int, slice],
    ) -> "Union[OptTraj, MultiTraj]":
        if isinstance(idx, int):
            return self.traj_list[idx]
        elif isinstance(idx, slice):
            return MultiTraj.from_list(self.traj_list[idx])
        else:
            raise TypeError(f"Only accept int and slice as index")

    def _target_list(self) -> List[float]:
        target_list = []
        for traj in self.traj_list:
            target_list.append(traj.final_target)

        return target_list

    def append(
        self,
        traj: OptTraj,
    ) -> None:
        """
        Append an OptTraj object to the MultiTraj object.
        """
        self.traj_list.append(traj)
        self.length += 1

    def save(
        self,
        path: str,
    ) -> None:
        """
        Save the MultiTraj object to a folder. The folder will contain a list of csv files,
        each of which is an OptTraj object. The file name will be in the form of "0.csv",
        "1.csv", "2.csv", etc.

        Fixed parameters will be saved in a file named "fixed.csv", will be empty if there
        is no fixed parameters.

        Here we assume all of the OptTraj have the same fixed_para. 
        """
        path = os.path.normpath(path)
        for idx in range(self.length):
            self[idx].save(
                f"{path}/{idx}.csv", 
                fixed_para_file_name=f"{path}/fixed.csv"
            )

    def sort_traj(self, select_num=1) -> "MultiTraj":
        """
        Sort the trajectories by the final target function value, from small to large,
        and return the top select_num trajectories as a new instance of MultiTraj.
        """
        if select_num > self.length:
            raise ValueError(f"Do not have enough data to sort. ")

        sort = np.argsort(self._target_list())
        new_traj = MultiTraj()
        for sorted_idx in range(select_num):
            idx = int(sort[sorted_idx])
            new_traj.append(self[idx])

        return new_traj
    
    def best_traj(self) -> OptTraj:
        """
        Return an OptTraj instance with the smallest final target function value.
        """
        return self.sort_traj(1)[0]

    def plot_target(self, ax=None, ylim=()):
        """
        Plot the target function trajectories of the optimization. The x axis is the iteration
        and the y axis is the target function value.
        """
        need_show = False
        if ax is None:
            fig, ax = plt.subplots(1, 1, figsize=(5, 4), dpi=150)
            need_show = True

        best = self.sort_traj()
        cmap = Cmap(self.length)
        for idx, traj in enumerate(self.traj_list):
            if traj == best:
                filter_name = "emph"
            else:
                filter_name = "trans"

            ax.plot(
                range(traj.length),
                traj.target_traj,
                label=f"traj {idx}",
                color=filter(cmap(idx), filter_name),
                zorder=-1
            )
            ax.scatter(
                [traj.length - 1],
                [traj.target_traj[-1]],
                color=filter(cmap(idx), filter_name),
                zorder=-1
            )

        ax.set_ylim(*ylim)
        # ax.set_title("error rates")
        ax.set_xlabel("Iterations")
        ax.set_ylabel("Cost function")
        # ax.set_legend()
        ax.grid()

        if need_show:
            # plt.savefig("./figures/C2QA slides/error rates w iteration small.png")
            plt.tight_layout()
            plt.show()


# ##############################################################################
class Optimization():
    """
    Optimize using a wrapper for `scipy.minimize`. There are three major difference 
    between this class and the original scipy minimizer
        - The cost function now takes a dictionary as input. The dictionary contains the 
          parameters passed from the optimizer. 
        - When optimizing, the parameters are automatically normalized to the range of [0, 1].
          Of course, it'll be denormalized when passed to the cost function. 
        - Users can define fixed and free parameters using dictionaries. They can 
          fix and free parameters using the `fix` and `free` methods. Both of the parameters
          will be passed to the cost function in a dictonary.

    Supported optimizers: L-BFGS-B, Nelder-Mead, Powell, shgo, differential evolution

    Currently it doesn't support the constraint function & gradient based optimizers.
    """
    def __init__(
        self,
        fixed_variables: Dict[str, float],
        free_variable_ranges: Dict[str, List[float]],
        target_func: Callable,
        target_kwargs: Dict = {},
        optimizer: str = "L-BFGS-B",
        opt_options: Dict = {},
    ):
        """
        Optimize using a wrapper for `scipy.minimize`. There are three major difference 
        between this class and the original scipy minimizer
            - The cost function now takes a dictionary as input. The dictionary contains the 
            parameters passed from the optimizer. 
            - When optimizing, the parameters are automatically normalized to the range of [0, 1]. 
            Of course, it'll be denormalized when passed to the cost function.
            - Users can define fixed and free parameters using dictionaries. They can 
            fix and free parameters using the `fix` and `free` methods. Both of the parameters
            will be passed to the cost function in a dictonary.

        Supported optimizers: L-BFGS-B, Nelder-Mead, Powell, TNC, SLSQP, shgo, 
        differential evolution

        Currently it doesn't support the constraint function & gradient based optimizers.

        Parameters
        ----------
        fixed_variables : Dict[str, float]
            The fixed variables, in the form of a dictionary with name and value pairs.
        free_variable_ranges : Dict[str, List[float]]
            The range of the free variables, in the form of a dictionary with name and
            range pairs. For example: `{"var_1": [0, 1], "var_2": [0, 2]}`.
        target_func : Callable
            The target function to be optimized. The function should take a dictionary
            as the first positional argument, and the dictionary will contain the sanpled 
            fixed and free variables as key-value pairs. The function 
            should return a float number. The form of the function should be:
                `target_func(full_variable_dict, **kwargs)`
        target_kwargs : dict, optional
            The keyword arguments to be passed to the target function, by default {}.
        optimizer : str, optional
            The optimizer to be used, by default "L-BFGS-B". Supported optimizers:
            "L-BFGS-B", "Nelder-Mead", "Powell", "shgo", "differential evolution",
        opt_options : dict, optional
            The options to be passed to the optimizer, by default {}.
        """
        
        self.fixed_variables = copy.deepcopy(fixed_variables)
        self.free_variables = copy.deepcopy(free_variable_ranges)
        self._process_free_fix_overlap()
        self._update_free_name_list()

        # the value stored in self.default_variables is dynamic - it is always
        # the same as the one stored in self.fixed_variables and the middle point
        # of the range for the free variables
        self.default_variables = fixed_variables.copy()
        for key, (low, high) in self.free_variables.items():
            self.default_variables[key] = (low + high) / 2

        self.target_func = target_func
        self.target_kwargs = target_kwargs

        self.optimizer = optimizer
        assert self.optimizer in ["L-BFGS-B", "Nelder-Mead", "Powell", "TNC", "SLSQP", 
                                  "shgo", "differential evolution"]
        self.opt_options = opt_options

    def _process_free_fix_overlap(self):
        """
        check if there is any overlap between the free and fixed variables. If there is,
        leave the variable in the free_variables only.
        """
        var_to_remove = []
        for var in self.fixed_variables.keys():
            if var in self.free_variables.keys():
                var_to_remove.append(var)

        if len(var_to_remove) > 0:
            warnings.warn(
                f"There are some overlaps between free and fixed variables. "
                f"Those variables are set to be freed: {var_to_remove}"
            )
        for var in var_to_remove:
            del self.fixed_variables[var]

    def _update_free_name_list(self):
        """
        Update the order and name of the free variables. Should be called when the free
        and fixed variables are changed.
        """
        self.free_name_list = list(self.free_variables.keys())

    def _check_exist(
        self,
        variable: str,
    ):
        if variable not in self.default_variables.keys():
            raise KeyError(f"{variable} is not in the default variable dict. "
                "Please consider re-initializing an optimize object including this variable.")

    def _fix(
        self,
        variable: str,
        value: Union[float, None] = None,
    ):
        self._check_exist(variable)

        if value is None:
            value = self.default_variables[variable]

        if variable in self.fixed_variables:
            self.fixed_variables[variable] = value
        elif variable in self.free_variables:
            self.fixed_variables[variable] = value
            del self.free_variables[variable]

        # dynamically update the default value
        self.default_variables[variable] = value
        
    def fix(
        self,
        variables=None,
        **kwargs,
    ):
        """
        Fix a variable to a number.

        The method accpets:
        Optimize.fix("var"), 
        Optimize.fix(["var_1", "var_2"]), 
        Optimize.fix({"var_1": 1, "var_2": 2}), 
        Optimize.fix(var_1 = 1, var_2 = 2)
        """
        if variables is None:
            variables = kwargs

        if isinstance(variables, str):
            self._fix(variables)
        elif isinstance(variables, list):
            for var in variables:
                self._fix(var)
        elif isinstance(variables, dict):
            for key, val in variables.items():
                self._fix(key, val)
        else:
            raise ValueError(f"Only accept str, list, dict as the input.")

        self._update_free_name_list()

    def _free(
        self,
        variable: str,
        range: List[float],
    ):
        self._check_exist(variable)

        if variable in self.free_variables:
            self.free_variables[variable] = range
        elif variable in self.fixed_variables:
            self.free_variables[variable] = range
            del self.fixed_variables[variable]

        # dynamically update the default value
        self.default_variables[variable] = (range[0] + range[1]) / 2

    def free(
        self,
        variables: Union[Dict, None] = None,
        fix_rest: bool = False,
        **kwargs,
    ):
        """
        Free a variable and specify its range.

        The method accpets: 
        Optimize.fix({"var_1": (0, 1), "var_2": (0, 2)}), 
        Optimize.fix(var_1 = (0, 1), var_2 = (0, 2))

        If fix_rest is True, the rest of the variables will be fixed to the default value.
        """

        if variables is None:
            variables = kwargs

        if not isinstance(variables, dict):
            raise ValueError(f"Only accept dict as the input.")

        for key, val in variables.items():
            self._free(key, copy.copy(val))

        if fix_rest:
            remaining_var = [var for var in self.free_variables.keys()
                             if var not in variables.keys()]
            self.fix(remaining_var)

        self._update_free_name_list()

    def _normalize_input(self, variables: Dict[str, float]) -> Dict[str, float]:
        """
        Normalize the input variables to the range of [0, 1], according to the range
        specified in self.free_variables.
        """
        new_var = variables.copy()

        for var, range in self.free_variables.items():
            low, high = range
            new_var[var] = (new_var[var] - low) / (high - low)

        return new_var

    def _denormalize_input(self, variables: Dict[str, float]) -> Dict[str, float]:
        new_var = variables.copy()

        for var, range in self.free_variables.items():
            low, high = range
            new_var[var] = new_var[var] * (high - low) + low

        return new_var

    def _normalize_output(self, output):
        return output / TARGET_NORMALIZE

    def _denormalize_output(self, output):
        return output * TARGET_NORMALIZE

    def _x_arr_2_dict(self, x: Union[np.ndarray, List]):
        return dict(zip(self.free_name_list, x))

    def _x_dict_2_arr(self, x: Dict):
        return [x[name] for name in self.free_name_list]

    def target_w_free_var(self, free_var: Dict[str, float]):
        """
        Calculate the target function value with the free variables.
        """
        return self.target_func(self.fixed_variables | free_var, **self.target_kwargs)

    def _opt_func(self, x):
        """
        The function that will be directly fed to the optimizer. 

        x should be a LIST of free variable in the order of self.free_name_list. 
        But this is totally implicit for the user. 
        """
        x_dict = self._x_arr_2_dict(x)
        denorm_x = self._denormalize_input(x_dict)

        target = self._normalize_output(self.target_w_free_var(denorm_x))

        return target

    def opt_init(
        self,
        init_x: Dict[str, float] = {},
        check_func: Callable = lambda *args, **kwargs: True,
        check_kwargs: Dict = {}
    ) -> Dict[str, float]:
        """
        Initialize the optimization. If not specifying the initial x, a random x within range
        will be used.

        Parameters
        ----------
        init_x : Dict[str, float], optional
            The initial free parameters of the optimization, in the form of a dictionary,
            by default {}. If it doesn't contain all the free parameters, the rest of the
            parameters will be initialized randomly.
        check_func : Callable, optional
            The function to check whether the initialization is legal, by default
            is (lambda *args, **kwargs: True). The function should take a dictionary as 
            an input, which contains both of the fixed and free variables. 
            The function should return a boolean value. So it will look like:
                check_func(full_dict, **check_kwargs)
        check_kwargs: Dict, optional
            A dictionary of the key word argument, will be passed to the function.
        """
        max_trial = 100
        count = 0

        # check init_x is within the range
        for var, val in init_x.items():
            if var in self.free_variables:
                low, high = self.free_variables[var]
                if val < low or val > high:
                    raise ValueError(f"init_x[{var}] = {val} is not within the range of [{low}, {high}].")
            else:
                raise ValueError(f"{var} in init_x is not a free variable.")

        # randomly initialize the free variables not specified in init_x until it is legal
        while True:
            norm_init = np.random.uniform(
                low=0,
                high=1,
                size=len(self.free_name_list)
            )
            norm_init_dict = dict(
                zip(self.free_name_list, norm_init))
            denorm_init_dict = self._denormalize_input(norm_init_dict)

            full_init = self.fixed_variables | denorm_init_dict | init_x
            if check_func(full_init, **check_kwargs):
                return denorm_init_dict
            
            count += 1
            if count >= max_trial:
                raise ValueError(f"Cannot find a legal initialization in {count} trials.")


    def _evaluate_record(self, x):
        """
        evaluate the target function and constraint function, in order for the
        record to be saved in the OptTraj object
        """
        x_dict = self._x_arr_2_dict(x)
        denorm_x = self._denormalize_input(x_dict)

        target = self.target_func(
            self.fixed_variables | denorm_x, **self.target_kwargs)

        return denorm_x, target
            
    @staticmethod
    def _running_filename(file_name: str) -> str:
        suffix = file_name.split(".")[-1]
        return f"{file_name[:-len(suffix)]}_RUNNING.{suffix}"
    
    def _construct_call_back(
        self,
        user_callback: Union[Callable, None],
        result: OptTraj,
        file_name: Union[str, None],
        fixed_para_file_name: Union[str, None],
        callback_kwargs: Dict = {},
    ) -> Callable:
        """
        Construct the callback function for the optimizer. The callback function will
        record the result, save the result, and call the user specified callback function.
        """
        def opt_call_back(x, convergence=None):
            # record the result
            denorm_x, target = self._evaluate_record(x)
            result.append(
                denorm_x,
                target,
            )

            # save the result on the fly
            if file_name is not None:
                result.save(self._running_filename(file_name), fixed_para_file_name)

            # call the user specified callback function
            if user_callback is not None:
                user_callback(
                    denorm_x.copy(),
                    target,
                    **callback_kwargs
                )

        return opt_call_back

    def run(
        self,
        init_x: dict = {},
        callback: Union[Callable, None] = None,
        callback_kwargs: dict = {},
        check_func: Callable = lambda x: True,
        check_kwargs: dict = {},
        file_name: Union[str, None] = None,
        fixed_para_file_name: Union[str, None] = None,
    ):
        """
        Run the optimization.

        Parameters
        ----------
        init_x : Dict[str, float], optional
            The initial free parameters of the optimization, in the form of a dictionary,
            by default {}. If it doesn't contain all the free parameters, the rest of the
            parameters will be initialized randomly.
        call_back : Callable, optional
            The function to be called after each iteration, by default None. The function
            should take the following arguments:
            - free_var: the free variables of the current iteration, in the form of a
                dictionary.
            - target: the target function value of the current iteration.
        check_func : Callable, optional
            The function to check whether the initialization is legal, by default is 
            (lambda *args, **kwargs: True). The function should take a dictionary as 
            an input, which contains both of the fixed and free variables. 
            The function should return a boolean value. So it will look like:
                check_func(full_dict, **check_kwargs)
        check_kwargs: Dict, optional
            A dictionary of the key word argument, will be passed to the function.
        file_name : str, optional
            The file name to save the OptTraj object, by default None. If not None, the 
            result will be saved as the optimization goes. 
        fixed_para_file_name : str, optional
            The file name to save the fixed_para dictionary, by default None.
        """

        init_x_combined = self.opt_init(
            init_x=init_x,
            check_func=check_func,
            check_kwargs=check_kwargs
        )
        
        init_x_arr = self._x_dict_2_arr(self._normalize_input(init_x_combined))

        init_denorm_x, init_target = self._evaluate_record(init_x_arr)
        result = OptTraj(
            self.free_name_list,
            np.array([self._x_dict_2_arr(init_denorm_x)]),
            np.array([init_target]),
            fixed_para = self.fixed_variables
        )

        opt_call_back = self._construct_call_back(
            callback, result, 
            file_name, fixed_para_file_name,
            callback_kwargs
        )

        tol = self.opt_options.pop("tol", 1e-10)
        opt_kwargs = {
            "bounds": [[0.0, 1.0]] * len(self.free_name_list),
            "callback": opt_call_back,
            "tol": tol,
        }

        # run the scipy optimizer
        if self.optimizer in ("L-BFGS-B", "Nelder-Mead", "Powell", "TNC", "SLSQP"):
            scipy_res = minimize(
                self._opt_func,
                **opt_kwargs,
                x0=init_x_arr,
                method=self.optimizer,
                options=self.opt_options,
            )
        elif self.optimizer == "shgo":
            opt_options = self.opt_options.copy()
            opt_options.update({"f_tol": opt_kwargs.pop("tol")})
            scipy_res = shgo(
                self._opt_func,
                **opt_kwargs,
                options=opt_options,
            )
        elif self.optimizer == "differential evolution":
            scipy_res = differential_evolution(
                self._opt_func,
                **opt_kwargs,
            )
        # elif self.optimizer == "bayesian optimization":
        #     bo_res = bayesian_optimization(
        #         self._opt_func, 
        #         lower=opt_bounds[:, 0], 
        #         upper=opt_bounds[:, 1],
        #         num_iterations=len(self.free_name_list)
        #     )
        #     result = OptTraj(
        #         self.free_name_list,
        #         np.array(bo_res["X"]),
        #         np.array(bo_res["y"]),
        #         np.ones_like(bo_res["y"]) * np.nan,
        #         fixed_para = self.fixed_variables,
        #     )
        else:
            raise ValueError(f"Optimizer {self.optimizer} is not supported.")
        
        # save the result: delete the file with suffix
        if file_name is not None:
            try:
                os.remove(self._running_filename(file_name))
            except FileNotFoundError:
                pass
            result.save(file_name, fixed_para_file_name)

        if not scipy_res.success:
            warnings.warn(f"The optimization fails with fixed parameter {self.fixed_variables}, initial parameter {init_x_combined}")

        result.store_optimizer_result(scipy_res)

        return result


class MultiOpt():
    """
    Run the optimization multiple times. 
    """
    def __init__(
        self,
        optimize: Optimization,
    ):
        """
        """
        self.optimize = optimize

    def _worker(self, args) -> OptTraj:
        idx, call_back, check_func, check_kwargs, save_path, init_x = args

        if save_path is not None:
            save_kwargs = dict(
                file_name=f"{save_path}/{idx}.csv",
                fixed_para_file_name=f"{save_path}/fixed.csv",
            )
        else:
            save_kwargs = {}

        try: 
            result = self.optimize.run(
                init_x=init_x,  
                callback=call_back,
                check_func=check_func,
                check_kwargs=check_kwargs,
                **save_kwargs,
            )

        except ValueError as e:
            if save_path is not None:
                try:
                    os.remove(self.optimize._running_filename(f"{save_path}/{idx}.csv"))
                except FileNotFoundError:
                    pass
            return None

        return result

    def run(
        self,
        run_num: int,
        call_back: Union[Callable, None] = None,
        check_func: Callable = lambda x: True,
        check_kwargs: dict = {},
        save_path: Union[str, None] = None,
        cpu_num: int = 1,
    ) -> MultiTraj:
        """
        Run the optimization multiple times.

        Parameters
        ----------
        run_num : int
            The number of times to run the optimization.
        call_back : Callable, optional
            The function to be called after each iteration, by default None. The function
            should take the following arguments:
            - free_var: the free variables of the current iteration, in the form of a
                dictionary.
            - target: the target function value of the current iteration.
        check_func : Callable, optional
            The function to check whether the initialization is legal, by default
            is (lambda *args, **kwargs: True). The function should take a dictionary as
            an input, which contains both of the fixed and free variables.
            The function should return a boolean value. So it will look like:
                check_func(full_dict, **check_kwargs)
        check_kwargs: Dict, optional
            A dictionary of the key word argument, will be passed to the check function.
        save_path : str, optional
            The path to save the MultiTraj object, by default None. If not None, the
            result will be saved as the optimization goes.
        cpu_num : int, optional
            The number of CPUs to use for the optimization, by default 1.
        """
        if save_path is not None:
            save_path = os.path.normpath(save_path)

        # help to create initial guess externally
        init_x_list = [self.optimize.opt_init({}) for _ in range(run_num)]

        # Use multiprocessing to execute the worker function in parallel
        map_method = get_map_method(cpu_num)
        results = map_method(self._worker, 
            [(idx, call_back, check_func, check_kwargs, save_path, init_x_list[idx]) for idx in range(run_num)])

        # Filter out None results and append valid ones to multi_result
        multi_result = MultiTraj()
        for result in results:
            if result is not None:
                multi_result.append(result)

        return multi_result

