from sympy import symbols, simplify, Matrix, sin, cos, Function
from pycamps.modules.module import Module

class InfBus(Module):
    '''Contant voltage souce with series impedance'''
    def __init__(self, IndexName, RefFrameAngle, RefFrameSpeed, BaseSpeed, ParamMap=None):
        super().__init__()
        ParameterNames = ['Rinf', 'Linf', 'vInfd', 'vInfq']
        StateVariableNames = ['Id', 'Iq']
        PortInputNames = ['Vd', 'Vq']
        PortStateNames = ['Id', 'Iq']
        ControllableInputNames = []

        Units = ['A', 'A'] if BaseSpeed == 1 else ['units', 'units']

        self.ParameterMap = ParamMap if ParamMap is not None and all(
            key in [p + IndexName for p in ParameterNames] for key in ParamMap.keys()) else {}

        self.RefFrameAngle = RefFrameAngle
        self.RefFrameSpeed = RefFrameSpeed
        self.BaseSpeed = BaseSpeed
        self.Units = Units
        self.Parameters = Matrix(symbols([p + IndexName for p in ParameterNames]))
        self.StateVariables = Matrix(symbols([s + IndexName for s in StateVariableNames]))
        self.ControllableInputs = Matrix(symbols([ci + IndexName for ci in ControllableInputNames]))
        self.PortInputs = Matrix(symbols([p + IndexName for p in PortInputNames]))
        self.PortStates = Matrix(symbols([p + IndexName for p in PortStateNames]))
        self.PortVoltages = self.PortInputs
        self.PortCurrents = -self.PortStates
        self.StateVariableDerivatives = Matrix(symbols(['d' + s + IndexName + 'dt' for s in StateVariableNames]))
        self.PortStateDerivatives = Matrix(symbols(['d' + p + IndexName + 'dt' for p in PortStateNames]))
        self.PortStates_Time = Matrix([Function(p + IndexName + '_t')(symbols('t', real=True)) for p in PortStateNames])
        self.PortOutputTypes = ['Current', 'Current']
        self.StateSpaceEquations = InfBus.dynamics(self)

    def dynamics(self):
        '''
        Inputs:
        this.StateVariables: Id,Iq
        this.PortInputs: Vd,Vq
        this.Parameters: Rinf,Linf,vInfd,vInfq
        this.RefFrameAngle: angle of rotating reference frame
        this.RefFrameSpeed: speed of rotating reference frame
        this.BaseSpeed: Base speed

        Outputs:
        StateSpace: [dIddt ; dIqdt]
        '''

        Id, Iq = self.StateVariables
        Vd, Vq = self.PortInputs
        Rinf, Linf, vInfd, vInfq = self.Parameters

        wb = self.BaseSpeed
        dphidt = self.RefFrameSpeed
        
        # InfBus Dynamics
        dIddt = dphidt * Iq + (vInfd - Vd - Rinf * Id) / Linf
        dIqdt = (vInfq - Vq - Rinf * Iq) / Linf - dphidt * Id

        StateSpace = wb * Matrix([dIddt, dIqdt])
        return StateSpace
    