from sympy import symbols, Function, simplify, Matrix
from pycamps.modules.module import Module

class PVSOAControl(Module):
    def __init__(self, IndexName, RefFrameAngle, RefFrameSpeed, BaseSpeed, ParamMap=None):
        '''
        Implements a solar PV model with SOA control.
        '''
        super().__init__()
        ParameterNames = ['Rf', 'Lf', 'Vs']
        StateVariableNames = ['iPVd', 'iPVq']
        PortInputNames = ['vPVd', 'vPVq']
        PortStateNames = ['iPVd', 'iPVq']
        ControllableInputNames = ['Sd', 'Sq']
        SetPointNames = ['P', 'Q']

        Units = ['A', 'A'] if BaseSpeed == 1 else ['units', 'units']

        self.ParameterMap = ParamMap if ParamMap is not None and all(
            key in [p + IndexName for p in ParameterNames] for key in ParamMap.keys()) else {}
        
        self.RefFrameAngle = RefFrameAngle
        self.RefFrameSpeed = RefFrameSpeed
        self.BaseSpeed = BaseSpeed
        self.Units = Units

        self.Parameters = Matrix(symbols([p + IndexName for p in ParameterNames]))
        self.StateVariables = Matrix(symbols([s + IndexName for s in StateVariableNames]))
        self.ControllableInputs = Matrix(symbols([c + IndexName for c in ControllableInputNames]))
        self.PortInputs = Matrix(symbols([p + IndexName for p in PortInputNames]))
        self.PortStates = Matrix(symbols([p + IndexName for p in PortStateNames]))

        self.PortVoltages = self.PortInputs
        self.PortCurrents = -self.PortStates
        self.StateVariableDerivatives = Matrix(symbols(['d' + s + IndexName + 'dt' for s in StateVariableNames]))
        self.PortStateDerivatives = Matrix(symbols(['d' + p + IndexName + 'dt' for p in PortStateNames]))
        self.PortStates_Time = Matrix([Function(p + IndexName + '_t')(symbols('t', real=True)) for p in PortStateNames])
        self.PortOutputTypes = ['Current', 'Current']
        self.SetPoints = Matrix(symbols([s + IndexName + '_ref' for s in SetPointNames]))
        self.StateSpaceEquations, self.ControlInputEquations = self.dynamics()

    def dynamics(self):
        iPVd, iPVq = self.StateVariables
        vPVd, vPVq = self.PortInputs
        Rf, Lf, Vs = self.Parameters
        Pref, Qref = self.SetPoints
        Sd, Sq = self.ControllableInputs
        dphidt = self.RefFrameSpeed
        wb = self.BaseSpeed
        
        # Control Design
        # I = (Pref + 1i*Qref)/(vPVd + 1i*vPVq);
        # iPVdref = real(I); iPVqref = imag(I);
        iPVdref = (Pref*vPVd + Qref*vPVq)/(vPVd**2 + vPVq**2) # Assuming Pref, Qref, vPVd, vPVq are real quantities
        iPVqref = (Qref*vPVd - Pref*vPVq)/(vPVd**2 + vPVq**2)
        Sd_eq = 1/Vs*(vPVd - Lf*dphidt*iPVq + Rf*iPVd - Lf*(iPVd-iPVdref))
        Sq_eq = 1/Vs*(vPVq + Lf*dphidt*iPVd + Rf*iPVq - Lf*(iPVq-iPVqref))
        
        # Load Dynamics
        diPVddt = - Rf*iPVd/Lf + dphidt*iPVq + (Vs*Sd - vPVd)/Lf
        diPVqdt = - Rf*iPVq/Lf - dphidt*iPVd + (Vs*Sq - vPVq)/Lf
        
        StateSpaceEquations = wb*Matrix([diPVddt, diPVqdt])
        ControlInputEquations = Matrix([Sd_eq, Sq_eq])
        StateSpaceEquations = simplify(StateSpaceEquations)
        ControlInputEquations = simplify(ControlInputEquations)
        return StateSpaceEquations, ControlInputEquations

