from sympy import symbols, Function, simplify, Matrix, sin, cos, pprint, diag, jacobian
from pycamps.modules.module import Module

class SMFundamental(Module):
    '''Fundamental model of a synchronous machine'''
    def __init__(self, IndexName, RefFrameAngle, RefFrameSpeed, BaseSpeed, ParamMap=None):
        super().__init__()
        ParameterNames = ['rs','Lls','Lmd','Lmq','rfd','Llfd','rkd','Llkd','rkq1','Llkq1','H','F','Tm','vfd']
        StateVariableNames = ['iSd','iSq','ifd','ikd','ikq1','delta','omega']
        PortInputNames = ['vSd','vSq']
        PortStateNames = ['iSd','iSq']
        InternalInputNames = ['A11', 'A12', 'A13', 'A14', 'A21', 'A22', 'A23', 'A24', 'C1', 'C2']

        Units = ['A','A','A','A','A','radians','rad/s'] if BaseSpeed == 1 else ['units']*7

        self.ParameterMap = ParamMap if ParamMap is not None and all(
            key in [p + IndexName for p in ParameterNames] for key in ParamMap.keys()) else {}
        
        self.RefFrameAngle = RefFrameAngle
        self.RefFrameSpeed = RefFrameSpeed
        self.BaseSpeed = BaseSpeed
        self.Units = Units

        self.Parameters = Matrix(symbols([p + IndexName for p in ParameterNames]))
        self.StateVariables =  Matrix(symbols([s + IndexName for s in StateVariableNames]))
        self.InternalInputs =  Matrix(symbols([i + IndexName for i in InternalInputNames]))
        self.PortInputs =  Matrix(symbols([p + IndexName for p in PortInputNames]))
        self.PortStates =  Matrix(symbols([p + IndexName for p in PortStateNames]))

        self.PortCurrents = self.PortStates
        self.PortVoltages = self.PortInputs
        self.StateVariableDerivatives =  Matrix(symbols(['d' + s + IndexName + 'dt' for s in StateVariableNames]))
        self.PortStateDerivatives =  Matrix(symbols(['d' + p + IndexName + 'dt' for p in PortStateNames]))
        self.PortStates_Time = Matrix([Function(p + IndexName + '_t')(symbols('t', real=True)) for p in PortStateNames])
        self.PortOutputTypes = ['Current']*2
        self.StateSpaceEquations, self.InternalEquations = self.dynamics()

    def dynamics(self):
        '''
        Inputs:
        this.StateVariables: iSd,iSq,ifd,ikd,ikq1,delta,omega
        this.InputVariables: vSd,vSq
        this.Parameters: Lls, Lmd, Lmq, Llfd, Llkd, Llkq1-Inductances
        			rs, rfd, rkd, rkq1 - resitances
        			H, F - Mechanical parameters
                   Tm, vF - control inputs
        this.InternalInputs: A11,A12,A13,A14,A21,A22,A23,A24,C1,C2
        this.RefFrameAngle: angle of rotating reference frame
        this.RefFrameSpeed: speed of rotating reference frame
        this.BaseSpeed: Base speed
            
        Outputs:
        StateSpace: [diSddt ; diSqdt ; difddt ; dikddt; dikq1dt; ddeltadt; domegadt]
        InternalEquations

        Krause, P.C., Analysis of Electric Machinery, McGraw-Hill, 1986, Chapter 5
        '''
        iSd, iSq, ifd, ikd, ikq1, delta, omega = self.StateVariables
        vSd, vSq = self.PortInputs
        rs, Lls, Lmd, Lmq, rfd, Llfd, rkd, Llkd, rkq1, Llkq1, H, F, Tm, vfd = self.Parameters
        A11, A12, A13, A14, A21, A22, A23, A24, C1, C2 = self.InternalInputs
    
        wb = self.BaseSpeed
        omega0 = self.RefFrameSpeed
        
        # Transformation matrix
        T = Matrix([[cos(delta), sin(delta)], [-sin(delta), cos(delta)]])

        # Derivative fo transformation matrix
        P = (omega-omega0)*Matrix([[-sin(delta), -cos(delta)], [cos(delta), -sin(delta)]])               

        # In rotor reference frame        
        i_rot = T*Matrix([iSd, iSq])
        v_rot = T*Matrix([vSd, vSq])
        ids, iqs = i_rot
        vds, vqs = v_rot

        # Vector of currents in rotor reference
        I = Matrix([ids, iqs, ifd, ikd, ikq1])
        
        # Vector of voltages in rotor reference
        V = Matrix([vds, vqs, vfd, 0, 0])

        # Inductance matrix
        Ls = diag(Lls + Lmd, Lls + Lmq)
        Lsr = Matrix([[Lmd, Lmd, 0], [0, 0, Lmq]])
        Lr = Matrix([[Llfd + Lmd, Lmd, 0], [Lmd, Llkd + Lmd, 0], [0, 0, Llkq1 + Lmq]])
        L = Matrix.vstack(Matrix.hstack(Ls, Lsr), Matrix.hstack(Lsr.T, Lr))

        # Resistance matrix
        R = diag(rs, rs, rfd, rkd, rkq1)

        # Flux linkage
        psi = L * I

        # Flux induced due to relative motion
        S = Matrix([-omega * psi[1], omega * psi[0], 0, 0, 0])

        # Electrical Dynamics
        dpsidt = V - R*I - S
        dIdt = wb * (L.inv() * dpsidt)
                   
        # Electromagnetic torque
        Te = psi[0]*I[1]-psi[1]*I[0]

        # Mechanical dynamics
        ddeltadt = wb*(omega - omega0)
        domegadt = (Tm + Te - F*(omega-omega0))/(2*H)

        # Conversion to network reference frame
        dIs_netdt = T.inv() * dIdt[:2] + P*I[:2]

        StateSpace = Matrix([dIs_netdt, dIdt[2:], ddeltadt, domegadt])
        
        Ports = Matrix([iSd,iSq,vSd,vSq])
        A = jacobian(StateSpace[:2], Ports)
        C = StateSpace[:2] - A * Ports

        StateSpace[0] = A11*iSd + A12*iSq + A13*vSd + A14*vSq + C1
        StateSpace[1] = A21*iSd + A22*iSq + A23*vSd + A24*vSq + C2
        InternalEquations = Matrix([A[0,0], A[0,1], A[0,2], A[0,3], A[1,0], A[1,1], A[1,2], A[1,3], C[0], C[1]])

        StateSpace = simplify(StateSpace)
        return StateSpace, InternalEquations