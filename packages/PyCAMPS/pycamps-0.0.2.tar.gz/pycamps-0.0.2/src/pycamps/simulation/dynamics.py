import os
import numpy as np
import sympy as sp
from sympy import Matrix, symbols, diag, eye
from scipy.optimize import fsolve, root
from scipy.io import loadmat, savemat
import pickle
from pycamps.simulation.numerical_integration import NumericalIntegration
from pycamps.logger import configure_logging

logger = configure_logging()

class Dynamics:
    def __init__(self, power_system, params_directory=None, custom_module_files=None):
        self.PS = power_system
        self.params = {}
        self.input_states = []
        self.input_equations = []
        self.module_to_params = self.get_required_parameters()
        self.load_new_params(params_directory, custom_module_files)

    def get_required_parameters(self):
        '''
        Create a mapping of each module_name to the parameters required for that module.
        Example: {
                    'G1': ['eqprime_G1', 'omega_G1', ...],
                    'TL_1_2': ['v1_TL_1_2', 'v2_TL_1_2', ...],
                    'L1': ['LL_L1', 'RL_L1', ...]
                }
        '''
        module_to_params = {}

        for module in self.PS.Modules:
            # TODO: This is a hacky way to get the module name, will fix
            module_name = str(module.StateVariables[0]).split('_', 1)[-1]
            module_to_params[module_name] = []
            for param in self.PS.Parameters:
                if str(param).split('_', 1)[-1] == module_name:
                    module_to_params[module_name].append(param)
            for set_point in self.PS.SetPoints:
                if str(set_point).split('_', 1)[-1] in (module_name + '_ref', module_name + '_star'):
                    module_to_params[module_name].append(set_point)
            for controller_gain in self.PS.ControllerGains:
                if str(controller_gain).split('_', 1)[-1] == module_name:
                    module_to_params[module_name].append(controller_gain)
        
        logger.debug(f"Required params for each module: {module_to_params}")
        return module_to_params

    def load_new_params(self, params_directory=None, custom_module_files=None, reference_frame={sp.Symbol('dphidt', real=True): 1, sp.Symbol('phi', real=True): 0}):
        '''
        There are two supported options to load in parameters:
        1. Load in a custom mapping of each module_name to the full file path containing that module's parameters.
        2. Load in parameters from a single directory, where the file name is 'module_name.mat'
            and the parameters are the variables in the file.
        '''
        self.params = {}

        for module_name, required_params in self.module_to_params.items():
            if custom_module_files and module_name in custom_module_files:
                # We expect a full file path for now
                file_path = custom_module_files[module_name]
            elif params_directory: # Going with default naming convention
                file_path = os.path.join(params_directory, f'{module_name}.mat')
            else:
                logger.error(f'Missing parameters for {module_name}')
                raise ValueError(f'Missing parameters for {module_name}')
            param_values = loadmat(file_path)
            logger.debug(f"Fetching params: {required_params} from file: {file_path}")
            for param_name in required_params:
                self.params[param_name] = param_values[str(param_name)].item()
        logger.debug(f"Loaded Params: {self.params}")

        # Generate a list of input states and equations
        self.input_states = sum(self.PS.StateVariables.tolist(), []) + sum(self.PS.DesiredStateVariables.tolist(), []) + sum(self.PS.SetPointOutputs.tolist(), [])
        subs_equations = {}
        self.input_equations = []
        for control_input, equation in zip(self.PS.ControllableInputs, self.PS.ControlInputEquations):
            sub_eq = equation.subs(self.params)
            subs_equations[control_input] = sub_eq
        for internal_input, equation in zip(self.PS.InternalInputs, self.PS.InternalEquations):
            sub_eq = equation.subs(self.params)
            subs_equations[internal_input] = sub_eq
        for equation in self.PS.StateSpaceEquations:
            sub_eq = equation.subs(self.params).subs(subs_equations)
            self.input_equations.append(sub_eq)
        for equation in self.PS.DesiredStateSpace:
            sub_eq = equation.subs(self.params).subs(subs_equations)
            self.input_equations.append(sub_eq)

        for i, equation in enumerate(self.input_equations):
            self.input_equations[i] = equation.subs(reference_frame) # hacky, will fix

        if len(self.input_states) != len(self.input_equations):
            logger.error('Number of states and equations in solve do not match')
            raise ValueError('Number of states and equations do not match')
        
        logger.debug(f'Input States: {self.input_states}')
        eq_string = "-------------------------\n" + "\n".join([f'Equation {i+1}: {eq}' for i, eq in enumerate(self.input_equations)]) + "\n-------------------------"
        logger.debug(f'Input Equations:\n{eq_string}')

    def save_dynamics(self, file_path=None):
        if not file_path:
            file_path = f'Results/Dynamics/Dynamics_{self.PS.system_name}.pkl'
        if not os.path.exists('Results/Dynamics/'):
            os.makedirs('Results/Dynamics/')
        with open(file_path, 'wb') as f:
            pickle.dump(self, f)
        logger.info(f'Saved dynamics object to {file_path}')

    def solve_equilibrium(self, x0=None, options=None, method='fsolve'):
        '''
        Given the system dynamics, solve for the equilibrium values of the system.
        If initial guess x0 is not provided, random values are used.

        Supported methods: 'fsolve', 'hybr', 'lm', 'broyden1', 'broyden2', 'anderson',
          'linearmixing', 'diagbroyden', 'excitingmixing', 'krylov', 'df-sane'
        '''
        logger.info(f'Solving for equilibrium values of {self.PS.system_name}')

        if x0 is None:
            x0 = np.random.randn(len(self.input_states))
        if method not in ['fsolve', 'hybr', 'lm', 'broyden1', 'broyden2', 'anderson', 'linearmixing', 'diagbroyden', 'excitingmixing', 'krylov', 'df-sane']:
            logger.error(f'Invalid method: {method}')
            raise ValueError('Invalid method: {method}')

        if len(x0) != len(self.input_states):
            logger.error('x0 has the wrong length')
            raise ValueError('x0 has the wrong length')

        dynamics_fn = sp.lambdify(self.input_states, self.input_equations, "numpy")
        failed_solve=False
        failed_solve_message = ''
        if method == 'fsolve':
            if options is None:
                options = {'maxfev': 100000 * len(self.input_states), 'xtol': 0.01}
            logger.debug(f'Using fsolve with options: {options}')
            x, info, ier, mesg = fsolve(lambda x: dynamics_fn(*x), x0, full_output=True, **options)
            if ier != 1:
                failed_solve = True
                failed_solve_message = mesg
        else:
            if options is None:
                options = {'maxfev': 100000 * len(self.input_states), 'xtol': 0.01}
            logger.debug(f'Using {method} with options: {options}')
            sol = root(fun=lambda x: dynamics_fn(*x), x0=x0, method=method, options=options)
            if sol.success:
                x = sol.x
            else:
                failed_solve = True
                failed_solve_message = sol.message
        
        if failed_solve:
            logger.error(f'Equilibrium was not found. {failed_solve_message}')
            raise ValueError(f'Equilibrium was not found. { failed_solve_message }')
        
        logger.debug(f"Equilibrium values (should be close to zero): {dynamics_fn(*x)}")
        solution = {}
        for i, state in enumerate(self.input_states):
            solution[str(state)] = x[i]

        # Nicely print the solution dictionary
        solution_str = "-------------------------\n" + "\n".join([f"{key}: {value}" for key, value in solution.items()]) + "\n-------------------------"
        logger.info(f'Equilibrium values:\n{solution_str}')
        
        # Check if directory exists, if not, make it
        os.makedirs(os.path.dirname(f'results/equilibrium/'), exist_ok=True)
        savemat(f'results/equilibrium/{self.PS.system_name}_Solved.mat', solution)
        logger.info(f'Saved equilibrium values to results/equilibrium/{self.PS.system_name}_Solved.mat')

        return x
    
    def simulate_trajectory(self, xf=None, simulation_time=0.1, method='trapezoid_adaptive'):
        '''
        Given the system dynamics, simulate the trajectory of the system.
        If solved values xf is not provided, random values are used.

        Supported methods: 'trapezoid_adaptive', 'trapezoid', 'LSODA', 'RK45',
          'RK23', 'DOP853', 'Radau', 'BDF'
        '''
        logger.info(f'Simulating trajectory of {self.PS.system_name}')

        if xf is None:
            xf = np.random.randn(len(self.input_states))
        if len(xf) != len(self.input_states):
            logger.error('xf has the wrong length')
            raise ValueError('xf has the wrong length')

        dynamics_fn = sp.lambdify(self.input_states, self.input_equations, "numpy")
        integrator = NumericalIntegration(dynamics_fn)
        time, x_span, _ = integrator.integrate([0, simulation_time], xf, method=method)

        states = {}
        for i, state in enumerate(self.input_states):
            states[str(state)] = x_span[:,i]
    
        # Check if directory exists, if not, make it
        os.makedirs(os.path.dirname(f'results/trajectory/'), exist_ok=True)
        savemat(f'results/trajectory/{self.PS.system_name}_Simulation.mat', states)
        logger.info(f'Saved trajectory values to results/trajectory/{self.PS.system_name}_Simulation.mat')

        return time, states
    
    def linearized_analysis(self, xf=None):
        '''
        Given the system dynamics, perform a linearized analysis of the system.
        If solved values xf is not provided, random values are used.
        '''
        logger.info(f'Performing linearized analysis of {self.PS.system_name}')

        if xf is None:
            xf = np.random.randn(len(self.input_states))
            logger.debug(f'Generated random xf: {xf}')
        else:
            logger.debug(f'Using provided xf: {xf}')
        if len(xf) != len(self.input_states):
            logger.error('xf has the wrong length')
            raise ValueError('xf has the wrong length')

        dx = Matrix(self.input_equations)
        x = Matrix(self.input_states)
        logger.debug(f'x: {x}')
        logger.debug(f'dx: {dx}')

        # Compute the Jacobian matrix
        A = Matrix(dx).jacobian(x)
        A = A.evalf(10)
        logger.debug(f'A: {A}')

        # Substitute x with x0
        A1 = A.subs(dict(zip(x, xf)))
        A1 = A1.evalf(4)
        logger.debug(f'A1: {A1}')

        # Compute eigenvalues and eigenvectors
        eigen_data = A1.eigenvects()
        lam = np.array([eigen[0] for eigen in eigen_data], dtype=complex)
        v = np.array([vec for eigen in eigen_data for vec in eigen[2]], dtype=complex).T[0]
        logger.debug(f'Eigenvalues: {lam}')
        logger.debug(f'Eigenvectors: {v}')

        # Compute the inverse transpose of eigenvectors
        u = np.linalg.inv(v).T
        logger.debug(f'Inverse Transpose of Eigenvectors: {u}')

        # Find indices of unstable eigenvalues
        ind_lam = np.where(np.real(lam) > 0)[0]
        logger.debug(f'Indices of unstable eigenvalues: {ind_lam}')

        if ind_lam.size > 0:
            logger.info('Unstable EigenValues')
            unstable_eigenvalues = lam[ind_lam]
            logger.info(unstable_eigenvalues.round(4))
            
            # Compute participation factors
            pf = np.real(u * v)
            pf_sort = np.zeros_like(pf)
            ind_st = np.zeros_like(pf, dtype=int)
            
            for i in range(pf.shape[1]):
                pf_list = pf[:, i].tolist()
                sorted_pf = sorted(zip(pf_list, range(pf.shape[0])), reverse=True)
                pf_sort[:, i], ind_st[:, i] = zip(*sorted_pf)
            
            logger.info('Sub-matrix of participation factor:')
            sub_pf = pf_sort[:2, ind_lam]
            logger.info(sub_pf)
            logger.info('States contributing to instability:')
            states = [x[i] for i in ind_st[:2, ind_lam].flatten()]
            logger.info(states)

            return np.array(A1).astype(float), unstable_eigenvalues, sub_pf, states
        else:
            logger.info('No unstable eigenvalues')
            return np.array(A1).astype(float), None, None, None


        