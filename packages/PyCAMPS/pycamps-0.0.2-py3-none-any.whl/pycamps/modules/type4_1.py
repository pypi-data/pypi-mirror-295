from sympy import symbols, simplify, Matrix, sin, cos, Function
from pycamps.modules.module import Module

'''
This module contains the Type 4-1 model of a synchronous machine and its extension with Governor Control.
'''

class Type4_1(Module):
    '''Standard Type 4-1 model of a synchronous machine'''
    def __init__(self, IndexName, RefFrameAngle, RefFrameSpeed, BaseSpeed, ParamMap=None):
        super().__init__()
        ParameterNames = ['J', 'D', 'xdprime', 'RS', 'eqprime', 'Pm']
        StateVariableNames = ['delta', 'omega']
        PortInputNames = ['vSd', 'vSq']
        PortStateNames = ['iSd', 'iSq'] # These are not necessarily states. They are outputs instead
        SetPointNames = []

        Units = ['radians', 'rad/s'] if BaseSpeed == 1 else ['units', 'units']

        self.ParameterMap = ParamMap if ParamMap is not None and all(
            key in [p + IndexName for p in ParameterNames] for key in ParamMap.keys()) else {}

        self.RefFrameAngle = RefFrameAngle
        self.RefFrameSpeed = RefFrameSpeed
        self.BaseSpeed = BaseSpeed
        self.Units = Units
        self.Parameters = Matrix(symbols([p + IndexName for p in ParameterNames], real=True))
        self.StateVariables = Matrix(symbols([s + IndexName for s in StateVariableNames], real=True))
        self.SetPoints = Matrix(symbols([sp + IndexName + '_ref' for sp in SetPointNames], real=True))
        self.PortInputs = Matrix(symbols([p + IndexName for p in PortInputNames], real=True))
        self.PortStates = Matrix(symbols([p + IndexName for p in PortStateNames], real=True))

        self.PortVoltages = self.PortInputs
        
        delta = self.StateVariables[0]
        TN2M = Matrix([[sin(delta), -cos(delta)], [cos(delta), sin(delta)]])
        Vmach = TN2M * Matrix([[self.PortInputs[0]], [self.PortInputs[1]]])
        xdprime, RS, eqprime = self.Parameters[2], self.Parameters[3], self.Parameters[4]
        Imach = Matrix([[-xdprime, -RS], [-RS, xdprime]]).inv() * Matrix([[Vmach[1] - eqprime], [Vmach[0]]])
        self.PortCurrents = -simplify((TN2M.inv() * Imach)) # I'm skipping the transpose here

        self.PortOutputTypes = ['Current', 'Current']
        self.StateVariableDerivatives = Matrix(symbols(['d' + s + IndexName + 'dt' for s in StateVariableNames]))
        self.PortStateDerivatives = Matrix(symbols(['d' + p + IndexName + 'dt' for p in PortStateNames]))
        self.PortStates_Time = Matrix([Function(p + IndexName + '_t')(symbols('t', real=True)) for p in PortStateNames])
        self.StateSpaceEquations = self.dynamics()

    def dynamics(self):
        '''
        Inputs:
        this.StateVariables: delta,omega, eqprime
        this.InputVariables: iSd,iSq
        this.Parameters: J,D,Td0,xd,xdprime,RS,Pm,efd
        this.RefFrameAngle: angle of rotating reference frame
        this.RefFrameSpeed: speed of rotating reference frame
		this.BaseSpeed: Base speed
            
        Outputs:
        StateSpace: [diSddt ; diSqdt ; diRdt ; domegadt ; dthetadt]

        Refer Chapter 5 Section 5.5.1  - Kevin Bachovchin, Xia Miao, Marija Ilic (co-editors), State Space Modelling 
        and Primary Control of Smart Grid Components,�,Volume 2,
        Cambridge University Press for detailed model derivation
        '''
        delta, omega = self.StateVariables
        # PortInputs not explicitly used by this model. 
        J, D, xdprime, RS, eqprime, Pm = self.Parameters
        dphidt = self.RefFrameSpeed
        wb = self.BaseSpeed

        Inet = Matrix(self.PortCurrents) # I'm skipping the transpose here
        TN2M = Matrix([[sin(delta), -cos(delta)], [cos(delta), sin(delta)]])
        Imach = simplify(TN2M.inv() * Inet)
        iq = Imach[1]
        ddeltadt = omega - dphidt
        domegadt = 1 / J * (Pm + eqprime * iq - D * (omega - dphidt)) # Rotor dynamics

        return simplify(wb * Matrix([ddeltadt, domegadt]))
    
