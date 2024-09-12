from sympy import symbols, simplify, Matrix, sin, cos, I, re, im, Function, pi, sqrt
from pycamps.modules.module import Module

'''
This module contains the Type 4-1 model of a synchronous machine and its extension with Governor and Excitation Control.
'''

class SMOneAxis(Module):
    '''
    Implements one axis model of synchronous machine.
    '''
    def __init__(self, IndexName, RefFrameAngle, RefFrameSpeed, BaseSpeed, ParamMap=None):
        super().__init__()
        ParameterNames = ['J','D','Td0','xd','xdprime','RS','Pm','efd']
        StateVariableNames = ['eqprime','delta','omega']
        PortInputNames = ['vSd', 'vSq']
        PortStateNames = ['iSd', 'iSq'] # These are not necessarily states. They are outputs instead
        SetPointNames = []

        Units = ['V','radians','rad/s'] if BaseSpeed == 1 else ['units','units','units']

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

        eqprime, delta = self.StateVariables[0], self.StateVariables[1]
        TN2M = Matrix([[cos(delta), sin(delta)], [-sin(delta), cos(delta)]])
        Vmach = TN2M * Matrix([[self.PortInputs[0]], [self.PortInputs[1]]])
        xdprime, RS = self.Parameters[4], self.Parameters[5]
        Imach = Matrix([[-xdprime, -RS], [-RS, xdprime]]).inv() * Matrix([[Vmach[1] - eqprime], [Vmach[0]]])
        self.PortCurrents = -simplify((TN2M.inv() * Imach)) # I'm skipping the transpose here
        self.PortOutputTypes = ['Current', 'Current']
        self.StateVariableDerivatives = Matrix(symbols(['d' + s + IndexName + 'dt' for s in StateVariableNames]))
        self.PortStateDerivatives = Matrix(symbols(['d' + p + IndexName + 'dt' for p in PortStateNames]))
        self.PortStates_Time = Matrix(symbols([p + IndexName + '_t(t)' for p in PortStateNames]))
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
        StateSpace: [deqprimedt; ddeltadt ; domegadt]

        Refer Ilic, Marija D and Zaborszky, John, Dynamics and control
        of large electric power systems,2000, Wiley New York for
        detailed model derivation.
        '''
        J, D, Td0, xd, xdprime, RS, Pm, efd = self.Parameters
        eqprime, delta, omega = self.StateVariables
        iSd, iSq = self.PortStates
        vSd, vSq = self.PortInputs
        
        dphidt = self.RefFrameSpeed
        wb = self.BaseSpeed

        # Reference Transformation matrix: From network to machine
        TN2M = Matrix([[cos(delta), sin(delta)], [-sin(delta), cos(delta)]])

        vmach = TN2M*Matrix([[vSd],[vSq]])
        vd, vq = vmach
        
        imach = -(vd + I*(vq-eqprime))/(RS + I*xdprime)
        id, iq = re(imach), im(imach)

        # State space of machine
        ddeltadt = wb*(omega-dphidt)
        domegadt = 1/J*(Pm - eqprime*iq - D*(omega-dphidt))   # Rotor dynamics
        deqprimedt = (-(xd-xdprime)*id - eqprime + efd)/Td0

        return Matrix([deqprimedt, ddeltadt, domegadt])
    
class SMOneAxisV2GcEc(Module):
    ''' Implements Governor and excitation control on one axis model of
        synchronous machine. The model treats stator currents as port inputs
        and voltages as port states.
        Created by Xia Miao for ONR project - extracted and modified by Rupa on Nov 4, 2020'''
    def __init__(self, IndexName, RefFrameAngle, RefFrameSpeed, BaseSpeed, ParamMap=None):
        super().__init__()
        ParameterNames = ['H','F','Td0','xd','xdprime','rs']
        StateVariableNames = ['delta','omega','eqprime','Pm','omegaInt','a','Vr','efd','Vf']
        PortInputNames = ['iSd','iSq']
        PortStateNames = ['vSd','vSq']
        ControllerGainNames = ['Tg','Kt','r','Kp','Ki','Tu','Ka','Ta','Ke','Te','Tf']
        SetPointNames = ['omega','Vt','P']

        Units = ['radians','rad/s','W','W','A','A','rad/s','W','W','A','A'] if BaseSpeed == 1 else ['units']*11

        self.ParameterMap = ParamMap if ParamMap is not None and all(
            key in [p + IndexName for p in ParameterNames] for key in ParamMap.keys()) else {}
        
        self.RefFrameAngle = RefFrameAngle
        self.RefFrameSpeed = RefFrameSpeed
        self.BaseSpeed = BaseSpeed
        self.Units = Units

        self.Parameters = Matrix(symbols([p + IndexName for p in ParameterNames]))
        self.StateVariables =  Matrix(symbols([s + IndexName for s in StateVariableNames]))
        self.ControllerGains =  Matrix(symbols([c + IndexName for c in ControllerGainNames]))
        self.PortInputs =  Matrix(symbols([p + IndexName for p in PortInputNames]))
        self.PortStates =  Matrix(symbols([p + IndexName for p in PortStateNames]))

        self.PortCurrents = self.PortInputs
        delta, eqprime = self.StateVariables[:2]
        TN2M = Matrix([[sin(delta), cos(delta)], [-cos(delta), sin(delta)]])

        # Get eqprime in network reference
        E = (TN2M.inv() * Matrix([[0], [eqprime]]))
        vSd, vSq = E
        self.PortVoltages = Matrix([vSd, vSq])

        self.StateVariableDerivatives =  Matrix(symbols(['d' + s + IndexName + 'dt' for s in StateVariableNames]))
        self.PortStateDerivatives =  Matrix(symbols(['d' + p + IndexName + 'dt' for p in PortStateNames]))
        self.PortStates_Time = Matrix([Function(p + IndexName + '_t')(symbols('t', real=True)) for p in PortStateNames])
        self.SetPoints =  Matrix(symbols([p + IndexName + '_ref' for p in SetPointNames]))
        self.PortOutputTypes = ['Current', 'Current']
        self.StateSpaceEquations = self.dynamics()

    def dynamics(self):
        '''
        Inputs:
        this.StateVariables: delta, omega,eqprime, Pm, omegaInt, a, Vr, efd, Vf;
        this.InputVariables: iSd,iSq
        this.ControllerGains: Tg,Kt,r,Kp,Ki,Tu,Ka,Ta,Ke,Te,Tf
        this.SetPoints: omega_ref, Vt_ref, P_ref; 
        this.Parameters: H,F,Td0,xd,xdprime,rs
        this.RefFrameAngle: angle of rotating reference frame
        this.RefFrameSpeed: speed of rotating reference frame
        this.BaseSpeed: Base speed
            
        Outputs:
        StateSpace: [diSddt ; diSqdt ; diRdt ; domegadt ; dthetadt]
        ControlInputEquations

        Refer Ilic, Marija D and Zaborszky, John, Dynamics and control
        of large electric power systems,2000, Wiley New York for
        detailed open-loop model derivation
        The governor and exciter controllers are standard IEEE-TYPE 1. Refer Chapter 5 Section 5.5.2  - Kevin Bachovchin, Xia Miao, Marija Ilic (co-editors), State Space Modelling 
        and Primary Control of Smart Grid Components,,Volume 2,
        Cambridge University Press for governor and excitation controllers
        '''
        delta, omega, eqprime, Pm, omegaInt, a, Vr, efd, Vf = self.StateVariables
        iSd, iSq = -self.PortInputs
        H, D, Td0, xd, xdprime, Rs = self.Parameters
        Tg, Kt, r, Ki, Kp, Tu, Ka, Ta, Ke, Te, Tf = self.ControllerGains
        omega0, Vref, Pmref = self.SetPoints

        dphidt = self.RefFrameSpeed
        wb = self.BaseSpeed
        
        # Reference Transformation matrix: From network to machine
        TN2M = Matrix([[sin(delta), cos(delta)], [-cos(delta), sin(delta)]])
        imach = TN2M * Matrix([[iSd], [iSq]])
        id, iq = imach

        # Get eqprime in network reference
        E = (TN2M.inv() * Matrix([[0], [eqprime]]))
        vSd, vSq = E

        # machine dynamics 
        ddeltadt = -wb*(delta -pi/2)
        domegadt = 1/(2*H)*(Pm + Pmref - eqprime*iq - D*(omega - dphidt))
        deqprimedt = 1/Td0*(-eqprime -(xd - xdprime)*id +efd)

        # Governor control
        dPmdt = (-Pm + Kt*a)/Tu
        domegaIntdt = (omega-omega0)
        dadt = (-Kp*(omega-omega0) - Ki*omegaInt - a*r)/Tg

        # Exciter control - IEEE Type 1
        Vt = sqrt(vSd**2 + vSq**2)
        # Vt = eqprime
        dVrdt = (-Vr + Ka*(Vref - Vt - Vf))/Ta
        defddt = (-Ke*efd + Vr)/Te
        dVfdt = (-Vf + 0*defddt)/Tf
        
        StateSpace = Matrix([ddeltadt, domegadt, deqprimedt, dPmdt, domegaIntdt, dadt, dVrdt, defddt, dVfdt])
        StateSpace = simplify(StateSpace)
        return StateSpace