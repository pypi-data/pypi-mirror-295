from sympy import symbols, Function, simplify, Matrix
from pycamps.modules.module import Module

class PQLoad(Module):
    def __init__(self, IndexName, RefFrameAngle, RefFrameSpeed, BaseSpeed, ParamMap=None):
        super().__init__()
        ParameterNames = ['PL','QL']
        StateVariableNames = ['iLd','iLq']
        PortInputNames = ['vLd','vLq']
        PortStateNames = ['iLd','iLq']
        ControllableInputNames = ['LL']

        if BaseSpeed == 1:
            Units = ['V', 'V', 'A', 'A', 'V', 'V']
        else:
            Units = ['units']*6

        self.ParameterMap = ParamMap if ParamMap is not None and all(
            key in [p + IndexName for p in ParameterNames] for key in ParamMap.keys()) else {}

        self.RefFrameAngle = RefFrameAngle
        self.RefFrameSpeed = RefFrameSpeed
        self.BaseSpeed = BaseSpeed
        self.Units = Units
        
        self.Parameters = symbols([p + IndexName for p in ParameterNames])
        self.StateVariables = symbols([s + IndexName for s in StateVariableNames])
        self.ControllableInputs = symbols([c + IndexName for c in ControllableInputNames])
        self.PortInputs = symbols([p + IndexName for p in PortInputNames])
        self.PortStates = symbols([p + IndexName for p in PortStateNames])
        
        self.PortCurrents = self.PortInputs
        self.PortVoltages = self.PortStates
        self.StateVariableDerivatives = symbols(['d' + s + IndexName + 'dt' for s in StateVariableNames])
        self.PortStateDerivatives = symbols(['d' + p + IndexName + 'dt' for p in PortStateNames])
        
        self.PortStates_Time = Matrix([Function(p + IndexName + '_t')(symbols('t', real=True)) for p in PortStateNames])
        
        self.PortOutputTypes = ['Current','Current']
        self.StateSpaceEquations, self.InternalEquations = self.dynamics()

    def dynamics(self):
        '''
        Inputs:
        this.StateVariables: iLd,iLq
        this.InputVariables: vLd, vLq
        this.Parameters: PL, QL
        
        Outputs:
        StateSpace = [ diLddt ; diLqdt];
        NOTE: TO BE USED ONLY IN THE ABSENCE OF INDUCTOR CUTSETS
        '''
        iLd, iLq = self.StateVariables
        vLd, vLq = self.PortInputs
        PL, QL = self.Parameters
        # LL = (QL*(vLd**2 + vLq**2))/(PL**2 + QL**2)
        LL = self.ControllableInputs[0]

        wb = self.BaseSpeed
        dphidt = self.RefFrameSpeed

        # PQLoad Dynamics
        diLddt = (-PL/QL * iLd) + vLd/LL + dphidt*iLq
        diLqdt = (-PL/QL * iLq) + vLq/LL - dphidt*iLd
            
        LL = (QL*(vLd**2 + vLq**2))/(PL**2 + QL**2)

        StateSpace = wb * Matrix([diLddt, diLqdt])
        StateSpace = simplify(StateSpace)
        InternalEquations = Matrix([LL])
        return StateSpace, InternalEquations