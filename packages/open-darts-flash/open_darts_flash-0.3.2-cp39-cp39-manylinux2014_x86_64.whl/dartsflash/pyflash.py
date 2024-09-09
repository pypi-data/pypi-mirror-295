import numpy as np
import xarray as xr

import dartsflash.libflash
from dartsflash.libflash import FlashParams, EoSParams, EoS
from dartsflash.mixtures import Mixture, ConcentrationUnits as cu


class PyFlash:
    f: dartsflash.libflash.Flash = None

    def __init__(self, mixture: Mixture):
        self.mixture = mixture
        self.flash_params = FlashParams(mixture.comp_data)

        self.components = mixture.comp_data.components
        self.ions = mixture.comp_data.ions
        self.nc = mixture.comp_data.nc
        self.ni = mixture.comp_data.ni
        self.ns = mixture.comp_data.ns
        self.nv = self.ns + 2  # NC + 2 state specifications
        self.np_max = mixture.np_max

        self.eos = {}

        self.H2O_idx = self.components.index("H2O") if "H2O" in self.components else None

    def add_eos(self, eos_name: str, eos: EoS, eos_range: dict = None, initial_guesses: list = None,
                stability_tol: float = None, switch_tol: float = None, line_tol: float = None, max_iter: int = None,
                line_iter: int = None, root_flag: EoSParams.RootFlag = EoSParams.STABLE, preferred_roots: list = None,
                active_components: list = None):
        """
        Method to add EoS object and set EoS-specific parameters

        :param eos_name: Map key for EoS object
        :type eos_name: str
        :param eos: Equation of state
        :type eos: EoS
        :param eos_range: Composition range of applicability of EoS
        :type eos_range: dict
        :param initial_guesses: Set of initial guesses for EoS
        :type initial_guesses: list
        :param stability_tol: Stability test objective function convergence criterion
        :type stability_tol: float
        :param switch_tol: Switch to Newton criterion
        :type switch_tol: float
        :param line_tol: Line-search iteration tolerance
        :type line_tol: float
        :param max_iter: Maximum number of stability test iterations
        :type max_iter: int
        :param line_iter: Maximum number of stability line-search iterations
        :type line_iter: int
        :param root_flag: RootFlag enum for roots to be selected in stability test. 0) STABLE, 1) MIN, 2) MAX, 3) MINMAX
        :type root_flag: EoSParams.RootFlag
        :param preferred_roots:
        :type preferred_roots: list
        """
        eos_range = eos_range if eos_range is not None else {}
        for i, zrange in eos_range.items():
            eos.set_eos_range(i, zrange)
        
        if preferred_roots is not None:
            preferred_roots = [preferred_roots] if not isinstance(preferred_roots, (list, np.ndarray)) else preferred_roots
            for preferred_root in preferred_roots:
                i, x, flag = preferred_root
                eos.set_preferred_roots(i, x, flag)

        self.eos[eos_name] = eos
        self.flash_params.add_eos(eos_name, eos)

        params = self.flash_params.eos_params[eos_name]
        params.initial_guesses = initial_guesses if initial_guesses is not None else params.initial_guesses
        params.stability_tol = stability_tol if stability_tol is not None else params.stability_tol
        params.stability_switch_tol = switch_tol if switch_tol is not None else params.stability_tol
        params.stability_line_tol = line_tol if line_tol is not None else params.stability_line_tol
        params.stability_max_iter = max_iter if max_iter is not None else params.stability_max_iter
        params.stability_line_iter = line_iter if line_iter is not None else params.stability_line_iter

        params.root_flag = root_flag

        if active_components is not None:
            params.set_active_components(active_components)

    def init_flash(self, stabilityflash: bool = True, eos: list = None, initial_guess: list = None):
        if stabilityflash:
            self.f = dartsflash.libflash.Flash(self.flash_params, self.np_max)
        else:
            self.f = dartsflash.libflash.NegativeFlash(self.flash_params, eos, initial_guess)

    def get_state(self, state_variables, variable_idxs, idxs, mole_fractions, comp_in_dims,
                  swap_state_spec: bool = False, concentrations: dict = None, concentration_unit: cu = cu.MOLALITY):
        # Get state
        j = 0
        state = np.empty(self.nv)
        for ith_var, ith_idx in enumerate(variable_idxs):
            if hasattr(state_variables[ith_var], "__len__"):
                state[ith_idx] = state_variables[ith_var][idxs[j]]
                j += 1
            else:
                state[ith_idx] = state_variables[ith_var]

        # Swap state specification
        if swap_state_spec:
            spec = state[0], state[1]
            state[1], state[0] = spec

        # If mole fractions, normalize mole numbers
        if mole_fractions:
            sum_zc = np.sum(state[comp_in_dims])
            if sum_zc >= 1.-1e-15:
                return None
            else:
                for ith_comp in range(self.nc):
                    if (ith_comp + 2) not in comp_in_dims:
                        state[ith_comp + 2] *= (1. - sum_zc)

        # Calculate composition with concentrations
        if concentrations is not None:
            state[2:] = self.mixture.calculate_concentrations(state[2:self.nc+2], mole_fractions, concentrations=concentrations,
                                                              concentration_unit=concentration_unit)
        else:
            assert self.ni == 0, "Ions specified but no concentrations"

        return state

    def evaluate_full_space(self, state_spec: dict, compositions: dict, evaluate, output_arrays: dict, mole_fractions: bool = True,
                            dims_order: list = None, concentrations: dict = None, concentration_unit: cu = cu.MOLALITY,
                            print_state: bool = True):
        """
        This is a loop over all specified states to which each DARTSFlash subroutine can be passed

        :param state_spec: Dictionary containing state specification
        :param compositions: Dictionary containing variable dimensions
        :param mole_fractions: Switch for mole fractions in state
        :param evaluate: Callable with set of methods to evaluate
        :param output_arrays: Array of corresponding shape to evaluate()
        :param dims_order: Option to change order of execution of for loops over dimensions
        :param concentrations: Dictionary of concentrations
        :param concentration_unit: Unit for concentration. 0/MOLALITY) molality (mol/kg H2O), 1/WEIGHT) Weight fraction (-)
        :param print_state: Switch for printing state and progress
        """
        assert self.flash_params.eos_params is not {}, "No EoS(Params) object has been defined"

        # Find dimensions and constants
        dimensions = {}
        constants = {}
        for var, dim in dict(list(state_spec.items()) + list(compositions.items())).items():
            if isinstance(dim, (list, np.ndarray)):
                dimensions[var] = dim
            else:
                constants[var] = dim
        dims_order = list(dimensions.keys()) if dims_order is None else dims_order
        assert len(dims_order) == len(dimensions), "Incompatible order of dimensions"

        # Create xarray DataArray to store results
        array_shape = [len(dimensions[var]) for var in dims_order]
        n_dims = [i for i, dim in enumerate(dims_order)]
        n_points = np.prod(array_shape)

        # Know where to find state variables/constants
        state_variables = [dimensions[var] for var in dims_order] + [constant for var, constant in constants.items()]
        comp_in_dims = [i + 2 for i, comp in enumerate(self.components) if comp in dimensions.keys()]
        variable_idxs = [(list(state_spec.keys()) + self.components).index(var)
                         for i, var in enumerate(dims_order + list(constants.keys()))]

        # If state spec is not in right order for function call (P,X,n) or (V,X,n), swap
        ls = list(state_spec.keys())
        first_spec = "pressure" if "pressure" in ls else "volume"
        second_spec = ls[0] if ls[1] == first_spec else ls[1]
        if ls != [first_spec, second_spec]:
            swap_state_spec = True
        else:
            swap_state_spec = False

        transpose_data = [i for i, dim in enumerate(dims_order + ["array"])]
        data_dims = dims_order
        if dims_order.index(second_spec) > dims_order.index(first_spec):
            idx1, idx2 = dims_order.index(first_spec), dims_order.index(second_spec)
            transpose_data[idx1], transpose_data[idx2] = idx2, idx1
            data_dims[idx1], data_dims[idx2] = data_dims[idx2], data_dims[idx1]

        # Create data dict and coords for xarray DataArray to store results
        data = {prop: (data_dims + [prop + '_array'] if array_len > 1 else data_dims,
                       np.full(tuple(array_shape + [array_len] if array_len > 1 else array_shape), np.nan))
                for prop, array_len in output_arrays.items()}
        coords = {dimension: xrange for dimension, xrange in dimensions.items()}

        # Loop over dimensions to create state and evaluate function
        idxs = np.array([0 for i in n_dims])
        for point in range(n_points):
            # Get state
            state = self.get_state(state_variables=state_variables, variable_idxs=variable_idxs, idxs=idxs,
                                   mole_fractions=mole_fractions, comp_in_dims=comp_in_dims, swap_state_spec=swap_state_spec,
                                   concentrations=concentrations, concentration_unit=concentration_unit)
            if print_state and state is not None:
                print("\rProgress: {}/{}".format(point+1, n_points), "idxs:", idxs, "state:", [float("%.4f" % i) for i in state], end='')

            # Evaluate method_to_evaluate(state)
            if state is not None:
                output_data = evaluate(state)
                for prop, method in output_data.items():
                    method_output = method()
                    if isinstance(data[prop][1][tuple(idxs)], (list, np.ndarray)):
                        try:
                            data[prop][1][tuple(idxs)][:len(method_output)] = method_output
                        except ValueError as e:
                            print(e.args[0])
                            data[prop][1][tuple(idxs)][:] = np.nan
                    else:
                        data[prop][1][tuple(idxs)] = method_output

            # Increment idxs
            idxs[0] += 1
            for i in n_dims[1:]:
                if idxs[i-1] == array_shape[i-1]:
                    idxs[i-1] = 0
                    idxs[i] += 1
                else:
                    break

        # Save data
        results = xr.Dataset(coords=coords)
        for var_name in data.keys():
            array_dims = np.ndim(data[var_name][1])
            results[var_name] = (data[var_name][0], np.transpose(data[var_name][1], tuple(transpose_data[:array_dims])))

        return results

    def evaluate_flash_1c(self, state_spec: dict, dims_order: list = None, print_state: bool = True):
        """
        Method to evaluate single-component flash

        :param state_spec: Dictionary containing state specification
        :param dims_order: Option to change order of execution of for loops over dimensions
        :param print_state: Switch for printing state and progress
        """
        output_arrays = {'p': 1, 'T': 1, 'nu': self.np_max, 'np': 1, 'eos': self.np_max}

        def evaluate(state):
            error = self.f.evaluate(state[0], state[1])
            flash_results = self.f.get_flash_results()
            output_data = {"p": lambda results=flash_results: results.p,
                           "T": lambda results=flash_results: results.T,
                           "nu": lambda results=flash_results: results.nu,
                           "np": lambda results=flash_results: results.np,
                           # "eos": lambda results=flash_results: results.eos
                           }
            return output_data

        return self.evaluate_full_space(state_spec=state_spec, compositions={self.components[0]: 1.}, evaluate=evaluate,
                                        output_arrays=output_arrays, dims_order=dims_order, print_state=print_state)

    def evaluate_flash(self, state_spec: dict, compositions: dict, mole_fractions: bool, dims_order: list = None,
                       concentrations: dict = None, concentration_unit: cu = cu.MOLALITY, print_state: bool = True):
        """
        Method to evaluate multi-component flash

        :param state_spec: Dictionary containing state specification
        :param compositions: Dictionary containing variable dimensions
        :param mole_fractions: Switch for mole fractions in state
        :param dims_order: Option to change order of execution of for loops over dimensions
        :param concentrations: Dictionary of concentrations
        :param concentration_unit: Unit for concentration. 0/MOLALITY) molality (mol/kg H2O), 1/WEIGHT) Weight fraction (-)
        :param print_state: Switch for printing state and progress
        """
        output_arrays = {'p': 1, 'T': 1, 'nu': self.np_max, 'np': 1, 'X': self.np_max * self.ns, 'eos': self.np_max}

        def evaluate(state):
            error = self.f.evaluate(state[0], state[1], state[2:])
            flash_results = self.f.get_flash_results()
            output_data = {"p": lambda results=flash_results: results.p,
                           "T": lambda results=flash_results: results.T,
                           "nu": lambda results=flash_results: results.nu,
                           "np": lambda results=flash_results: results.np,
                           "X": lambda results=flash_results: results.X,
                           # "eos": lambda results=flash_results: results.eos
                           }
            return output_data

        return self.evaluate_full_space(state_spec=state_spec, compositions=compositions, mole_fractions=mole_fractions,
                                        evaluate=evaluate, output_arrays=output_arrays, dims_order=dims_order,
                                        concentrations=concentrations, concentration_unit=concentration_unit,
                                        print_state=print_state)

    def evaluate_properties_1p(self, state_spec: dict, compositions: dict, mole_fractions: bool,
                               properties_to_evaluate: dict, dims_order: list = None, concentrations: dict = None,
                               concentration_unit: cu = cu.MOLALITY, print_state: bool = True):
        """
        Method to evaluate single phase properties

        :param state_spec: Dictionary containing state specification
        :param compositions: Dictionary containing variable dimensions
        :param mole_fractions: Switch for mole fractions in state
        :param properties_to_evaluate: Dictionary of methods to evaluate
        :param dims_order: Option to change order of execution of for loops over dimensions
        :param concentrations: Dictionary of concentrations
        :param concentration_unit: Unit for concentration. 0/MOLALITY) molality (mol/kg H2O), 1/WEIGHT) Weight fraction (-)
        :param print_state: Switch for printing state and progress
        """
        output_arrays = {}
        for prop_name, method in properties_to_evaluate.items():
            output_sample = method(0, 0, np.ones(self.ns))
            output_arrays[prop_name] = len(output_sample) if hasattr(output_sample, '__len__') else 1

        def evaluate(state):
            output_data = {}
            for property_name, method in properties_to_evaluate.items():
                result = method(state[0], state[1], state[2:])
                output_data[property_name] = lambda res=result: res
            return output_data

        return self.evaluate_full_space(state_spec=state_spec, compositions=compositions, mole_fractions=mole_fractions,
                                        evaluate=evaluate, output_arrays=output_arrays, dims_order=dims_order,
                                        concentrations=concentrations, concentration_unit=concentration_unit,
                                        print_state=print_state)

    def evaluate_properties_np(self, flash_results: xr.Dataset, properties_to_evaluate: dict, print_state: bool = True):
        return

    def evaluate_properties_of_mixing(self, state_spec: dict, compositions: dict, mole_fractions: bool,
                                      properties_to_evaluate: dict, dims_order: list = None, 
                                      concentrations: dict = None, concentration_unit: cu = cu.MOLALITY,
                                      print_state: bool = True):
        """
        Method to evaluate properties of mixing

        :param state_spec: Dictionary containing state specification
        :param compositions: Dictionary containing variable dimensions
        :param mole_fractions: Switch for mole fractions in state
        :param properties_to_evaluate: Dictionary of methods to evaluate
        :param dims_order: Option to change order of execution of for loops over dimensions
        :param concentrations: Dictionary of concentrations
        :param concentration_unit: Unit for concentration. 0/MOLALITY) molality (mol/kg H2O), 1/WEIGHT) Weight fraction (-)
        :param print_state: Switch for printing state and progress
        """
        output_arrays = {property_name: 1 for property_name in properties_to_evaluate.keys()}

        def evaluate(state):
            output_data = {}
            flash_params = self.flash_params
            for property_name, method in properties_to_evaluate.items():
                pure = eval("flash_params." + property_name + "_pure")(state[0], state[1])
                result = method(state[0], state[1], state[2:])
                output_data[property_name] = lambda res=result, pu=pure: res - np.sum(pu * state[2:])
            return output_data

        return self.evaluate_full_space(state_spec=state_spec, compositions=compositions, mole_fractions=mole_fractions,
                                        evaluate=evaluate, output_arrays=output_arrays, dims_order=dims_order,
                                        concentrations=concentrations, concentration_unit=concentration_unit,
                                        print_state=print_state)

    def evaluate_stationary_points(self, state_spec: dict, compositions: dict, mole_fractions: bool, dims_order: list = None,
                                   concentrations: dict = None, concentration_unit: cu = cu.MOLALITY, print_state: bool = True):
        """
        Method to evaluate stationary points

        :param state_spec: Dictionary containing state specification
        :param compositions: Dictionary containing variable dimensions
        :param mole_fractions: Switch for mole fractions in state
        :param dims_order: Option to change order of execution of for loops over dimensions
        :param concentrations: Dictionary of concentrations
        :param concentration_unit: Unit for concentration. 0/MOLALITY) molality (mol/kg H2O), 1/WEIGHT) Weight fraction (-)
        :param print_state: Switch for printing state and progress
        """
        output_arrays = {'Y': self.np_max * self.nc, 'tot_sp': 1, 'neg_sp': 1, 'eos': self.np_max}

        def evaluate(state):
            stationary_points = self.f.find_stationary_points(state[0], state[1], state[2:])
            output_data = {"Y": lambda spts=stationary_points: np.array([sp.Y for sp in spts]).flatten(),
                           "tot_sp": lambda spts=stationary_points: len(spts),
                           "neg_sp": lambda spts=stationary_points: np.sum([sp.tpd < -1e-8 for sp in spts]),
                           "eos": lambda spts=stationary_points: np.array([sp.eos_name for sp in spts]),
            }
            return output_data

        return self.evaluate_full_space(state_spec=state_spec, compositions=compositions, mole_fractions=mole_fractions,
                                        evaluate=evaluate, output_arrays=output_arrays, dims_order=dims_order,
                                        concentrations=concentrations, concentration_unit=concentration_unit,
                                        print_state=print_state)

    def output_to_file(self, data: xr.Dataset, csv_filename: str = None, h5_filename: str = None):
        """
        Method to write xarray.Dataset to .csv and/or .h5 format

        :param data: Xarray Dataset
        :param csv_filename: Filename to write to .csv format
        :param h5_filename: Filename to write to .h5 format
        """
        if csv_filename is not None:
            df = data.to_dataframe()
            csv_filename = csv_filename + '.csv' if not csv_filename[:-4] == '.csv' else csv_filename
            df.to_csv(csv_filename)

        if h5_filename is not None:
            h5_filename = h5_filename + '.h5' if not h5_filename[:-3] == '.h5' else h5_filename
            data.to_netcdf(h5_filename, engine='h5netcdf')
