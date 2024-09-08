from sympy import symbols, Function, simplify, Matrix, sin, cos, pprint
from pycamps.modules.module import Module

class ModuleTemplate(Module):
    '''Template for creating a new module. Replace this docstring with a description of the module'''
    def __init__(self, IndexName, RefFrameAngle, RefFrameSpeed, BaseSpeed, ParamMap=None):
        super().__init__()
        ParameterNames = []
        StateVariableNames = []
        PortInputNames = []
        PortStateNames = []
        ControllableInputNames = []
        InternalInputNames = []
        ControllerGainNames = []
        SetPointNames = []

        Units = [] if BaseSpeed == 1 else ['units']

        self.ParameterMap = ParamMap if ParamMap is not None and all(
            key in [p + IndexName for p in ParameterNames] for key in ParamMap.keys()) else {}
        
        self.RefFrameAngle = RefFrameAngle
        self.RefFrameSpeed = RefFrameSpeed
        self.BaseSpeed = BaseSpeed
        self.Units = Units

        self.Parameters = Matrix(symbols([p + IndexName for p in ParameterNames]))
        self.StateVariables =  Matrix(symbols([s + IndexName for s in StateVariableNames]))
        self.ControllableInputs =  Matrix(symbols([c + IndexName for c in ControllableInputNames]))
        self.InternalInputs =  Matrix(symbols([i + IndexName for i in InternalInputNames]))
        self.ControllerGains =  Matrix(symbols([c + IndexName for c in ControllerGainNames]))
        self.PortInputs =  Matrix(symbols([p + IndexName for p in PortInputNames]))
        self.PortStates =  Matrix(symbols([p + IndexName for p in PortStateNames]))

        self.PortCurrents = -self.PortStates # This varies based on module
        self.PortVoltages = self.PortInputs
        self.StateVariableDerivatives =  Matrix(symbols(['d' + s + IndexName + 'dt' for s in StateVariableNames]))
        self.PortStateDerivatives =  Matrix(symbols(['d' + p + IndexName + 'dt' for p in PortStateNames]))
        self.PortStates_Time = Matrix([Function(p + IndexName + '_t')(symbols('t', real=True)) for p in PortStateNames])
        self.SetPoints =  Matrix(symbols([p + IndexName + '_ref' for p in SetPointNames+ControllableInputNames])) # This varies based on module
        self.PortOutputTypes = []
        self.StateSpaceEquations = self.dynamics() # May also return ControlInputEquations and InternalEquations

    def dynamics(self):
        '''
        Inputs:
        this.StateVariables: 
        this.InputVariables: 
        this.Parameters:
        this.ControllableInputs: 
        this.InternalInputs: 
        this.SetPoints: 
        this.RefFrameAngle: angle of rotating reference frame
        this.RefFrameSpeed: speed of rotating reference frame
        this.BaseSpeed: Base speed
            
        Outputs:
        StateSpace: []
        ControlInputEquations
        InternalEquations

        ### Add paper reference here
        '''
        x, y, z = self.StateVariables
        a, b = self.PortInputs
        p1, p2 = self.Parameters
        t1, t2 = self.ControllableInputs
        A1, A2 = self.InternalInputs
        K1, K2, K3 = self.ControllerGains
        delta_ref, omega_ref, iF_ref = self.SetPoints
        
        Aeq, Beq = list(self.SetPoints)[-2:]
        
        wb = self.BaseSpeed
        dphidt = self.RefFrameSpeed
        
        # StateSpace
        # Use the helper function below to translate from MATLAB to Python syntax
        # Remember that MATLAB indexing starts at 1, while Python indexing starts at 0
        #   1D Matrix indexing: C(4) in MATLAB is C[3] in Python
        #   2D Matrix indexing: A(1,2) in MATLAB is A[0,1] in Python
        #   Matrix slicing: A(1:2) inclusive in MATLAB is A[0:2] exclusive in Python
        dxdt = A1*x + A2*y + a + b
        
        # Control Inputs...
        
        StateSpace = []
        Ports = []
        InternalEquations = []
        ControlInputEquations = []

        StateSpace = simplify(StateSpace)
        ControlInputEquations = simplify(ControlInputEquations)
        StateSpace = simplify(StateSpace)
        return StateSpace # May also return ControlInputEquations and InternalEquations
    
def translate_equations(equation):
    '''
    Translates MATLAB syntax to Python syntax
    '''
    equation = equation.replace(';', '')
    equation = equation.replace('==', '=')
    equation = equation.replace('^', '**')
    equation = equation.replace('...', '\\')
    
    print(equation)

if __name__ == '__main__':
    # Run this file to translate the equation, then paste it into the dynamics function
    translate_equations()