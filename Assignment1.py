from JANNAF.get_cp import get_cp
from JANNAF.get_jannaf import get_jannaf
from JANNAF.get_cp_mix import get_cp_mix
from JANNAF.get_LHS_ethylene import get_LHS_ethylene
from JANNAF.get_RHS import get_RHS
import numpy as np
import matplotlib.pyplot as plt

#======== PART 1 | ITEM 1 ========
# Calculate and plot the variation of 𝐶!
# for H 2, O 2, N 2, CO 2 and H 2O from 600 to 2500
# Calculate the same also for ethylene (C2H 4)

compounds, coefs1, coefs2 = get_jannaf()
fig, ax = plt.subplots()
N_points = 100
#                  W_H2,  W_O2,   W_N2,  W_CO2, W_H2O, W_C2H4
w_list = np.array([2.016, 31.999, 28.01, 44.01, 78.01, 28.05])
R = 8.314 #/mol
R_bar = R / w_list  #/g

for i, (compound, coef1, coef2) in enumerate(zip(compounds, coefs1, coefs2)):
    cp_list = np.empty(N_points)
    temp_list = np.empty(N_points)
    for j, temp in enumerate(np.linspace(600, 2500, N_points)):
        cp_list[j] = get_cp(coef1, coef2, temp)
        temp_list[j] = temp

    cp_list *= R_bar[i]
    ax.plot(temp_list, cp_list, label=compound)

plt.legend()
plt.grid()
ax.set_xlabel('Temperature [K]')
ax.set_ylabel('$C_p$ [x]')
ax.set_title('$C_p$ variation with temperature for different compounds')
#plt.savefig('figures/cp_compounds.pdf')
plt.show()

#======== PART 1 | ITEM 2 ========
# Calculate and plot (in the same figure) the variation of 𝐶!,#$% for reactants and combustion
# products from 300 to 2400K, assuming the reactants to be air and ethylene at equivalence ratios
# 0.4, 0.6, 0.8, 1.0, 1.2, 1.4, 1.6. Assume complete combustion

# Compute combustion products from equivalence ratio
phi_arr = np.linspace(0.4, 1.6, 7)
cp_reac_arr = np.empty((len(phi_arr), N_points))
cp_prod_arr = np.empty((len(phi_arr), N_points))
temp_arr = np.empty(N_points)

for i, phi in enumerate(phi_arr):
    for j, temp in enumerate(np.linspace(600, 2500, N_points)):
        cp_reac, cp_prod = get_cp_mix(phi, temp)
        cp_reac_arr[i,j] = cp_reac
        cp_prod_arr[i,j] = cp_prod


fig, ax = plt.subplots()
for i in range(len(phi_arr)):
    lbl_r = "Reactants, $\phi$ = {:.1f}".format(phi_arr[i])
    lbl_p = "Products, $\phi$ = {:.1f}".format(phi_arr[i])
    ax.plot(temp_arr, cp_reac_arr[i], label=lbl_r)
    ax.plot(temp_arr, cp_prod_arr[i], label=lbl_p)

plt.legend()
plt.show()


#======== PART 1 | ITEM 3 ========
# Compute and plot the flame adiabatic temperature for complete combustion of H 2/air and
# reactant temperature at 1100K for the same equivalence ratios. Compare this with the adiabatic
# flame temperature in the case of ethylene/air combustion.

# determine summation of Y and delta_h0 = LHS
LHS = get_LHS_ethylene(phi)

# make guess for AFT
aft_0 = 999
aft_1 = 9999
AFT_list = [aft_0, aft_1]
RHS_list = [get_RHS(aft_0), aft_RHS(aft_1)]

if RHS_list[0] > LHS:
    raise Exception("Left point invalid")
if RHS_list[1] < LHS:
    raise Exception("Right point invalid")

running = True
it = 0
tol = 1e-3
while running:
    next_aft = (AFT_list[-2] + AFT_list[-1]) * 0.5
    msg = "Starting iteration {:02} with next AFT of {:04} [K]".format(it, next_aft)
    print(msg)
    next_RHS = get_RHS(next_aft)

    if abs(next_RHS - LHS) < tol:
        running = False
        print("Bisection converged to AFT = {:.2f} [K]".format(next_RHS))

    elif next_RHS > LHS:
        next_left_aft = next_RHS
        next_right_aft = RHS_list[-1]
        RHS_list.extend([next_left_aft, next_right_aft])
        it += 1

    else:
        next_left_aft = RHS_list[-2]
        next_right_aft = next_RHS
        RHS_list.extend([next_left_aft, next_right_aft])
        it += 1






