from sympy import symbols, Function, simplify, Matrix
from pycamps.modules.module import Module

class RLLoad(Module):
    '''
    Constant impedance load
    '''
    def __init__(self, IndexName, RefFrameAngle=None, RefFrameSpeed=None, BaseSpeed=1, ParamMap=None):
        super().__init__()
        self.ModuleName = IndexName
        ParameterNames = ['RL', 'LL']
        StateVariableNames = ['iLd', 'iLq']
        PortInputNames = ['vLd', 'vLq']
        PortStateNames = ['iLd', 'iLq']
        ControllableInputNames = []

        Units = ['A', 'A'] if BaseSpeed == 1 else ['units', 'units']

        IndexName = '_' + IndexName # TODO: Properly implement index names without leading underscore
        self.ParameterMap = ParamMap if ParamMap is not None and all(
            key in [p + IndexName for p in ParameterNames] for key in ParamMap.keys()) else {}

        self.RefFrameAngle = RefFrameAngle if RefFrameAngle is not None else symbols('phi', real=True)
        self.RefFrameSpeed = RefFrameSpeed if RefFrameSpeed is not None else symbols('dphidt', real=True)
        self.BaseSpeed = BaseSpeed
        self.Units = Units

        self.Parameters = Matrix(symbols([p + IndexName for p in ParameterNames]))
        self.StateVariables = Matrix(symbols([s + IndexName for s in StateVariableNames]))
        self.ControllableInputs = Matrix(symbols([c + IndexName for c in ControllableInputNames]))
        self.PortInputs = Matrix(symbols([p + IndexName for p in PortInputNames]))
        self.PortStates = Matrix(symbols([p + IndexName for p in PortStateNames]))

        self.PortVoltages = self.PortInputs
        self.PortCurrents = self.PortStates

        self.StateVariableDerivatives = Matrix(symbols(['d' + s + IndexName + 'dt' for s in StateVariableNames]))
        self.PortStateDerivatives = Matrix(symbols(['d' + p + IndexName + 'dt' for p in PortStateNames]))
        self.PortStates_Time = Matrix([Function(p + IndexName + '_t')(symbols('t', real=True)) for p in PortStateNames])
        self.PortOutputTypes = ['Current', 'Current']
        self.StateSpaceEquations = self.dynamics()

    def dynamics(self):
        '''
        Inputs:
        this.StateVariables: iLd,iLq
        this.InputVariables: vLd, vLq
        this.Parameters: RL, LL
        
        Outputs:
        StateSpace = [ diLddt ; diLqdt]
        '''
        iLd, iLq = self.StateVariables
        vLd, vLq = self.PortInputs
        RL, LL = self.Parameters

        dphidt = self.RefFrameSpeed
        wb = self.BaseSpeed

        # RLLoad dynamics equations
        diLddt = dphidt * iLq + (vLd - RL * iLd) / LL
        diLqdt = -dphidt * iLd + (vLq - RL * iLq) / LL

        StateSpace = wb * simplify(Matrix([diLddt, diLqdt]))
        return StateSpace
