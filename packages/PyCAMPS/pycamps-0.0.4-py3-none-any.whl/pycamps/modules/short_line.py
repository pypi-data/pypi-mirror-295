from sympy import symbols, Function, simplify, Matrix
from pycamps.modules.module import Module

class ShortLine(Module):
    def __init__(self, IndexName, RefFrameAngle=None, RefFrameSpeed=None, BaseSpeed=1, ParamMap=None):
        super().__init__()
        self.ModuleName = IndexName
        ParameterNames = ['RTL', 'LTL']
        StateVariableNames = ['iTLMd', 'iTLMq']
        PortInputNames = ['vTLLd', 'vTLLq', 'vTLRd', 'vTLRq']
        PortStateNames = ['iTLMd', 'iTLMq', 'iTLMd', 'iTLMq']
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
        self.StateVariables =  Matrix(symbols([s + IndexName for s in StateVariableNames]))
        self.ControllableInputs =  Matrix(symbols([c + IndexName for c in ControllableInputNames]))
        self.PortInputs =  Matrix(symbols([p + IndexName for p in PortInputNames]))
        self.PortStates =  Matrix(symbols([p + IndexName for p in PortStateNames]))

        self.PortCurrents = Matrix([self.PortStates[0], self.PortStates[1], -self.PortStates[2], -self.PortStates[3]])
        self.PortVoltages = self.PortInputs
        self.StateVariableDerivatives =  Matrix(symbols(['d' + s + IndexName + 'dt' for s in StateVariableNames]))
        self.PortStateDerivatives =  Matrix(symbols(['d' + p + IndexName + 'dt' for p in PortStateNames]))
        self.PortStates_Time = Matrix([Function(p + IndexName + '_t')(symbols('t', real=True)) for p in PortStateNames])
        self.PortOutputTypes = ['Current', 'Current', 'Current', 'Current']
        self.StateSpaceEquations = self.dynamics()

    def dynamics(self):
        iTLMd, iTLMq = self.StateVariables
        vTLLd, vTLLq, vTLRd, vTLRq = self.PortInputs
        RTL, LTL = self.Parameters

        wb = self.BaseSpeed
        dphidt = self.RefFrameSpeed

        # Transmission Line Dynamics
        diTLMddt = dphidt * iTLMq - (vTLRd - vTLLd + RTL * iTLMd) / LTL
        diTLMqdt = -dphidt * iTLMd - (vTLRq - vTLLq + RTL * iTLMq) / LTL

        StateSpace = wb * Matrix([diTLMddt, diTLMqdt])
        StateSpace = simplify(StateSpace) # what does simplyfy() do?
        return StateSpace