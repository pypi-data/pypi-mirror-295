from sympy import symbols, Function, simplify, Matrix, sin, cos, pprint
from pycamps.modules.module import Module

class SM7StateControl(Module):
    '''This module is still under development and is not yet functional'''
    def __init__(self, IndexName, RefFrameAngle, RefFrameSpeed, BaseSpeed, ParamMap=None):
        super().__init__()
        ParameterNames = ['LSd','LSq','LF','LRD','LRQ','Lad','Laq','Laf','Ldf','RS','RF','Rkd','Rkq','H','F']
        StateVariableNames = ['iSd','iSq','iRd','iRq','iF','delta','omega']
        PortInputNames = ['vSd','vSq']
        PortStateNames = ['iSd','iSq']
        ControllableInputNames = ['Tm','vF']
        InternalInputNames = ['A11', 'A12', 'A13', 'A14', 'A21', 'A22', 'A23', 'A24', 'C1', 'C2']
        ControllerGainNames = ['K1','K2','K3']
        SetPointNames = ['delta','omega','iF']

        Units = ['A','A','A','A','A','rad','rad/s'] if BaseSpeed == 1 else ['units']*7

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

        self.PortCurrents = -self.PortStates
        self.PortVoltages = self.PortInputs
        self.StateVariableDerivatives =  Matrix(symbols(['d' + s + IndexName + 'dt' for s in StateVariableNames]))
        self.PortStateDerivatives =  Matrix(symbols(['d' + p + IndexName + 'dt' for p in PortStateNames]))
        self.PortStates_Time = Matrix([Function(p + IndexName + '_t')(symbols('t', real=True)) for p in PortStateNames])
        self.SetPoints =  Matrix(symbols([p + IndexName + '_ref' for p in SetPointNames+ControllableInputNames]))
        self.PortOutputTypes = ['Current', 'Current']
        self.StateSpaceEquations, self.ControlInputEquations, self.InternalEquations = self.dynamics()

    def dynamics(self):
        '''
        Inputs:
        this.StateVariables: iSd,iSq,iR,omega,theta
        this.InputVariables: vSd,vSq
        this.Parameters: LSd, LSq, LF, LRd, LRq - diagonal elements of L matrix
        			Lad, Laf, Laq, Ldf - off-diagonal elemts of inductance matrix
        			H, F - Mechanical parameters - Inertia constant and damping
        this.ControllableInputs: Tm, vF
        this.InternalInputs: A11,A12,A13,A14,A21,A22,A23,A24,C1,C2
        this.SetPoints: Tm_ref, vF_ref, iF_ref, delta_ref, omega_ref
        this.RefFrameAngle: angle of rotating reference frame
        this.RefFrameSpeed: speed of rotating reference frame
        this.BaseSpeed: Base speed
            
        Outputs:
        StateSpace: [diSddt ; diSqdt ; diRdt ; domegadt ; dthetadt]
        ControlInputEquations
        InternalEquations

        Refer 'Milos Cvetkovic, Power-Electronics-Enabled Transient Stabilization
        of Power Systems, Ph.D.Thesis, Page 76-78'
        '''
        iSd, iSq, iRd, iRq, iF, delta, omega = self.StateVariables
        vSd, vSq = self.PortInputs
        LSd, LSq, LF, LRd, LRq, Lad, Laq, Laf, Ldf, RS, RF, Rkd, Rkq, H, F = self.Parameters
        Tm, vf = self.ControllableInputs
        A11, A12, A13, A14, A21, A22, A23, A24, C1, C2 = self.InternalInputs
        K1, K2, K3 = self.ControllerGains
        delta_ref, omega_ref, iF_ref = self.SetPoints[:3]
        
        Tmeq, vfeq = list(self.SetPoints)[-2:]
        
        wb = self.BaseSpeed
        omega0 = self.RefFrameSpeed
        
        # StateSpace
        diSddt = -wb*(iF*((RF*sin(delta)*(LRd*Laf - Lad*Ldf))/(LF*Lad**2 - 2*Lad*Laf*Ldf + LRd*Laf**2 + LSd*Ldf**2 - LRd*LF*LSd) - (LRq*Laf*omega*cos(delta))/(Laq**2 - LRq*LSq)) + iRd*((Rkd*sin(delta)*(LF*Lad - Laf*Ldf))/(LF*Lad**2 - 2*Lad*Laf*Ldf + LRd*Laf**2 + LSd*Ldf**2 - LRd*LF*LSd) - (LRq*Lad*omega*cos(delta))/(Laq**2 - LRq*LSq)) - vSd*(LRq/(2*(Laq**2 - LRq*LSq)) + cos(2*delta)*(LRq/(2*(Laq**2 - LRq*LSq)) + (Ldf**2 - LRd*LF)/(2*(LF*Lad**2 - 2*Lad*Laf*Ldf + LRd*Laf**2 + LSd*Ldf**2 - LRd*LF*LSd))) - (Ldf**2 - LRd*LF)/(2*(LF*Lad**2 - 2*Lad*Laf*Ldf + LRd*Laf**2 + LSd*Ldf**2 - LRd*LF*LSd))) + iSq*(omega - omega0 + omega*((LRq*LSd)/(2*(Laq**2 - LRq*LSq)) - (LSq*(Ldf**2 - LRd*LF))/(2*(LF*Lad**2 - 2*Lad*Laf*Ldf + LRd*Laf**2 + LSd*Ldf**2 - LRd*LF*LSd))) - RS*sin(2*delta)*(LRq/(2*(Laq**2 - LRq*LSq)) + (Ldf**2 - LRd*LF)/(2*(LF*Lad**2 - 2*Lad*Laf*Ldf + LRd*Laf**2 + LSd*Ldf**2 - LRd*LF*LSd))) + omega*cos(2*delta)*((LRq*LSd)/(2*(Laq**2 - LRq*LSq)) + (LSq*(Ldf**2 - LRd*LF))/(2*(LF*Lad**2 - 2*Lad*Laf*Ldf + LRd*Laf**2 + LSd*Ldf**2 - LRd*LF*LSd)))) + iRq*((Laq*Rkq*cos(delta))/(Laq**2 - LRq*LSq) - (Laq*omega*sin(delta)*(Ldf**2 - LRd*LF))/(LF*Lad**2 - 2*Lad*Laf*Ldf + LRd*Laf**2 + LSd*Ldf**2 - LRd*LF*LSd)) - iSd*(RS*(LRq/(2*(Laq**2 - LRq*LSq)) - (Ldf**2 - LRd*LF)/(2*(LF*Lad**2 - 2*Lad*Laf*Ldf + LRd*Laf**2 + LSd*Ldf**2 - LRd*LF*LSd))) + RS*cos(2*delta)*(LRq/(2*(Laq**2 - LRq*LSq)) + (Ldf**2 - LRd*LF)/(2*(LF*Lad**2 - 2*Lad*Laf*Ldf + LRd*Laf**2 + LSd*Ldf**2 - LRd*LF*LSd))) + omega*sin(2*delta)*((LRq*LSd)/(2*(Laq**2 - LRq*LSq)) + (LSq*(Ldf**2 - LRd*LF))/(2*(LF*Lad**2 - 2*Lad*Laf*Ldf + LRd*Laf**2 + LSd*Ldf**2 - LRd*LF*LSd)))) - vSq*sin(2*delta)*(LRq/(2*(Laq**2 - LRq*LSq)) + (Ldf**2 - LRd*LF)/(2*(LF*Lad**2 - 2*Lad*Laf*Ldf + LRd*Laf**2 + LSd*Ldf**2 - LRd*LF*LSd))) + (vf*sin(delta)*(LRd*Laf - Lad*Ldf))/(LF*Lad**2 - 2*Lad*Laf*Ldf + LRd*Laf**2 + LSd*Ldf**2 - LRd*LF*LSd))
        diSqdt = wb*(iF*((RF*cos(delta)*(LRd*Laf - Lad*Ldf))/(LF*Lad**2 - 2*Lad*Laf*Ldf + LRd*Laf**2 + LSd*Ldf**2 - LRd*LF*LSd) + (LRq*Laf*omega*sin(delta))/(Laq**2 - LRq*LSq)) + iRd*((Rkd*cos(delta)*(LF*Lad - Laf*Ldf))/(LF*Lad**2 - 2*Lad*Laf*Ldf + LRd*Laf**2 + LSd*Ldf**2 - LRd*LF*LSd) + (LRq*Lad*omega*sin(delta))/(Laq**2 - LRq*LSq)) - vSq*(cos(2*delta)*(LRq/(2*(Laq**2 - LRq*LSq)) + (Ldf**2 - LRd*LF)/(2*(LF*Lad**2 - 2*Lad*Laf*Ldf + LRd*Laf**2 + LSd*Ldf**2 - LRd*LF*LSd))) - LRq/(2*(Laq**2 - LRq*LSq)) + (Ldf**2 - LRd*LF)/(2*(LF*Lad**2 - 2*Lad*Laf*Ldf + LRd*Laf**2 + LSd*Ldf**2 - LRd*LF*LSd))) + iSd*(omega - omega0 + omega*((LRq*LSd)/(2*(Laq**2 - LRq*LSq)) - (LSq*(Ldf**2 - LRd*LF))/(2*(LF*Lad**2 - 2*Lad*Laf*Ldf + LRd*Laf**2 + LSd*Ldf**2 - LRd*LF*LSd))) + RS*sin(2*delta)*(LRq/(2*(Laq**2 - LRq*LSq)) + (Ldf**2 - LRd*LF)/(2*(LF*Lad**2 - 2*Lad*Laf*Ldf + LRd*Laf**2 + LSd*Ldf**2 - LRd*LF*LSd))) - omega*cos(2*delta)*((LRq*LSd)/(2*(Laq**2 - LRq*LSq)) + (LSq*(Ldf**2 - LRd*LF))/(2*(LF*Lad**2 - 2*Lad*Laf*Ldf + LRd*Laf**2 + LSd*Ldf**2 - LRd*LF*LSd)))) - iRq*((Laq*Rkq*sin(delta))/(Laq**2 - LRq*LSq) + (Laq*omega*cos(delta)*(Ldf**2 - LRd*LF))/(LF*Lad**2 - 2*Lad*Laf*Ldf + LRd*Laf**2 + LSd*Ldf**2 - LRd*LF*LSd)) - iSq*(RS*cos(2*delta)*(LRq/(2*(Laq**2 - LRq*LSq)) + (Ldf**2 - LRd*LF)/(2*(LF*Lad**2 - 2*Lad*Laf*Ldf + LRd*Laf**2 + LSd*Ldf**2 - LRd*LF*LSd))) - RS*(LRq/(2*(Laq**2 - LRq*LSq)) - (Ldf**2 - LRd*LF)/(2*(LF*Lad**2 - 2*Lad*Laf*Ldf + LRd*Laf**2 + LSd*Ldf**2 - LRd*LF*LSd))) + omega*sin(2*delta)*((LRq*LSd)/(2*(Laq**2 - LRq*LSq)) + (LSq*(Ldf**2 - LRd*LF))/(2*(LF*Lad**2 - 2*Lad*Laf*Ldf + LRd*Laf**2 + LSd*Ldf**2 - LRd*LF*LSd)))) + vSd*sin(2*delta)*(LRq/(2*(Laq**2 - LRq*LSq)) + (Ldf**2 - LRd*LF)/(2*(LF*Lad**2 - 2*Lad*Laf*Ldf + LRd*Laf**2 + LSd*Ldf**2 - LRd*LF*LSd))) + (vf*cos(delta)*(LRd*Laf - Lad*Ldf))/(LF*Lad**2 - 2*Lad*Laf*Ldf + LRd*Laf**2 + LSd*Ldf**2 - LRd*LF*LSd))
        diRddt = wb*(iSq*((RS*cos(delta)*(LF*Lad - Laf*Ldf))/(LF*Lad**2 - 2*Lad*Laf*Ldf + LRd*Laf**2 + LSd*Ldf**2 - LRd*LF*LSd) + (LSq*omega*sin(delta)*(LF*Lad - Laf*Ldf))/(LF*Lad**2 - 2*Lad*Laf*Ldf + LRd*Laf**2 + LSd*Ldf**2 - LRd*LF*LSd)) - iSd*((RS*sin(delta)*(LF*Lad - Laf*Ldf))/(LF*Lad**2 - 2*Lad*Laf*Ldf + LRd*Laf**2 + LSd*Ldf**2 - LRd*LF*LSd) - (LSq*omega*cos(delta)*(LF*Lad - Laf*Ldf))/(LF*Lad**2 - 2*Lad*Laf*Ldf + LRd*Laf**2 + LSd*Ldf**2 - LRd*LF*LSd)) + (vf*(Lad*Laf - LSd*Ldf))/(LF*Lad**2 - 2*Lad*Laf*Ldf + LRd*Laf**2 + LSd*Ldf**2 - LRd*LF*LSd) + (vSq*cos(delta)*(LF*Lad - Laf*Ldf))/(LF*Lad**2 - 2*Lad*Laf*Ldf + LRd*Laf**2 + LSd*Ldf**2 - LRd*LF*LSd) - (vSd*sin(delta)*(LF*Lad - Laf*Ldf))/(LF*Lad**2 - 2*Lad*Laf*Ldf + LRd*Laf**2 + LSd*Ldf**2 - LRd*LF*LSd) - (iRd*Rkd*(Laf**2 - LF*LSd))/(LF*Lad**2 - 2*Lad*Laf*Ldf + LRd*Laf**2 + LSd*Ldf**2 - LRd*LF*LSd) + (iF*RF*(Lad*Laf - LSd*Ldf))/(LF*Lad**2 - 2*Lad*Laf*Ldf + LRd*Laf**2 + LSd*Ldf**2 - LRd*LF*LSd) + (Laq*iRq*omega*(LF*Lad - Laf*Ldf))/(LF*Lad**2 - 2*Lad*Laf*Ldf + LRd*Laf**2 + LSd*Ldf**2 - LRd*LF*LSd))
        diFdt = -wb*(iSd*((RS*sin(delta)*(LRd*Laf - Lad*Ldf))/(LF*Lad**2 - 2*Lad*Laf*Ldf + LRd*Laf**2 + LSd*Ldf**2 - LRd*LF*LSd) - (LSq*omega*cos(delta)*(LRd*Laf - Lad*Ldf))/(LF*Lad**2 - 2*Lad*Laf*Ldf + LRd*Laf**2 + LSd*Ldf**2 - LRd*LF*LSd)) - iSq*((RS*cos(delta)*(LRd*Laf - Lad*Ldf))/(LF*Lad**2 - 2*Lad*Laf*Ldf + LRd*Laf**2 + LSd*Ldf**2 - LRd*LF*LSd) + (LSq*omega*sin(delta)*(LRd*Laf - Lad*Ldf))/(LF*Lad**2 - 2*Lad*Laf*Ldf + LRd*Laf**2 + LSd*Ldf**2 - LRd*LF*LSd)) + (vf*(Lad**2 - LRd*LSd))/(LF*Lad**2 - 2*Lad*Laf*Ldf + LRd*Laf**2 + LSd*Ldf**2 - LRd*LF*LSd) - (vSq*cos(delta)*(LRd*Laf - Lad*Ldf))/(LF*Lad**2 - 2*Lad*Laf*Ldf + LRd*Laf**2 + LSd*Ldf**2 - LRd*LF*LSd) + (vSd*sin(delta)*(LRd*Laf - Lad*Ldf))/(LF*Lad**2 - 2*Lad*Laf*Ldf + LRd*Laf**2 + LSd*Ldf**2 - LRd*LF*LSd) + (iF*RF*(Lad**2 - LRd*LSd))/(LF*Lad**2 - 2*Lad*Laf*Ldf + LRd*Laf**2 + LSd*Ldf**2 - LRd*LF*LSd) - (iRd*Rkd*(Lad*Laf - LSd*Ldf))/(LF*Lad**2 - 2*Lad*Laf*Ldf + LRd*Laf**2 + LSd*Ldf**2 - LRd*LF*LSd) - (Laq*iRq*omega*(LRd*Laf - Lad*Ldf))/(LF*Lad**2 - 2*Lad*Laf*Ldf + LRd*Laf**2 + LSd*Ldf**2 - LRd*LF*LSd))
        diRqdt = -wb*(iSd*((Laq*RS*cos(delta))/(Laq**2 - LRq*LSq) + (Laq*LSd*omega*sin(delta))/(Laq**2 - LRq*LSq)) + iSq*((Laq*RS*sin(delta))/(Laq**2 - LRq*LSq) - (Laq*LSd*omega*cos(delta))/(Laq**2 - LRq*LSq)) + (Laq*vSd*cos(delta))/(Laq**2 - LRq*LSq) + (Laq*vSq*sin(delta))/(Laq**2 - LRq*LSq) - (LSq*iRq*Rkq)/(Laq**2 - LRq*LSq) + (Lad*Laq*iRd*omega)/(Laq**2 - LRq*LSq) + (Laf*Laq*iF*omega)/(Laq**2 - LRq*LSq))
        ddeltadt = wb*(omega - omega0)
        domegadt = -(iSd*vSd - Tm +F*(omega-omega0) + iSq*vSq)/(2*H)
        
        # Control Inputs
        Tm = -K1*(delta-delta_ref) - K2*(omega-omega_ref)+ Tmeq
        vf = -K3*(iF-iF_ref) + vfeq
    
        StateSpace = Matrix([diSddt, diSqdt, diRddt, diRqdt, diFdt, ddeltadt, domegadt])
        
        Ports = Matrix([iSd, iSq, vSd, vSq])
        A = Matrix(StateSpace[:2]).jacobian(Ports)
        C = Matrix(StateSpace[:2]) - A*Ports
        # pprint(A)

        StateSpace[0] = A11*iSd + A12*iSq + A13*vSd + A14*vSq + C1
        StateSpace[1] = A21*iSd + A22*iSq + A23*vSd + A24*vSq + C2
        InternalEquations = Matrix([A[0,0], A[0,1], A[0,2], A[0,3], A[1,0], A[1,1], A[1,2], A[1,3], C[0], C[1]])
        # print("Internal Equations")
        # pprint(InternalEquations)
        
        ControlInputEquations = Matrix([Tm, vf])
        StateSpace = simplify(StateSpace)
        ControlInputEquations = simplify(ControlInputEquations)
        return StateSpace, ControlInputEquations, InternalEquations
    
if __name__ == '__main__':
    sm7 = SM7StateControl('1', 0, 1, 1)
    pprint(sm7.StateSpaceEquations)
    pprint(sm7.ControlInputEquations)
    pprint(sm7.InternalEquations)