class SolarPV_v2_SOAControl(Module):
    def __init__(self, IndexName, RefFrameAngle, RefFrameSpeed, BaseSpeed, Mode, ParamMap=None):
        '''
        Another implementation of a solar PV model with SOA control.
        '''
        super().__init__()
        ParameterNames = ['Rf', 'Lf', 'Vs', 'KV']
        StateVariableNames = ['iPVd', 'iPVq']
        PortStateNames = ['iPVd', 'iPVq']
        PortInputNames = ['vPVd', 'vPVq']
        ControllableInputNames = ['Sd', 'Sq']
        if Mode == 'PQ':
            SetPointNames = ['P', 'Q']
        else:
            SetPointNames = ['Vt']
        
        if BaseSpeed == 1:
            Units = ['A', 'A', 'V', 'V']
        else:
            Units = ['units']*4
        
        # If optional parameter ParamMap is given, set this.ParameterMap
        # equal to ParamMap. Otherwise, set it to an empty array.
        if ParamMap is None:
            self.ParameterMap = []
        else:
            if not all([key in ParameterNames + [IndexName] for key in ParamMap.keys()]):
                raise ValueError('One or more keys in the Parameter Map do not match the parameter names')
            else:
                self.ParameterMap = ParamMap
        
        self.RefFrameAngle = RefFrameAngle
        self.RefFrameSpeed = RefFrameSpeed
        self.BaseSpeed = BaseSpeed
        self.Units = Units
        
        self.Parameters = symbols([name + IndexName for name in ParameterNames])
        self.StateVariables = symbols([name + IndexName for name in StateVariableNames])
        self.ControllableInputs = symbols([name + IndexName for name in ControllableInputNames])
        self.PortInputs = symbols([name + IndexName for name in PortInputNames])
        self.PortStates = symbols([name + IndexName for name in PortStateNames])
        self.PortVoltages = self.PortInputs
        self.PortCurrents = [-state for state in self.PortStates]
        self.StateVariableDerivatives = symbols(['d' + name + IndexName + 'dt' for name in StateVariableNames])
        self.PortStateDerivatives = symbols(['d' + name + IndexName + 'dt' for name in PortStateNames])
        self.PortStates_Time = Matrix([Function(p + IndexName + '_t')(symbols('t', real=True)) for p in PortStateNames])
        self.PortOutputTypes = ['Current', 'Current']
        self.SetPoints = symbols([name + IndexName + '_ref' for name in SetPointNames])
        self.StateSpace, self.ControlInputEquations = self.dynamics(Mode)

    def dynamics(self, Mode):
        iPVd = self.StateVariables[0]
        iPVq = self.StateVariables[1]
        
        vPVd = self.PortInputs[0]
        vPVq = self.PortInputs[1]
        
        Rf = self.Parameters[0]
        Lf = self.Parameters[1]
        Vs = self.Parameters[2]
        Kv = self.Parameters[3]
        
        if Mode == 'PQ':
            Pref = self.SetPoints[0]
            Qref = self.SetPoints[1]
        else:
            Vref = self.SetPoints[0]
        
        Sd = self.ControllableInputs[0]
        Sq = self.ControllableInputs[1]
        
        dphidt = self.RefFrameSpeed
        wb = self.BaseSpeed
        
        if Mode == 'PQ':
            Vmag2 = vPVd**2 + vPVq**2
            iPVdref = (Pref*vPVd + Qref*vPVq)/Vmag2
            iPVqref = (-Qref*vPVd + Pref*vPVq)/Vmag2
        else:
            vPVdref = Vref
            vPVqref = 0
            iPVdref = - Kv*(vPVd - vPVdref)
            iPVqref = - Kv*(vPVq - vPVqref)
        
        # Open loop equations
        diPVddt = -(Rf/Lf)*iPVd + (Vs*Sd - vPVd)/Lf + dphidt*iPVq
        diPVqdt = -(Rf/Lf)*iPVq + (Vs*Sq - vPVq)/Lf - dphidt*iPVd
        
        Sd = (vPVd - dphidt*Lf*iPVq + Rf*iPVdref)/Vs
        Sq = (vPVq + dphidt*Lf*iPVd + Rf*iPVqref)/Vs
        
        StateSpace = wb*[diPVddt, diPVqdt]
        ControlInputEquations = [Sd, Sq]
        StateSpace = simplify(StateSpace)
        ControlInputEquations = simplify(ControlInputEquations)
        
        return StateSpace, ControlInputEquations