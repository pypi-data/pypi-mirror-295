import os

class StateSpace:
    '''
    This class represents state space equations.
    The inputs are PS - PowerSystem object

    Usage:
    state_space = StateSpace(PS)
    state_space.print_equations('Equations/SMTLLoad.txt')
    state_space.print_vector_x('Equations/SMTLLoad.txt')

    state_space.write_equations('Equations/SMTLLoad.txt')
    state_space.write_vector_x('Equations/SMTLLoad.txt')
    '''

    def __init__(self, system_name, set_point_outputs, set_point_output_equations, controllable_inputs, control_input_equations, internal_inputs, internal_equations, state_variable_derivatives, state_space_equations, desired_state_variable_derivatives, desired_state_space, state_variables, desired_state_variables):
        self.system_name = system_name
        self.SetPointOutputs = set_point_outputs
        self.SetPointOutputEquations = set_point_output_equations
        self.ControllableInputs = controllable_inputs
        self.ControlInputEquations = control_input_equations
        self.InternalInputs = internal_inputs
        self.InternalEquations = internal_equations
        self.StateVariableDerivatives = state_variable_derivatives
        self.StateSpaceEquations = state_space_equations
        self.DesiredStateVariableDerivatives = desired_state_variable_derivatives
        self.DesiredStateSpace = desired_state_space
        self.StateVariables = state_variables
        self.DesiredStateVariables = desired_state_variables

    @classmethod
    def from_power_system(cls, PS):
        return cls(
            system_name=PS.system_name,
            set_point_outputs=PS.SetPointOutputs,
            set_point_output_equations=PS.SetPointOutputEquations,
            controllable_inputs=PS.ControllableInputs,
            control_input_equations=PS.ControlInputEquations,
            internal_inputs=PS.InternalInputs,
            internal_equations=PS.InternalEquations,
            state_variable_derivatives=PS.StateVariableDerivatives,
            state_space_equations=PS.StateSpaceEquations,
            desired_state_variable_derivatives=PS.DesiredStateVariableDerivatives,
            desired_state_space=PS.DesiredStateSpace,
            state_variables=PS.StateVariables,
            desired_state_variables=PS.DesiredStateVariables
        )

    @classmethod
    def from_module(cls, module):
        return cls(
            system_name=module.IndexName,
            set_point_outputs=module.SetPoints,
            set_point_output_equations=module.SetPointOutputEquations,
            controllable_inputs=module.ControllableInputs,
            control_input_equations=module.ControlInputEquations,
            internal_inputs=module.InternalInputs,
            internal_equations=module.InternalEquations,
            state_variable_derivatives=module.StateVariableDerivatives,
            state_space_equations=module.StateSpaceEquations,
            desired_state_variable_derivatives=module.DesiredStateVariableDerivatives,
            desired_state_space=module.DesiredStateSpace,
            state_variables=module.StateVariables,
            desired_state_variables=module.DesiredStateVariables
        )

    # TODO: Implement the __eq__ method

    def print_equations(self):
        '''
        Prints out the interconnected state space equations.
        '''
        print(f'Power System: {self.system_name}\n')
        # Print the set point equations
        print("Set Point Outputs:")
        for output, equation in zip(self.SetPointOutputs, self.SetPointOutputEquations):
            print(f'{output} = {equation}\n')
        # Print the controllable input equations
        print("Controllable Inputs:")
        for input, equation in zip(self.ControllableInputs, self.ControlInputEquations):
            print(f'{input} = {equation}\n')
        # Print the internal input equations
        print("Internal Inputs:")
        for input, equation in zip(self.InternalInputs, self.InternalEquations):
            print(f'{input} = {equation}\n')
        # Print the state space equations
        print("State Space Equations:")
        for derivative, state_space in zip(self.StateVariableDerivatives, self.StateSpaceEquations):
            print(f'{derivative} = {state_space}\n')
        # Print the desired state space equations (used for control)
        print("Desired State Space Equations:")
        for derivative, state_space in zip(self.DesiredStateVariableDerivatives, self.DesiredStateSpace):
            print(f'{derivative} = {state_space}\n')

    def write_equations(self, filename=None):
        '''
        Writes out the interconnected state space equations to a file.
        '''
        if not filename:
            filename = f'{self.system_name}_Equations.txt'
        # Check if directory exists, if not, make it
        os.makedirs(os.path.dirname('results/equations/' + filename), exist_ok=True)

        with open('results/equations/' + filename, 'w') as f: # Empties out file contents before writing!
            # Write the set point equations
            for output, equation in zip(self.SetPointOutputs, self.SetPointOutputEquations):
                f.write(f'{output} = {equation}\n')
            # Write the controllable input equations
            for input, equation in zip(self.ControllableInputs, self.ControlInputEquations):
                f.write(f'{input} = {equation}\n')
            # Write the internal input equations
            for input, equation in zip(self.InternalInputs, self.InternalEquations):
                f.write(f'{input} = {equation}\n')
            # Write the state space equations
            for derivative, state_space in zip(self.StateVariableDerivatives, self.StateSpaceEquations):
                f.write(f'{derivative} = {state_space}\n')
            # Write the desired state space equations (used for control)
            for derivative, state_space in zip(self.DesiredStateVariableDerivatives, self.DesiredStateSpace):
                f.write(f'{derivative} = {state_space}\n')

    def print_vector_x(self):
        '''
        Prints out the interconnected state space equations (dx) in a form suitable for 
        running the simulation directly. Also assigns value of each element of the 
        vector (x) into the respective state variables.
        '''
        print(f'Power System: {self.system_name}\n')
        # State variables
        print('State Variables:')
        for i, variable in enumerate(self.StateVariables):
            print(f'{variable} = x({i})')
        # Desired state variables
        print('Desired State Variables:')
        for i, variable in enumerate(self.DesiredStateVariables):
            print(f'{variable} = x({i+len(self.StateVariables)})')
        # Set Point outputs
        print('Set Point Outputs:')
        for output, equation in zip(self.SetPointOutputs, self.SetPointOutputEquations):
            print(f'{output} = {equation}')
        # Print controllable input expressions
        print('Controllable Inputs:')
        for input, equation in zip(self.ControllableInputs, self.ControlInputEquations):
            print(f'{input} = {equation}')
        # Print internal input expressions
        print('Internal Inputs:')
        for input, equation in zip(self.InternalInputs, self.InternalEquations):
            print(f'{input} = {equation}')
        # Print state space equations
        print('State Space Equations:')
        for derivative, state_space in zip(self.StateVariableDerivatives, self.StateSpaceEquations):
            print(f'{derivative} = {state_space}')
        # Print desired state space equations
        print('Desired State Space Equations:')
        for derivative, state_space in zip(self.DesiredStateVariableDerivatives, self.DesiredStateSpace):
            print(f'{derivative} = {state_space}')
        # Return dx vector
        print('dx = [')
        # State variable derivatives
        for derivative in self.StateVariableDerivatives:
            print(derivative)
        # Desired state variable derivatives
        for derivative in self.DesiredStateVariableDerivatives:
            print(derivative)
        print(']')

    def write_vector_x(self, filename=None):
        '''
        Writes the interconnected state space equations (dx) into a file in a form 
        suitable for running the simulation directly. Also assigns value of each element 
        of the vector (x) into the respective state variables.
        '''
        if not filename:
            filename = f'{self.system_name}_Equations.txt'
            
        # Check if directory exists, if not, make it
        os.makedirs(os.path.dirname('results/equations/' + filename), exist_ok=True)

        with open('results/equations/' + filename, 'a') as f:
            # State variables
            for i, variable in enumerate(self.StateVariables):
                f.write(f'{variable} = x({i})\n')
            # Desired state variables
            for i, variable in enumerate(self.DesiredStateVariables):
                f.write(f'{variable} = x({i+len(self.StateVariables)})\n')
            # Set Point outputs
            for output, equation in zip(self.SetPointOutputs, self.SetPointOutputEquations):
                f.write(f'{output} = {equation}\n')
            # Write controllable input expressions
            for input, equation in zip(self.ControllableInputs, self.ControlInputEquations):
                f.write(f'{input} = {equation}\n')
            # Write internal input expressions
            for input, equation in zip(self.InternalInputs, self.InternalEquations):
                f.write(f'{input} = {equation}\n')
            # Write state space equations
            for derivative, state_space in zip(self.StateVariableDerivatives, self.StateSpaceEquations):
                f.write(f'{derivative} = {state_space}\n')
            # Write desired state space equations
            for derivative, state_space in zip(self.DesiredStateVariableDerivatives, self.DesiredStateSpace):
                f.write(f'{derivative} = {state_space}\n')
            # Return dx vector
            f.write('dx = [')
            # State variable derivatives
            for derivative in self.StateVariableDerivatives:
                f.write(f'{derivative}\n')
            # Desired state variable derivatives
            for derivative in self.DesiredStateVariableDerivatives:
                f.write(f'{derivative}\n')
            f.write(']\n')
