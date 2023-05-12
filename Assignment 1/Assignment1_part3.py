# Imports
import numpy as np
import matplotlib.pyplot as plt
#-------------------
#       PLAN
#-------------------

#retrieve adiabatic flame temperature from CAE
#Compute (RHS) e^-(delG/(R0*T))
    # delG = delH^R - T delS
    # Get delH from reaction formation
    # get delS from engineeringtoolbox or something
#LHS: p_no^2 / (p_n2 * p_o2)
#--> n_no^2 / (n_n2*n_o2)
# compute n_no as we know n_n2 and n_o2 from complete combustion equation
# compute n_tot (products from combustion)
# now we have X_no  (n_no/n_tot)
phi_list_1bar = [4.0000E-01, 6.0000E-01, 8.0000E-01, 9.9000E-01]
aft_list_1bar = [1.6238E+03, 2.0283E+03, 2.3317E+03, 2.4829E+03]
NO_list_1bar = [1.5971E-03, 4.8941E-03, 6.8783E-03, 5.4125E-03]

phi_list_10bar = [4.0000E-01, 6.0000E-01, 8.0000E-01, 9.9000E-01]
aft_list_10bar = [1.6241E+03, 2.0351E+03, 2.3773E+03, 2.5795E+03]
NO_list_10bar = [1.5995E-03, 4.9858E-03, 7.3735E-03, 5.2720E-03]

def Gibbz(T):
    R0 = 8.31446261815324       # [J/mol K]
    deltaG0 = get_deltaG0(T)    # [J/mol]
    print('deltaG0', deltaG0)
    Kp = np.exp(-1*deltaG0/(R0*T))
    return Kp




def get_deltaG0(T):
    deltaH = get_deltaH()
    deltaS = get_deltaS()
    deltaG0 = deltaH - T * deltaS
    return deltaG0

def get_deltaH():
    H_f_NO = 90.29       # [kJ/mol] !
    return 2*H_f_NO*10**3   # [J /mol]

def get_deltaS():
    S0_NO = 210.66          # [J /mol K]
    S0_O2 = 205.04          # [J /mol K]
    S0_N2 =191.5
    return 2*S0_NO - S0_N2 - S0_O2



X_NO_list_1bar = []

for t, phi in zip(aft_list_1bar, phi_list_1bar):
    print('=========================')
    #n_O2_prod = (1 / phi - 1) * 3
    #n_N2_prod = 3 / phi * 3.76
    n_H2O_prod = 2
    n_CO2_prod = 2
    Kp = Gibbz(t)
    print('Kp', Kp)
    #n_NO = np.sqrt(Kp * n_O2_prod * n_N2_prod)
    A = 4 - Kp
    B = (-3 - 8.28/phi )*Kp
    C = (-33.84/phi**2 + 33.84/phi)*Kp
    D = np.sqrt(B**2 - 4*A*C)
    z1 = (-B + D)/(2*A)
    n_tot = 2 + 2 + 3*(1/phi - 1) - z1 + 3/phi * 3.76 - z1 + 2*z1
    n_NO = 2 * z1
    print('nNO', n_NO)
    print('nTOT', n_tot)
    X_NO_list_1bar.append(n_NO / n_tot)

fig, ax = plt.subplots()
ax.plot(phi_list_1bar, X_NO_list_1bar, label='NO Equilibrium')
ax.plot(phi_list_1bar, NO_list_1bar, label='CEA')
ax.set_xlabel('$\phi$ [-]')
ax.set_ylabel('$X_{NO}$ [-]')
ax.set_title('Variation of NO concentration with equivalence ratio at 1 Bar')
ax.legend()
ax.grid()
plt.savefig('./Bin/figures/NO_1bar.pdf')

X_NO_list_10bar = []
for t, phi in zip(aft_list_10bar, phi_list_10bar):
    print('=========================')
    #n_O2_prod = (1 / phi - 1) * 3
    #n_N2_prod = 3 / phi * 3.76
    n_H2O_prod = 2
    n_CO2_prod = 2
    Kp = Gibbz(t)
    print('Kp', Kp)
    #n_NO = np.sqrt(Kp * n_O2_prod * n_N2_prod)
    A = 4 - Kp
    B = (-3 - 8.28 / phi) * Kp
    C = (-33.84 / phi ** 2 + 33.84 / phi) * Kp
    D = np.sqrt(B ** 2 - 4 * A * C)
    z1 = (-B + D) / (2 * A)
    n_tot = 2 + 2 + 3*(1/phi -1 ) - z1 + 3/phi * 3.76 -z1 + 2*z1
    n_NO = 2*z1
    print('nNO', n_NO)
    print('nTOT', n_tot)
    X_NO_list_10bar.append(n_NO / n_tot)

fig, ax = plt.subplots()
ax.plot(phi_list_10bar, X_NO_list_10bar, label='NO Equilibrium')
ax.plot(phi_list_10bar, NO_list_10bar, label='CEA')
ax.set_xlabel('$\phi$ [-]')
ax.set_ylabel('$X_{NO}$ [-]')
ax.set_title('Variation of NO concentration with equivalence ratio at 10 Bar')
ax.legend()
ax.grid()
plt.savefig('./Bin/figures/NO_10bar.pdf')