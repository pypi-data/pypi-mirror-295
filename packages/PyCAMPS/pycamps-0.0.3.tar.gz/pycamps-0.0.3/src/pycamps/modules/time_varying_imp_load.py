from sympy import symbols, Function, simplify, Matrix, sin, cos, pprint
import numpy as np
from pycamps.modules.module import Module

class TimeVaryingImpLoad(Module):
    ''' Time varying impedance load as setpoints of P and Q (with filter)
        change but assumes nominal voltage
        Made by Rupa Nov 10 2017'''
    def __init__(self, IndexName, RefFrameAngle, RefFrameSpeed, BaseSpeed, ParamMap=None, data=None, t=None):
        super().__init__()
        ParameterNames = ['PL','QL']
        StateVariableNames = ['iLd','iLq']
        PortInputNames = ['vLd','vLq']
        PortStateNames = ['iLd','iLq']
        ControllableInputNames = ['RL','LL']

        Units = ['A','A'] if BaseSpeed == 1 else ['units']*2

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

        self.PortCurrents = self.PortStates
        self.PortVoltages = self.PortInputs
        self.StateVariableDerivatives =  Matrix(symbols(['d' + s + IndexName + 'dt' for s in StateVariableNames]))
        self.PortStateDerivatives =  Matrix(symbols(['d' + p + IndexName + 'dt' for p in PortStateNames]))
        self.PortStates_Time = Matrix([Function(p + IndexName + '_t')(symbols('t', real=True)) for p in PortStateNames])
        self.PortOutputTypes = ['Current', 'Current']
        self.StateSpaceEquations, self.ControlInputEquations = self.dynamics(data, t)

    def dynamics(self, data, t):
        '''
        Inputs:
        this.StateVariables: iLd,iLq
        this.InputVariables: vLd, vLq
        this.Parameters: RL, LL
            
        Outputs:
        StateSpace = [ diLddt ; diLqdt]
        ControlInputEquations
        '''
        iLd, iLq = self.StateVariables
        vLd, vLq = self.PortInputs

        if not data:
            P, Q = self.Parameters
        Ts = self.Parameters[2] if len(self.Parameters) > 2 else 10
        
        wb = self.BaseSpeed
        dphidt = self.RefFrameSpeed

        RL, LL = self.ControllableInputs
        
        if data:
            # Assuming data is a numpy array and t is defined
            tStep = data[1, 0] - data[0, 0]

            zohImpl = np.ones(int(Ts / tStep)) # zero-order hold (ZOH) implementation array
            nsamples = data.shape[0]
            tEnd = data[-1, 0]

            samples = np.arange(nsamples)

            # Sampled signal
            xSampled = np.zeros((len(t), 2))
            xSampled[::int(Ts / tStep), :] = data[samples * int(Ts), 1:3]

            # Convolution with impulse response
            xZohP = np.convolve(zohImpl, xSampled[:, 0])
            xZohQ = np.convolve(zohImpl, xSampled[:, 1])

            xZohP = xZohP[:len(t)]
            xZohQ = xZohQ[:len(t)]

            P = np.interp(t, np.arange(data[0, 0], tEnd, tStep), xZohP)
            Q = np.interp(t, np.arange(data[0, 0], tEnd, tStep), xZohQ)
        
        RL = P*(vLd**2 + vLq**2)/(P**2 + Q**2)
        LL = Q*(vLd**2 + vLq**2)/(P**2 + Q**2)
        
        # TimeVaryingImpLoad Dynamics
        diLddt = wb*(dphidt*iLq + (vLd - RL*iLd)/LL)
        diLqdt = wb*((vLq - RL*iLq)/LL - dphidt*iLd)

        StateSpace = Matrix([diLddt, diLqdt])
        ControlInputEquations = Matrix([RL, LL])

        StateSpace = simplify(StateSpace)
        return StateSpace, ControlInputEquations