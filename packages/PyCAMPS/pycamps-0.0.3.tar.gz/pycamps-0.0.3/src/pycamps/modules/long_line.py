from sympy import symbols, Function, simplify, Matrix
from pycamps.modules.module import Module

class LongLine(Module):
    def __init__(self, IndexName, RefFrameAngle, RefFrameSpeed, BaseSpeed, ParamMap=None):
        super().__init__()
        ParameterNames = ['RTL', 'CTL', 'LTL']
        StateVariableNames = ['vTLLd', 'vTLLq', 'iTLMd', 'iTLMq', 'vTLRd', 'vTLRq']
        PortInputNames = ['iInLd', 'iInLq', 'iInRd', 'iInRq']
        PortStateNames = ['vTLLd', 'vTLLq', 'vTLRd', 'vTLRq']
        ControllableInputNames = []

        Units = ['A', 'A'] if BaseSpeed == 1 else ['units', 'units']

        self.ParameterMap = ParamMap if ParamMap is not None and all(
            key in [p + IndexName for p in ParameterNames] for key in ParamMap.keys()) else {}

        self.RefFrameAngle = RefFrameAngle
        self.RefFrameSpeed = RefFrameSpeed
        self.BaseSpeed = BaseSpeed
        self.Units = Units
        
        self.Parameters = Matrix(symbols([p + IndexName for p in ParameterNames]))
        self.StateVariables =  Matrix(symbols([s + IndexName for s in StateVariableNames]))
        self.ControllableInputs =  Matrix(symbols([c + IndexName for c in ControllableInputNames]))
        self.PortInputs =  Matrix(symbols([p + IndexName for p in PortInputNames]))
        self.PortStates =  Matrix(symbols([p + IndexName for p in PortStateNames]))
        
        self.PortCurrents = self.PortInputs
        self.PortVoltages = self.PortStates
        self.StateVariableDerivatives =  Matrix(symbols(['d' + s + IndexName + 'dt' for s in StateVariableNames]))
        self.PortStateDerivatives =  Matrix(symbols(['d' + p + IndexName + 'dt' for p in PortStateNames]))
        self.PortStates_Time = Matrix([Function(p + IndexName + '_t')(symbols('t', real=True)) for p in PortStateNames])
        self.PortOutputTypes = ['Voltage', 'Voltage', 'Voltage', 'Voltage']
        self.StateSpaceEquations = self.dynamics()

    def dynamics(self):
        vTLLd, vTLLq, iTLMd, iTLMq, vTLRd, vTLRq = self.StateVariables
        iInLd, iInLq, iInRd, iInRq = self.PortInputs
        RTL, CTL, LTL = self.Parameters

        wb = self.BaseSpeed
        dphidt = self.RefFrameSpeed

        # Transmission Line Dynamics
        dvTLLddt = (iInLd - iTLMd) / CTL + dphidt * vTLLq
        dvTLLqdt = (iInLq - iTLMq) / CTL - dphidt * vTLLd
        diTLMddt = dphidt * iTLMq - (vTLRd - vTLLd + RTL * iTLMd) / LTL
        diTLMqdt = -dphidt * iTLMd - (vTLRq - vTLLq + RTL * iTLMq) / LTL
        dvTLRddt = (iInRd + iTLMd) / CTL + dphidt * vTLRq
        dvTLRqdt = (iInRq + iTLMq) / CTL - dphidt * vTLRd

        # StateSpace = wb * simplify([dvTLLddt, dvTLLqdt, diTLMddt, diTLMqdt, dvTLRddt, dvTLRqdt])
        StateSpace = [dvTLLddt, dvTLLqdt, diTLMddt, diTLMqdt, dvTLRddt, dvTLRqdt]
        StateSpace = Matrix([wb * expr for expr in StateSpace])
        StateSpace = simplify(StateSpace)
        return StateSpace
