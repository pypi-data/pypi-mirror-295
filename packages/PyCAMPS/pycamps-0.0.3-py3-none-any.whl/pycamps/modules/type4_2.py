from sympy import symbols, Function, simplify, Matrix, sin, cos, pprint
from pycamps.modules.module import Module

'''
This module contains the Type 4-2 model of a synchronous machine and its extension with Excitation Control.
'''

class Type4_2(Module):
    '''Standard Type 4-2 model of a synchronous machine'''
    def __init__(self, IndexName, RefFrameAngle, RefFrameSpeed, BaseSpeed, ParamMap=None):
        super().__init__()
        ParameterNames = ['Td0','xd','xdprime','Rs','efd','delta']
        StateVariableNames = ['eqprime']
        PortInputNames = ['vSd','vSq']
        PortStateNames = ['iSd','iSq']

        Units = ['V'] if BaseSpeed == 1 else ['units']

        self.ParameterMap = ParamMap if ParamMap is not None and all(
            key in [p + IndexName for p in ParameterNames] for key in ParamMap.keys()) else {}
        
        self.RefFrameAngle = RefFrameAngle
        self.RefFrameSpeed = RefFrameSpeed
        self.BaseSpeed = BaseSpeed
        self.Units = Units

        self.Parameters = Matrix(symbols([p + IndexName for p in ParameterNames]))
        self.StateVariables =  Matrix(symbols([s + IndexName for s in StateVariableNames]))
        self.PortInputs =  Matrix(symbols([p + IndexName for p in PortInputNames]))
        self.PortStates =  Matrix(symbols([p + IndexName for p in PortStateNames]))
        
        self.PortVoltages = self.PortInputs

        delta = self.Parameters[5]
        TN2M = Matrix([[sin(delta), -cos(delta)], [cos(delta), sin(delta)]])
        Vmach = TN2M * Matrix([[self.PortInputs[0]], [self.PortInputs[1]]])
        xdprime, RS, eqprime = self.Parameters[2], self.Parameters[3], self.StateVariables[0]
        Imach = Matrix([[-xdprime, -RS], [-RS, xdprime]]).inv() * Matrix([[Vmach[1] - eqprime], [Vmach[0]]])
        self.PortCurrents = -simplify((TN2M.inv() * Imach)) # I'm skipping the transpose here

        self.StateVariableDerivatives =  Matrix(symbols(['d' + s + IndexName + 'dt' for s in StateVariableNames]))
        self.PortStateDerivatives =  Matrix(symbols(['d' + p + IndexName + 'dt' for p in PortStateNames]))
        self.PortStates_Time = Matrix([Function(p + IndexName + '_t')(symbols('t', real=True)) for p in PortStateNames])
        self.PortOutputTypes = ['Current', 'Current']
        self.StateSpaceEquations = self.dynamics()

    def dynamics(self):
        '''
        Inputs:
        this.StateVariables: eqprime
        this.InputVariables: vSd,vSq
        this.Parameters: Td0,xd,xdprime,Rs,efd, delta
        this.RefFrameAngle: angle of rotating reference frame
        this.RefFrameSpeed: speed of rotating reference frame
        this.BaseSpeed: Base speed
            
        Outputs:
        StateSpace: [deqprimedt]

        Refer Chapter 5 Section 5.5.2  - Kevin Bachovchin, Xia Miao, Marija Ilic (co-editors), State Space Modelling 
        and Primary Control of Smart Grid Components,,Volume 2,
        Cambridge University Press for detailed model derivation
        '''
        eqprime = self.StateVariables[0]
        vSd, vSq = self.PortInputs
        Td0, xd, xdprime, Rs, efd, delta = self.Parameters

        # Reference Transformation matrix: From network to machine
        TN2M = Matrix([[sin(delta), -cos(delta)], [cos(delta), sin(delta)]])
        vmach = TN2M * Matrix([[vSd], [vSq]])
        vd, vq = vmach
        
        # State space of machine
        deqprimedt = (-eqprime*xd/xdprime + vq*(xd-xdprime)/xdprime + efd)/Td0

        StateSpace = Matrix([deqprimedt])
        return simplify(StateSpace)
    
