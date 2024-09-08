import sympy, os
import matplotlib.pyplot as plt

from pycamps.modules import long_line, rl_load, type4_1
from pycamps.simulation import power_system, dynamics
from pycamps.logger import configure_logging

# Specify name of power system (for saving files)
system_name = "Type4_1_LL_RLLoad"

# Configure logging
os.environ['LOG_LEVEL'] = 'INFO'
logger = configure_logging(log_file=f'{system_name}.log', log_to_console=True, log_to_file=True)

# Reference frame angle and speed
phi, dphidt = sympy.symbols('phi dphidt', real=True)
# Define base speed
wb = 377

SM1IndexName = '_G1'
SM1 = type4_1.Type4_1(SM1IndexName, phi, dphidt, wb)
TL1IndexName = '_TL_1_21'
TL1 = long_line.LongLine(TL1IndexName, phi, dphidt, wb)
Load1IndexName = '_L1'
L1 = rl_load.RLLoad(Load1IndexName,phi,dphidt,wb)

Modules = [SM1, TL1, L1]
Bus1 = [[SM1], [TL1,'L']]
Bus2 = [[L1], [TL1,'R']]
Buses = [Bus1, Bus2]
PS = power_system.PowerSystem(system_name, Modules, Buses)

# 1: Writes state space equations and vector x
StateSpace = PS.StateSpaceObject
StateSpace.write_equations()
StateSpace.write_vector_x()

# 2. Solve for system equilibrium
Simulator = dynamics.Dynamics(PS, params_directory='params')
xf = Simulator.solve_equilibrium(method='hybr')

# 3. Perform linearized analysis
Simulator.linearized_analysis(xf=xf)

# 4. Simulate system trajectory
time, states = Simulator.simulate_trajectory(xf=xf, simulation_time=0.1, method='LSODA')

# 5. Plot the results
plt.figure()
for variable_name, array in states.items():
    plt.plot(time, array, label=variable_name)

plt.legend()
plt.show()

