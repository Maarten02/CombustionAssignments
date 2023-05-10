# Ethylene imports
from JANNAF_C2H4.get_cp import get_cp as get_cp_ethylene
from JANNAF_C2H4.get_jannaf import get_jannaf as get_jannaf_ethylene
from JANNAF_C2H4.get_cp_mix import get_cp_mix as get_cp_mix_ethylene
from JANNAF_C2H4.get_LHS_ethylene import get_LHS_ethylene
from JANNAF_C2H4.get_RHS import get_RHS as get_RHS_ethylene

# H2 imports
from JANNAF_H2.get_cp import get_cp as get_cp_h2
from JANNAF_H2.get_jannaf import get_jannaf as get_jannaf_h2
from JANNAF_H2.get_cp_mix import get_cp_mix as get_cp_mix_h2
from JANNAF_H2.get_LHS_H2 import get_LHS_h2
from JANNAF_H2.get_RHS import get_RHS as get_RHS_h2

# other imports
import numpy as np
import matplotlib.pyplot as plt

#======== PART 1 | ITEM 1 ========
# Calculate and plot the variation of 𝐶!
# for H 2, O 2, N 2, CO 2 and H 2O from 600 to 2500
# Calculate the same also for ethylene (C2H 4)

compounds, coefs1, coefs2 = get_jannaf_ethylene()
fig, ax = plt.subplots()
N_points = 100
#                  W_H2,  W_O2,   W_N2,  W_CO2, W_H2O, W_C2H4
w_list = np.array([2.016, 31.999, 28.01, 44.01, 18.01528, 28.05])
R = 8.314 #/mol
R_bar = R / w_list  #/g

for i, (compound, coef1, coef2) in enumerate(zip(compounds, coefs1, coefs2)):
    cp_list = np.empty(N_points)
    temp_list = np.empty(N_points)
    for j, temp in enumerate(np.linspace(600, 2500, N_points)):
        cp_list[j] = get_cp_ethylene(coef1, coef2, temp)
        temp_list[j] = temp

    cp_list *= R_bar[i]
    ax.plot(temp_list, cp_list, label=compound)

plt.legend()
plt.grid()
ax.set_xlabel('Temperature [K]')
ax.set_ylabel('$C_p$ [x]')
ax.set_title('$C_p$ variation with temperature for different compounds')
#plt.savefig('figures/cp_compounds.pdf')
plt.savefig('figures/cp_comp.png')

#======== PART 1 | ITEM 2 ========
# Calculate and plot (in the same figure) the variation of 𝐶!,#$% for reactants and combustion
# products from 600 to 2400K, assuming the reactants to be air and ethylene at equivalence ratios
# 0.4, 0.6, 0.8, 1.0, 1.2, 1.4, 1.6. Assume complete combustion

# Compute combustion products from equivalence ratio
phi_arr = np.linspace(0.4, 1.6, 7)
cp_reac_arr = np.empty((len(phi_arr), N_points))
cp_prod_arr = np.empty((len(phi_arr), N_points))
temp_arr = np.empty(N_points)

for i, phi in enumerate(phi_arr):
    for j, temp in enumerate(np.linspace(600, 2400, N_points)):
        cp_reac, cp_prod = get_cp_mix_ethylene(phi, temp)
        cp_reac_arr[i,j] = cp_reac
        cp_prod_arr[i,j] = cp_prod


fig, ax = plt.subplots()
for i in range(len(phi_arr)):
    lbl_r = "Reactants, $\phi$ = {:.1f}".format(phi_arr[i])
    lbl_p = "Products, $\phi$ = {:.1f}".format(phi_arr[i])
    ax.plot(temp_arr, cp_reac_arr[i], label=lbl_r)
    ax.plot(temp_arr, cp_prod_arr[i], label=lbl_p)

plt.legend()
plt.savefig('figures/cp_mix.png')