class Type4_2Ec(Module):
    '''Type 4-2 model of a synchronous machine with excitation control'''
    def __init__(self, IndexName, RefFrameAngle, RefFrameSpeed, BaseSpeed, ParamMap=None):
        super().__init__()
        ParameterNames = ['Td0','xd','xdprime','Rs','delta']
        StateVariableNames = ['eqprime']
        PortInputNames = ['vSd','vSq']
        PortStateNames = ['iSd','iSq']
        ControllableInputNames = ['efd']
        ControllerGainNames = ['Keqprime']
        SetPointNames = ['eqprime', 'efd']

        Units = ['V'] if BaseSpeed == 1 else ['units']

        self.ParameterMap = ParamMap if ParamMap is not None and all(
            key in [p + IndexName for p in ParameterNames] for key in ParamMap.keys()) else {}
        
        self.RefFrameAngle = RefFrameAngle
        self.RefFrameSpeed = RefFrameSpeed
        self.BaseSpeed = BaseSpeed
        self.Units = Units

        self.Parameters = Matrix(symbols([p + IndexName for p in ParameterNames]))
        self.StateVariables =  Matrix(symbols([s + IndexName for s in StateVariableNames]))
        self.ControllableInputs =  Matrix(symbols([c + IndexName for c in ControllableInputNames]))
        self.ControllerGains =  Matrix(symbols([c + IndexName for c in ControllerGainNames]))
        self.SetPoints =  Matrix(symbols([p + IndexName + '_ref' for p in SetPointNames]))
        self.PortInputs =  Matrix(symbols([p + IndexName for p in PortInputNames]))
        self.PortStates =  Matrix(symbols([p + IndexName for p in PortStateNames]))
        
        self.PortVoltages = self.PortInputs

        delta = self.Parameters[4]
        TN2M = Matrix([[sin(delta), -cos(delta)], [cos(delta), sin(delta)]])
        Vmach = TN2M * Matrix([[self.PortInputs[0]], [self.PortInputs[1]]])
        xdprime, RS, eqprime = self.Parameters[2], self.Parameters[3], self.StateVariables[0]
        Imach = Matrix([[-xdprime, -RS], [-RS, xdprime]]).inv() * Matrix([[Vmach[1] - eqprime], [Vmach[0]]])
        self.PortCurrents = -simplify((TN2M.inv() * Imach)) # I'm skipping the transpose here

        self.StateVariableDerivatives =  Matrix(symbols(['d' + s + IndexName + 'dt' for s in StateVariableNames]))
        self.PortStateDerivatives =  Matrix(symbols(['d' + p + IndexName + 'dt' for p in PortStateNames]))
        self.PortStates_Time = Matrix([Function(p + IndexName + '_t')(symbols('t', real=True)) for p in PortStateNames])
        self.PortOutputTypes = ['Current', 'Current']
        self.StateSpaceEquations, self.ControlInputEquations = self.dynamics()

    def dynamics(self):
        '''
        Inputs:
        this.StateVariables: eqprime
        this.InputVariables: vSd,vSq
        this.Parameters: Td0,xd,xdprime,Rs,efd, delta
        this.RefFrameAngle: angle of rotating reference frame
        this.RefFrameSpeed: speed of rotating reference frame
		this.BaseSpeed: Base speed
            
        Outputs:
        StateSpace: [deqprimedt]

        Refer Chapter 5 Section 5.5.2  - Kevin Bachovchin, Xia Miao, Marija Ilic (co-editors), State Space Modelling 
        and Primary Control of Smart Grid Components,,Volume 2,
        Cambridge University Press for detailed model derivation
        '''
        eqprime = self.StateVariables[0]
        vSd, vSq = self.PortInputs
        Td0, xd, xdprime, Rs, delta = self.Parameters
        efd = self.ControllableInputs[0]
        K1 = self.ControllerGains[0]
        eqprime_ref, efd_ref = self.SetPoints

        # Reference Transformation matrix: From network to machine
        TN2M = Matrix([[sin(delta), -cos(delta)], [cos(delta), sin(delta)]])
        vmach = TN2M * Matrix([[vSd], [vSq]])
        vd, vq = vmach
        
        # State space of machine
        deqprimedt = (-eqprime*xd/xdprime + vq*(xd-xdprime)/xdprime + efd)/Td0
        StateSpace = Matrix([deqprimedt])

        # Control design
        efdctrl = efd_ref - K1*(eqprime - eqprime_ref)
        ControlInputEquations = Matrix([efdctrl])

        return simplify(StateSpace), simplify(ControlInputEquations)