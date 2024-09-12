from sympy import symbols, Function, simplify, Matrix, sin, cos, pprint
from pycamps.modules.module import Module

class RCShunt(Module):
    '''RC Shunt module'''
    def __init__(self, IndexName, RefFrameAngle=None, RefFrameSpeed=None, BaseSpeed=1, ParamMap=None):
        super().__init__()
        self.ModuleName = IndexName
        ParameterNames = ['Rsh','Csh']
        StateVariableNames = ['vcd','vcq']
        PortInputNames = ['iInd', 'iInq']
        PortStateNames = ['vcd','vcq']

        Units = ['V','V'] if BaseSpeed == 1 else ['units']*2

        self.RefFrameAngle = RefFrameAngle if RefFrameAngle is not None else symbols('phi', real=True)
        self.RefFrameSpeed = RefFrameSpeed if RefFrameSpeed is not None else symbols('dphidt', real=True)
        self.BaseSpeed = BaseSpeed
        IndexName = '_' + IndexName # TODO: Properly implement index names without leading underscore

        self.ParameterMap = ParamMap if ParamMap is not None and all(
            key in [p + IndexName for p in ParameterNames] for key in ParamMap.keys()) else {}
        
        self.Units = Units

        self.Parameters = Matrix(symbols([p + IndexName for p in ParameterNames]))
        self.StateVariables =  Matrix(symbols([s + IndexName for s in StateVariableNames]))
        self.PortInputs =  Matrix(symbols([p + IndexName for p in PortInputNames]))
        self.PortStates =  Matrix(symbols([p + IndexName for p in PortStateNames]))

        self.PortCurrents = self.PortInputs
        self.PortVoltages = self.PortStates

        self.StateVariableDerivatives =  Matrix(symbols(['d' + s + IndexName + 'dt' for s in StateVariableNames]))
        self.PortStateDerivatives =  Matrix(symbols(['d' + p + IndexName + 'dt' for p in PortStateNames]))
        self.PortStates_Time = Matrix([Function(p + IndexName + '_t')(symbols('t', real=True)) for p in PortStateNames])
        self.PortOutputTypes = ['Voltage']*2
        self.StateSpaceEquations = self.dynamics()

    def dynamics(self):
        '''
        Inputs:
        this.StateVariables: vcd; vcq
        this.InputVariables: iInd, iInq
        this.Parameters: RSh, Csh
            
        Outputs:
        StateSpace = [dvcddt, dvcqdt]
        '''
        vcd, vcq = self.StateVariables
        iInd, iInq = self.PortInputs
        Rsh, Csh = self.Parameters
        
        wb = self.BaseSpeed
        dphidt = self.RefFrameSpeed
        
        # Transmission Line Dynamics
        dvcddt = ( - vcd/(Rsh*Csh) + iInd/Csh + dphidt*vcq);         
        dvcqdt = (- vcq/(Rsh*Csh) + iInq/Csh - dphidt*vcd)
        
        StateSpace = Matrix([dvcddt, dvcqdt])
        StateSpace = simplify(StateSpace)
        return StateSpace