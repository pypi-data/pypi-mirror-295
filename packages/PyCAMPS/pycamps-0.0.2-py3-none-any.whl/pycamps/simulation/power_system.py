import sympy as sp
import numpy as np
from pycamps.simulation.state_space import StateSpace
from pycamps.modules.short_line import ShortLine
from pycamps.modules.long_line import LongLine
from pycamps.modules.sm_one_axis import SMOneAxis
from pycamps.modules.pq_load import PQLoad
from pycamps.logger import configure_logging

# Configure logging
logger = configure_logging()

class PowerSystem:
    '''PowerSystem class for the power system model'''
    def __init__(self, system_name, Modules, Buses):
        self.system_name = system_name
        self.Modules = Modules
        self.G = self.produce_g_matrix(Modules, Buses)
        self.StateVariableDerivatives = sp.Matrix([])
        self.StateSpaceEquations = sp.Matrix([])
        self.DesiredStateVariableDerivatives = sp.Matrix([])
        self.DesiredStateSpace = sp.Matrix([])
        self.ControllableInputs = sp.Matrix([])
        self.InternalInputs = sp.Matrix([])
        self.ControlInputEquations = sp.Matrix([])
        self.SetPointOutputs = sp.Matrix([])
        self.SetPointOutputEquations = sp.Matrix([])
        self.StateVariables = sp.Matrix([])
        self.DesiredStateVariables = sp.Matrix([])
        self.InternalEquations = sp.Matrix([])
        self.Parameters = sp.Matrix([])
        self.SetPoints = sp.Matrix([])
        self.ControllerGains = sp.Matrix([])
        self.Units = sp.Matrix([])
        self.StateSpaceObject = None
        self.KCLEquations = None
        
        if Modules is not None:
            self.produce_state_space()
            logger.info(f"Produced state space for {system_name}")

    def produce_g_matrix(self, modules, buses):
        """
        Forms the G-matrix for the given system.
        - modules: ordered list of all modules in the system
        - buses: a list containing each individual Bus with unordered list
                of modules at the Bus
        """
        G = []
        for bus in buses:
            ind = ind1 = 0
            for mod in bus:
                if isinstance(mod[0], (ShortLine, SMOneAxis)):
                    ind = 1
                if isinstance(mod[0], PQLoad):
                    ind1 = 1
            if ind and ind1:
                logger.warning('PQ load model forms as inductor cutset. Results might be inappropriate')
            
            G_temp = np.array([]).reshape(2, 0)
            for module in modules:
                two_port_module = isinstance(module, (LongLine, ShortLine))
                logger.debug(f"Module {module} is a two port module")
                member = 0
                side = None
                for mod in bus:
                    if module == mod[0]:
                        member = 1
                        if two_port_module:
                            side = mod[1]
                        break
                
                if member:
                    if two_port_module:
                        module_g = np.array([[1, 0, 0, 0], [0, 1, 0, 0]]) if side == 'L' else np.array([[0, 0, 1, 0], [0, 0, 0, 1]])
                    else:
                        module_g = np.array([[1, 0], [0, 1]])
                else:
                    module_g = np.zeros((2, 4)) if two_port_module else np.zeros((2, 2))
                
                G_temp = np.hstack((G_temp, module_g))

            G.append(G_temp)
        
        G = np.vstack(G)
        logger.info(f'Produced G-matrix:\n{G}')
        return G
    
    def produce_state_space(self):
        def find(variable, match):
            for i, value in enumerate(variable):
                if value == match:
                    return i
            logger.error(f"Could not find match {match} in {variable}")
            raise IndexError('No match found')
        
        def getfield(dict_obj, key):
            return dict_obj[key]
        
        def setdiff(a, b):
            return list(set(a) - set(b))
        
        def isempty(matrix):
            return matrix.shape == (0, 0)
        
        StateVariableDerivatives = sp.Matrix()
        StateSpaceEquations = sp.Matrix()
        DesiredStateVariableDerivatives = sp.Matrix()
        DesiredStateSpace = sp.Matrix()
        ControllableInputs = sp.Matrix()
        InternalInputs = sp.Matrix()
        ControlInputEquations = sp.Matrix()
        InternalEquations = sp.Matrix()
        SetPointOutputs = sp.Matrix()
        SetPointOutputEquations = sp.Matrix()
        StateVariables = sp.Matrix()
        DesiredStateVariables = sp.Matrix()
        Parameters = sp.Matrix()
        SetPoints = sp.Matrix()
        ControllerGains = sp.Matrix()
        Units = []

        # Form the matrices of all port voltages/currents/input/states
        I = sp.Matrix()
        V = sp.Matrix()
        PortInputs = sp.Matrix()
        PortStates = sp.Matrix()
        PortStates_Time = sp.Matrix()
        PortStateDerivatives = sp.Matrix()
        PortOutputTypes = []

        for module in self.Modules:
            logger.debug(f"Processing module {module}")
            StateVariableDerivatives = StateVariableDerivatives.col_join(module.StateVariableDerivatives)
            StateSpaceEquations = StateSpaceEquations.col_join(module.StateSpaceEquations) ###
            DesiredStateVariableDerivatives = DesiredStateVariableDerivatives.col_join(module.DesiredStateVariableDerivatives.T)
            DesiredStateSpace = DesiredStateSpace.col_join(module.DesiredStateSpace)
            if not isempty(module.ControllableInputs):
                ControllableInputs = ControllableInputs.col_join(module.ControllableInputs)
            if not isempty(module.InternalInputs):
                InternalInputs = InternalInputs.col_join(module.InternalInputs)
            if not isempty(module.ControlInputEquations):
                ControlInputEquations = ControlInputEquations.col_join(module.ControlInputEquations)
            if not isempty(module.InternalEquations):
                InternalEquations = InternalEquations.col_join(module.InternalEquations)
            if not isempty(module.SetPointOutputs):
                SetPointOutputs = SetPointOutputs.col_join(module.SetPointOutputs)
            SetPointOutputEquations = SetPointOutputEquations.col_join(module.SetPointOutputEquations)
            StateVariables = StateVariables.col_join(module.StateVariables)
            DesiredStateVariables = DesiredStateVariables.col_join(module.DesiredStateVariables.T)
            Parameters = Parameters.col_join(module.Parameters)
            if not isempty(module.SetPoints):
                SetPoints = SetPoints.col_join(module.SetPoints)
            if not isempty(module.ControllerGains):
                ControllerGains = ControllerGains.col_join(module.ControllerGains)
            Units.extend(module.Units)
            I = I.col_join(module.PortCurrents) # I'm skipping the extra transposes here
            V = V.col_join(module.PortVoltages) # Assuming vertical vectors
            PortInputs = PortInputs.row_join(module.PortInputs.T) # I'm assuming all of these are horizontal
            PortStates = PortStates.row_join(module.PortStates.T)
            PortStates_Time = PortStates_Time.row_join(module.PortStates_Time.T)
            PortStateDerivatives = PortStateDerivatives.row_join(module.PortStateDerivatives.T)
            PortOutputTypes.extend(module.PortOutputTypes)

        OriginalStateVariables = StateVariables

        if self.G is not None and not self.G.size == 0:
            # Create custom print function that uses latex dictionary
            self.KCLEquations = self.G * I
            kcl_equations_str = "-------------------------\n" + "\n".join([str(eq) + " = 0" for eq in self.KCLEquations]) + "\n-------------------------"
            logger.info(f'The KCL constraints between modules are:\n{kcl_equations_str}')
        
        PortStates_TimeDerivatives = sp.diff(PortStates_Time, sp.symbols('t', real=True))
        PortStatesTimeSubstituteDict = {PortStates[i]: PortStates_Time[i] for i in range(len(PortStates))}
        PortStatesDerivativesSubstituteDict = {PortStates_TimeDerivatives[i]: PortStateDerivatives[i] for i in range(len(PortStates))}

        StateSpaceEquationsPythonList = []
        StateSpaceEquationsPythonListBeforeSubs = []
        InputsSolutionList = []
        ToRemoveIndices = []
        for row in range(self.G.shape[0]):
            logger.debug(f'Processing junction {row}')
            # For each junction, express the port inputs to one module in terms of the
            # port states of the connecting module(s)
            RowTemp = sp.Matrix(self.G[row, :]).T
            PortsAtJunction = [i for i, value in enumerate(RowTemp) if not value.is_zero]

            AllCapacitorLoop = False # Check for an all-capacitor loop at the junction
            AllInductorCutset = False # Check for an all-inductor cutset at the junction
            FirstVoltagePortStateFound = False
            StateVariableIndices = [] # Index of port state voltages at the junction
            PortsToRemove = []
            InputVariablesToSolveFor = [] # Port input voltages
            FirstVoltage = None

            for k in PortsAtJunction:
                logger.debug(f'Processing port {k} in junction {row}')
                if PortOutputTypes[k] == 'Voltage':
                    logger.debug(f'Port {k} is a voltage port')
                    if not FirstVoltagePortStateFound:
                        logger.debug(f"First voltage port state found at port {k}")
                        index = find(StateVariableDerivatives, PortStateDerivatives[k])
                        StateVariableIndices.append(index)
                        StateVariableDerivativeToSolveFor = PortStateDerivatives[k]
                        InputVariablesToSolveFor.append(PortInputs[k])
                        FirstVoltage = V[k]
                        FirstVoltagePortStateFound = True
                        # if there's a second "Voltage" port at the junction, then there
                        # is at least one all-capacitor loop at the junction
                    else:
                        logger.debug(f'Second voltage port found at port {k} (AllCapacitorLoop)')
                        AllCapacitorLoop = True
                        index = find(StateVariableDerivatives, PortStateDerivatives[k])
                        StateVariableIndices.append(index)
                        InputVariablesToSolveFor.append(PortInputs[k])
                        PortsToRemove.append(k)
                        SecondVoltage = V[k]
                        VoltageEquation = FirstVoltage - SecondVoltage # I think Rupa wanted to carry over FirstVoltage from previous row?
                        VoltageExpression = sp.solve(VoltageEquation, PortStates[k], dict=True)[0][PortStates[k]]
                        
                        VoltageExpression_Time = VoltageExpression.subs(PortStatesTimeSubstituteDict)
                        derivative = sp.diff(VoltageExpression_Time, sp.symbols('t', real=True))
                        VoltageDerivativeExpression = derivative.subs(PortStatesDerivativesSubstituteDict)
                        VoltageExpressionSubstituteDict = {PortStates[k]: VoltageExpression}
                        StateSpaceEquations = StateSpaceEquations.subs(VoltageExpressionSubstituteDict)
                        I = I.subs(VoltageExpressionSubstituteDict)
                        V = V.subs(VoltageExpressionSubstituteDict)
                        ControlInputEquations = ControlInputEquations.subs(VoltageExpressionSubstituteDict)
                        StateVariableDerivatives = StateVariableDerivatives.subs({PortStateDerivatives[k]: VoltageDerivativeExpression})


            if FirstVoltagePortStateFound: # only goes into this branch if there is a voltage port at the junction
                if not AllCapacitorLoop:
                    logger.debug(f'Junction {row} not an all-capacitor loop')
                    InputsAtJunction = [PortInputs[k] for k in PortsAtJunction] # Find the inputs at this junction
                    logger.debug(f"Inputs at junction {row}: {InputsAtJunction}")
                    VoltageEquations = None # Find the voltage port equations at this junction
                    FirstVoltage = V[PortsAtJunction[0]]
                    for i in range(1, len(PortsAtJunction)):
                        SecondVoltage = V[PortsAtJunction[i]]
                        if not VoltageEquations:
                            VoltageEquations = sp.Matrix([FirstVoltage - SecondVoltage])
                        else:
                            VoltageEquations = VoltageEquations.col_join(sp.Matrix([FirstVoltage - SecondVoltage]))
                    # Solve the KCL equation and the voltage equations at that junction for
					# the input variables
                    EquationsAtJunction = sp.Matrix.vstack(RowTemp*I, VoltageEquations)

                    # TODO: Double check if this is correct!
                    InputsSolution = sp.solve(EquationsAtJunction, InputsAtJunction) 
                    StateSpaceEquationsPythonListBeforeSubs.append(StateSpaceEquations)
                    InputsSolutionList.append(InputsSolution)

                    StateSpaceEquations = StateSpaceEquations.subs(InputsSolution)
                    StateSpaceEquationsPythonList.append(StateSpaceEquations)
                    V = V.subs(InputsSolution)
                    I = I.subs(InputsSolution)
                    # Also substitute in the port inputs in the controller equations
                    DesiredStateSpace = DesiredStateSpace.subs(InputsSolution)
                    ControlInputEquations = ControlInputEquations.subs(InputsSolution)
                    InternalEquations = InternalEquations.subs(InputsSolution)

                    # what is happening in this if block:
                        # If there is only one voltage port at the junction, 
                        # then we can solve for the voltage inputs at the junction in terms of the other voltages at the junction and the current inputs at the junction (KCL equation) and the state equations for the voltages (KVL equations). We can then substitute these solutions into the state space model. If there are more than one voltage port at the junction, then we must solve a system of equations (consisting of the KCL equation and the state equations for the Voltages) and unknowns (consisting of the current inputs and the Voltage derivative which is not replaced) to find the voltage inputs at the junction. We can then substitute these solutions into the state space model. We must also remove the other Voltage derivatives equations from the state space model as they are dependent and hence aren't states.  
 
                else:
                    logger.debug(f'Junction {row} is an all-capacitor loop')
                    Equations = RowTemp * I
                    StateEquations = StateVariableDerivatives.extract(StateVariableIndices, [-1]) - StateSpaceEquations.extract(StateVariableIndices, [-1])
                    Equations = Equations.col_join(StateEquations)
                    VariablesToSolveFor = [StateVariableDerivativeToSolveFor] + InputVariablesToSolveFor
                    Solution = sp.solve(Equations, VariablesToSolveFor)
                    if type(Solution) == list:
                        Solution = Solution[0]
                    
                    # Put the solution for the Voltage derivative in the state space model
                    NewStateSpaceEquation = getfield(Solution, StateVariableDerivativeToSolveFor)
                    MutableStateSpaceEquations = sp.Matrix(StateSpaceEquations)
                    MutableStateSpaceEquations[StateVariableIndices[0]] = NewStateSpaceEquation
                    StateSpaceEquations = MutableStateSpaceEquations

                    StateSpaceEquations = StateSpaceEquations.subs(Solution)
                    ControlInputEquations = ControlInputEquations.subs(Solution)
                    InternalEquations = InternalEquations.subs(Solution)

                    # Remove the other Voltage derivatives equations from the state space model.
                    # (They are dependent so hence aren't states)
                    StateVariables = sp.Matrix([row for i, row in enumerate(StateVariables.tolist()) if i not in StateVariableIndices[1:]])
                    StateSpaceEquations = sp.Matrix([row for i, row in enumerate(StateSpaceEquations.tolist()) if i not in StateVariableIndices[1:]])
                    StateVariableDerivatives = sp.Matrix([row for i, row in enumerate(StateVariableDerivatives.tolist()) if i not in StateVariableIndices[1:]])

                    # Find the voltage equations at this junction in order to solve for
					# the voltage inputs at the junction (don't find in terms of the
					# Voltages which have already been substituted for)
                    VoltageEquations = None
                    ValidPorts = setdiff(PortsAtJunction, PortsToRemove)
                    FirstVoltage = V[ValidPorts[0]]
                    for i in range(1, len(ValidPorts)):
                        SecondVoltage = V[PortsAtJunction[i]]
                        if not VoltageEquations:
                            VoltageEquations = sp.Matrix([FirstVoltage - SecondVoltage])
                        else:
                            VoltageEquations = VoltageEquations.col_join(sp.Matrix([FirstVoltage - SecondVoltage]))
                    V_InputsAtJunction = []
                    for port in ValidPorts:
                        if PortOutputTypes[port] == 'Current':
                            V_InputsAtJunction.append(PortInputs[port])
                    if V_InputsAtJunction:
                        V_InputsSolution = sp.solve(VoltageEquations, V_InputsAtJunction)
                        StateSpaceEquations = StateSpaceEquations.subs(V_InputsSolution)
                        DesiredStateSpace = DesiredStateSpace.subs(V_InputsSolution)
                        ControlInputEquations = ControlInputEquations.subs(V_InputsSolution)
                        InternalEquations = InternalEquations.subs(V_InputsSolution)
                        V = V.subs(V_InputsSolution)
                        I = I.subs(V_InputsSolution)

            else: # Goes into this branch if there is no voltage port at the junction
                logger.debug(f'No voltage port at junction {row} (all-inductor cutset)')
                StateVariableIndices, InputVariablesToSolveFor, PortsToRemove = [], [], [] # Initialize variables
                FirstVoltage_list = V[PortsAtJunction[0]] # Find the first voltage port at the junction
                FirstVoltage = sp.Matrix([FirstVoltage_list])
                VoltageEquations = sp.Matrix() # Find the voltage port equations at this junction
                PortRemovalFlag = False 
                StateVariableDerivativeToSolveFor = sp.Matrix([PortStateDerivatives[i] for i in PortsAtJunction[1:]]) # Find the state derivative to solve for
                for i, port in enumerate(PortsAtJunction): # Loop through the ports at the junction
                    try:
                        a = find(StateVariableDerivatives, PortStateDerivatives[port]) # Find the index of the port state current at the junction
                        StateVariableIndices.append(a) # Add the index to the list of indices
                    except:
                        PortsToRemove.append(port) # Why the port is being removed: The port is not a state variable
                        PortRemovalFlag = True
                    InputVariablesToSolveFor.append(PortInputs[port]) # Do we still solve for this input variable if the port is removed?
                    if i > 0:
                        SecondVoltage_list = V[port]
                        SecondVoltage = sp.Matrix([SecondVoltage_list])
                        VoltageEquations = VoltageEquations.col_join(sp.Matrix([FirstVoltage - SecondVoltage]))
                
                CurrentEquation = RowTemp * I
                
                if not PortRemovalFlag:
                    logger.debug('No ports to remove')
                    PortsToRemove = PortsAtJunction[0] # Why do I remove the first port at the junction? 
                    CurrentExpression = sp.solve(CurrentEquation, PortStates[PortsToRemove])
                    PortStateExpression = CurrentExpression[PortStates[PortsToRemove]]
                    
                    # Substitute PortStates(t) for PortStates before differentiating
                    Temp = PortStateExpression.subs(PortStatesTimeSubstituteDict)
                    CurrentDerivativeExpression = sp.diff(Temp, sp.symbols('t', real=True))
                    CurrentDerivativeExpression = CurrentDerivativeExpression.subs(PortStatesDerivativesSubstituteDict)

                    logger.debug('All-inductor cutset: Replaced ', PortStates[PortsAtJunction[0]], ' with ', PortStateExpression, \
                            ' and ', PortStateDerivatives[PortsAtJunction[0]],' with ', CurrentDerivativeExpression)
                    PortStateSubstituteDict = {PortStates[PortsAtJunction[0]]: PortStateExpression}
                    StateSpaceEquations = StateSpaceEquations.subs(PortStateSubstituteDict)
                    DesiredStateSpace = DesiredStateSpace.subs(PortStateSubstituteDict)
                    ControlInputEquations = ControlInputEquations.subs(PortStateSubstituteDict)
                    SetPointOutputEquations = SetPointOutputEquations.subs(PortStateSubstituteDict)
                    InternalEquations = InternalEquations.subs(PortStateSubstituteDict)
                    # I = I.subs(PortStateSubstituteDict)

                    StateVariableDerivatives1 = StateVariableDerivatives.subs({PortStateDerivatives[PortsAtJunction[0]]: CurrentDerivativeExpression})
                    Equations = StateVariableDerivatives1.extract(StateVariableIndices, [-1]) - StateSpaceEquations.extract(StateVariableIndices, [-1])
                    Equations = sp.simplify(Equations.col_join(VoltageEquations))
                    VariablesToSolveFor = list(StateVariableDerivativeToSolveFor)
                    VariablesToSolveFor.extend(InputVariablesToSolveFor)
                    Solution = sp.solve(Equations, VariablesToSolveFor)
                else:
                    logger.debug('Removing ports', PortsToRemove)
                    indices = setdiff(PortsAtJunction, PortsToRemove) # indices of ports to keep
                    StateVariableDerivativeToSolveFor = sp.Matrix([PortStateDerivatives[i] for i in indices])
                    Equations = CurrentEquation.col_join(VoltageEquations)
                    VariablesToSolveFor = sp.Matrix([InputVariablesToSolveFor])
                    if len(StateVariableIndices) > 0:
                        StateVariableDerivatives_selected = sp.Matrix([StateVariableDerivatives[i] for i in StateVariableIndices])
                        StateSpaceEquations_selected = sp.Matrix([StateSpaceEquations[i] for i in StateVariableIndices])
                        # EquationsAtJunction = sp.Matrix.vstack(RowTemp*I, VoltageEquations)
                        Equations = sp.Matrix.vstack(Equations, StateVariableDerivatives_selected - StateSpaceEquations_selected)
                        VariablesToSolveFor = VariablesToSolveFor.row_join(StateVariableDerivativeToSolveFor)
                    VariablesToSolveForCell = VariablesToSolveFor.tolist()[0]

                    Solution = sp.solve(Equations, VariablesToSolveForCell)
                    if type(Solution) == list:
                        Solution = Solution[0]
                
                logger.debug("Solving for input variables")
                for variable in InputVariablesToSolveFor: # Why are we not also substituting StateVariablesToSolveFor?
                    InputSol = {variable: Solution[variable]}
                    StateSpaceEquations = StateSpaceEquations.subs(InputSol)
                    I = I.subs(InputSol)
                    DesiredStateSpace = DesiredStateSpace.subs(InputSol)
                    ControlInputEquations = ControlInputEquations.subs(InputSol)
                    SetPointOutputEquations = SetPointOutputEquations.subs(InputSol)
                    InternalEquations = InternalEquations.subs(InputSol)

                # Put the solution for the Voltage derivative in the state space model
                MutableStateSpaceEquations = sp.Matrix(StateSpaceEquations)
                for derivative in StateVariableDerivativeToSolveFor:
                    NewStateSpaceEquation = getfield(Solution, derivative)
                    idx = find(StateVariableDerivatives, derivative)
                    MutableStateSpaceEquations[idx] = NewStateSpaceEquation
                StateSpaceEquations = MutableStateSpaceEquations
            
                if not PortRemovalFlag and len(StateVariableIndices) > 0:
                    if StateVariableIndices[0] not in ToRemoveIndices:
                        ToRemoveIndices.append(StateVariableIndices[0])
                    FirstStateVariable = StateVariables[StateVariableIndices[0]]
                    if FirstStateVariable is not None:
                        FinCurrEqns = FirstStateVariable - PortStateExpression
                        Sol = sp.solve(FinCurrEqns, FirstStateVariable, dict=True)
                        if type(Sol) == list:
                            Sol = Sol[0]
                        StateSpaceEquations = StateSpaceEquations.subs(Sol)
                        ControlInputEquations = ControlInputEquations.subs(Sol)

            # Remove the other Voltage derivatives equations from the state space model.
            # (They are dependent so hence aren't states)

            # Out of the original if/else block based on whether Voltage port is found
            if ToRemoveIndices:
                logger.debug('Removing indices ', ToRemoveIndices)
                StateVariables = sp.Matrix([row for i, row in enumerate(StateVariables.tolist()) if i not in ToRemoveIndices])
                StateSpaceEquations = sp.Matrix([row for i, row in enumerate(StateSpaceEquations.tolist()) if i not in ToRemoveIndices])
                StateVariableDerivatives = sp.Matrix([row for i, row in enumerate(StateVariableDerivatives.tolist()) if i not in ToRemoveIndices])		
            
            if InternalInputs and not isempty(InternalInputs):
                logger.debug(f'Solving for InternalInputs at junction {row}')
                EquationsIntern = InternalInputs - InternalEquations
                SolIntern = sp.solve(EquationsIntern, InternalInputs)
                InternalEquations = InternalEquations.subs(SolIntern)
            
            if ControllableInputs and not isempty(ControllableInputs):
                logger.debug(f'Solving for ControllableInputs at junction {row}')
                EquationsControl = ControllableInputs - ControlInputEquations
                SolControl = sp.solve(EquationsControl, ControllableInputs)
                ControlInputEquations = ControlInputEquations.subs(SolControl)

            if SetPointOutputs and not isempty(SetPointOutputs):
                logger.debug(f'Solving for SetPointOutputs at junction {row}')
                EquationsSetPoints = SetPointOutputs - SetPointOutputEquations
                SolSetPoints = sp.solve(EquationsSetPoints, SetPointOutputs)
                SetPointOutputEquations = SetPointOutputEquations.subs(SolSetPoints)
                    
            ReturnUnits = []
            for variable in StateVariables:
                idxUnit = find(OriginalStateVariables, variable)
                ReturnUnits.append(Units[idxUnit] if idxUnit < len(Units) else None)
            Units = ReturnUnits

        self.StateVariableDerivatives = StateVariableDerivatives
        self.StateSpaceEquations = StateSpaceEquations
        self.DesiredStateVariableDerivatives = DesiredStateVariableDerivatives
        self.DesiredStateSpace = DesiredStateSpace
        self.ControllableInputs = ControllableInputs
        self.InternalInputs = InternalInputs
        self.ControlInputEquations = ControlInputEquations
        self.SetPointOutputs = SetPointOutputs
        self.SetPointOutputEquations = SetPointOutputEquations
        self.StateVariables = StateVariables
        self.DesiredStateVariables = DesiredStateVariables
        self.InternalEquations = InternalEquations
        self.Parameters = Parameters
        self.SetPoints = SetPoints
        self.ControllerGains = ControllerGains
        self.Units = Units
        self.StateSpaceObject = StateSpace(self.system_name, self.SetPointOutputs, self.SetPointOutputEquations, self.ControllableInputs, self.ControlInputEquations, self.InternalInputs, self.InternalEquations, self.StateVariableDerivatives, self.StateSpaceEquations, self.DesiredStateVariableDerivatives, self.DesiredStateSpace, self.StateVariables, self.DesiredStateVariables)

