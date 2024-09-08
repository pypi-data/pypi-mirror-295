import sympy as sp

class Module:
    """
    dynamic module superclass
    """

    def __init__(self):
        self.RefFrameAngle = sp.Matrix([])  # angular position of dq ref frame
        self.RefFrameSpeed = sp.Matrix([])  # angular speed of dq ref frame
        self.BaseSpeed = sp.Matrix([])  # base speed (or inverse of time units)
        self.Parameters = sp.Matrix([])  # inductances, capacitances, etc.
        self.ControllerGains = sp.Matrix([])  # gains of controllers
        self.SetPoints = sp.Matrix([])  # set points for controllers
        self.StateVariables = sp.Matrix([])
        self.StateSpaceEquations = sp.Matrix([])
        self.StateVariableDerivatives = sp.Matrix([])
        self.ParameterMap = sp.Matrix([])  # Map of parameters to their values or functions
        self.PortInputs = sp.Matrix([])
        self.PortStates = sp.Matrix([])
        self.PortVoltages = sp.Matrix([])
        self.PortCurrents = sp.Matrix([])
        self.PortStates_Time = sp.Matrix([])
        self.PortStateDerivatives = sp.Matrix([])
        self.PortOutputTypes = sp.Matrix([])  # either "current" or "charge"
        self.ControllableInputs = sp.Matrix([])  # with passivity-based control, controllable inputs
        self.InternalInputs = sp.Matrix([])
        self.ControlInputEquations = sp.Matrix([])  # in PBC, mathematical equations for controllable inputs
        self.InternalEquations = sp.Matrix([])
        self.DesiredStateVariables = sp.Matrix([])  # with PBC, for underactuated systems, there will be desired state variables
        self.DesiredStateVariableDerivatives = sp.Matrix([])
        self.DesiredStateSpace = sp.Matrix([])
        self.SetPointOutputs = sp.Matrix([])  # set point outputs that are sent to another module
        self.SetPointOutputEquations = sp.Matrix([])  # set point
        self.GTemp = sp.Matrix([])
        self.Units = sp.Matrix([])
        self.Data = sp.Matrix([])