class Type4_1Gc(Module):
    '''Type 4-1 model of a synchronous machine with Governor Control'''
    def __init__(self, IndexName, RefFrameAngle, RefFrameSpeed, BaseSpeed, ParamMap=None):
        super().__init__()
        ParameterNames = ['J', 'D', 'xdprime', 'RS', 'eqprime']
        StateVariableNames = ['delta', 'omega']
        PortInputNames = ['vSd', 'vSq']
        PortStateNames = ['iSd', 'iSq']
        ControllableInputNames = ['Pm']
        SetPointNames = ['delta', 'omega', 'Pm']
        ControllerGainNames = ['Kdelta', 'Komega']

        Units = ['radians', 'rad/s'] if BaseSpeed == 1 else ['units', 'units']

        self.ParameterMap = ParamMap if ParamMap is not None and all(
            key in [p + IndexName for p in ParameterNames] for key in ParamMap.keys()) else {}
        
        self.RefFrameAngle = RefFrameAngle
        self.RefFrameSpeed = RefFrameSpeed
        self.BaseSpeed = BaseSpeed
        self.Units = Units
        self.Parameters = Matrix(symbols([p + IndexName for p in ParameterNames]))
        self.StateVariables = Matrix(symbols([s + IndexName for s in StateVariableNames]))
        self.ControllableInputs = Matrix(symbols([c + IndexName for c in ControllableInputNames]))
        self.ControllerGains = Matrix(symbols([c + IndexName for c in ControllerGainNames]))
        self.SetPoints = Matrix(symbols([sp + IndexName + '_ref' for sp in SetPointNames]))
        self.PortInputs = Matrix(symbols([p + IndexName for p in PortInputNames]))
        self.PortStates = Matrix(symbols([p + IndexName for p in PortStateNames]))

        self.PortVoltages = self.PortInputs

        delta = self.StateVariables[0]
        TN2M = Matrix([[sin(delta), -cos(delta)], [cos(delta), sin(delta)]])
        Vmach = TN2M * Matrix([[self.PortInputs[0]], [self.PortInputs[1]]])
        Imach = Matrix([[-self.Parameters[2], -self.Parameters[3]], [-self.Parameters[3], self.Parameters[2]]]).inv() * Matrix([[Vmach[1] - self.Parameters[4]], [Vmach[0]]])
        self.PortCurrents = -simplify((TN2M.inv() * Imach))

        self.PortOutputTypes = ['Current', 'Current']

        self.StateVariableDerivatives = Matrix(symbols(['d' + s + IndexName + 'dt' for s in StateVariableNames]))
        self.PortStateDerivatives = Matrix(symbols(['d' + p + IndexName + 'dt' for p in PortStateNames]))
        self.PortStates_Time = Matrix([Function(p + IndexName + '_t')(symbols('t', real=True)) for p in PortStateNames])

        self.StateSpaceEquations, self.ControlInputEquations = self.dynamics()

    def dynamics(self):
        '''
        Inputs:
        this.StateVariables: delta,omega, eqprime
        this.InputVariables: iSd,iSq
        this.Parameters: J,D,Td0,xd,xdprime,RS,Pm,efd
        this.RefFrameAngle: angle of rotating reference frame
        this.RefFrameSpeed: speed of rotating reference frame
        this.BaseSpeed: Base speed

        Outputs:
        StateSpace: [diSddt ; diSqdt ; diRdt ; domegadt ; dthetadt]
        '''
        
        # State variables
        delta, omega = self.StateVariables
        J, D, xdprime, RS, eqprime = self.Parameters
        Pm = self.ControllableInputs[0]
        K1, K2 = self.ControllerGains
        delta_ref, omega_ref, Pm_ref = self.SetPoints
        dphidt = self.RefFrameSpeed
        wb = self.BaseSpeed

        Inet = Matrix(self.PortCurrents)
        TN2M = Matrix([[sin(delta), -cos(delta)], [cos(delta), sin(delta)]])
        Imach = simplify(TN2M.inv() * Inet)
        iq = Imach[1]
        ddeltadt = omega - dphidt
        domegadt = 1 / J * (Pm + eqprime * iq - D * (omega - dphidt))

        StateSpace = wb * Matrix([ddeltadt, domegadt])

        # Control design
        Pmctrl = Pm_ref - K1 * (delta - delta_ref) - K2 * (omega - omega_ref)

        ControlInputEquations = Matrix([Pmctrl])

        return StateSpace, ControlInputEquations