#======== PART 1 | ITEM 3 ========
# Compute and plot the flame adiabatic temperature for complete combustion of H 2/air and
# reactant temperature at 1100K for the same equivalence ratios. Compare this with the adiabatic
# flame temperature in the case of ethylene/air combustion.
c2h4_aft_list = []
h2_aft_list = []
tol = 1e-1

phi_arr = np.linspace(0.4, 1.6, 7)
for phi in phi_arr:

    # LHS for ethylene
    LHS = get_LHS_ethylene(phi)

    # make guess for AFT
    aft_0 = 1000
    aft_1 = 3499
    AFT_list = [aft_0, aft_1]
    RHS_list = [get_RHS_ethylene(phi, aft_0), get_RHS_ethylene(phi, aft_1)]

    if RHS_list[0] > LHS:
        raise Exception("Left point invalid")
    if RHS_list[1] < LHS:
        raise Exception("Right point invalid")

    # Ethylene AFT
    running = True
    it = 0

    while running:
        #print(AFT_list)
        next_aft = (AFT_list[-2] + AFT_list[-1]) * 0.5
        #msg = "[C2H4] Starting iteration {:02} for phi = {:.1f} with next AFT of {:04.3f} [K]".format(it, phi, next_aft)
        #print(msg)
        next_RHS = get_RHS_ethylene(phi, next_aft)

        if abs(next_RHS - LHS) < tol:
            running = False
            print("[C2H4] Bisection converged for phi = {:.1f} to AFT = {:.3f} [K]".format(phi, next_aft))
            c2h4_aft_list.append(next_aft)

        elif next_RHS > LHS:
            next_left_aft = AFT_list[-2]
            next_right_aft = next_aft
            AFT_list.extend([next_left_aft, next_right_aft])
            #print('extended list')
            it += 1

        else:
            next_left_aft = next_aft
            next_right_aft = AFT_list[-1]
            AFT_list.extend([next_left_aft, next_right_aft])
            #print('extended list')
            it += 1



    #=============== H2 AFT =======================


    # LHS for h2
    LHS = get_LHS_h2(phi)

    # make guess for AFT
    aft_0 = 1000
    aft_1 = 3499
    AFT_list = [aft_0, aft_1]
    RHS_list = [get_RHS_h2(phi, aft_0), get_RHS_h2(phi, aft_1)]

    if RHS_list[0] > LHS:
        raise Exception("Left point invalid")
    if RHS_list[1] < LHS:
        raise Exception("Right point invalid")

    # H2 AFT
    running = True
    it = 0

    while running:
        #print(AFT_list)
        next_aft = (AFT_list[-2] + AFT_list[-1]) * 0.5
        #msg = "[H2] Starting iteration {:02} for phi = {:.1f} with next AFT of {:04.3f} [K]".format(it, phi, next_aft)
        #print(msg)
        next_RHS = get_RHS_h2(phi, next_aft)

        if abs(next_RHS - LHS) < tol:
            running = False
            print("[H2] Bisection converged for phi = {:.1f} to AFT = {:.3f} [K]".format(phi, next_aft))
            h2_aft_list.append(next_aft)

        elif next_RHS > LHS:
            next_left_aft = AFT_list[-2]
            next_right_aft = next_aft
            AFT_list.extend([next_left_aft, next_right_aft])
            #print('extended list')
            it += 1

        else:
            next_left_aft = next_aft
            next_right_aft = AFT_list[-1]
            AFT_list.extend([next_left_aft, next_right_aft])
            #print('extended list')
            it += 1

fig, ax = plt.subplots()
ax.plot(phi_arr, np.array(c2h4_aft_list), label='C2H4')
ax.plot(phi_arr, np.array(h2_aft_list), label='H2')
ax.set_title('Variation of AFT with $\phi$')
ax.set_xlabel('$\phi$ [-]')
ax.set_ylabel('AFT [K]')
plt.legend()
plt.grid()
plt.savefig('figures/phiAFT.png')





