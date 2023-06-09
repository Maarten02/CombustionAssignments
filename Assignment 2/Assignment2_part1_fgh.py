import matplotlib.pyplot as plt
import numpy as np


"""Questions

1. How to compute density
2. fick's law, should we do D_NN
3. Le = 1 , do we use cp and lambda and density from mixture?
4. Le = 1, something wrong with dimensions? 
5. can we assume v (mean bulk velocity) is zero in the species mass flux equation?
6. We evaluate the species mass flux at t=0 because the problem is transient
"""



# Within the domain the mole fractions vary linearly. Compute and plot profiles in the domain of the
# following quantities
# a) Species mass and mole fractions, mean molar mass and density
# mean molar mass, W = sum X_k*W_k
# species mass fractions, Y_k  = X_k * W_k / W
# density, rho =
N = 101                             # number of points in the domain
L = 0.1 * 10**(-3)                  # length of domain in meters
X_points = np.linspace(0, L, N)     # [m] - the x coordinates
X_1 = np.linspace(0.4, 0, N)        # CH4
X_2 = np.linspace(0.4, 0, N)        # 02
X_3 = np.linspace(0.2, 1, N)        # N2

lambda_1 = 0.031992               # [W/m K]
lambda_2 = 0.025129                 # [W/m K]
lambda_3 = 0.020933                 # [W/m K]

W_1 = 16.04                        # [g/mol]
W_2 = 15.999*2                      # [g/mol]
W_3 = 28.0134                       # [g/mol]

Y_1 = np.empty(N)                   # CH4 Mass fraction spatial variation
Y_2 = np.empty(N)                   # O2 ''   ''       ''      ''
Y_3 = np.empty(N)                   # N2 ''   ''       ''      ''
W = np.empty(N)                     # Mean Molar Mass
rho = np.empty(N)                   # Mean Mass Density

n_1 = np.empty(N)                   # CH4 number of moles
n_2 = np.empty(N)                   # O2 number of moles
n_3 = np.empty(N)                   # N2 number of moles

m_1 = np.empty(N)                   # CH4 mass
m_2 = np.empty(N)                   # O2 mass
m_3 = np.empty(N)                   # N2 mass

m_tot = np.empty(N)                 # total
ave_lambda = np.empty(N)

D_N2O2 = 2.06 * 10 ** (-5)
D_CH4O2 = 2.23 * 10 ** (-5)

D_O2N2 = 2.06 * 10 ** (-5)
D_CH4N2 = 2.21 * 10 ** (-5)

D_O2O2 = 2.07 * 10 ** (-5)
D_N2N2 = 2.04 * 10 ** (-5)


d_n2o2_fick = np.empty(N)
d_CH4o2_fick = np.empty(N)
d_o2n2_fick = np.empty(N)
d_CH4n2_fick = np.empty(N)
d_o2o2_fick = np.empty(N)
d_n2n2_fick = np.empty(N)
D_CH4_wilke = np.empty(N)
D_o2_wilke = np.empty(N)
D_n2_wilke = np.empty(N)

X_n2_prime_CH4 = np.empty(N)
X_n2_prime_o2 = np.empty(N)
X_o2_prime_n2 = np.empty(N)
X_o2_prime_CH4 = np.empty(N)
X_CH4_prime_n2 = np.empty(N)
X_CH4_prime_o2 = np.empty(N)

cp_CH4 = 2226               # [J/kg K]
cp_n2 = 1.040 * 1000                # [J/kg K]
cp_o2 = 0.918 * 1000                # [J/kg K]

Le_CH4 = 0.97
Le_o2 = 1.11
Le_n2 = 1

D_Le_1 = np.empty(N)
D_Le_const_CH4 = np.empty(N)
D_Le_const_o2 = np.empty(N)
D_Le_const_n2 = np.empty(N)
for i in range(N):
    W[i] = X_1[i] * W_1 + X_2[i] * W_2 + X_3[i] * W_3
    Y_1[i] = X_1[i] * W_1 / W[i]
    Y_2[i] = X_2[i] * W_2 / W[i]
    Y_3[i] = X_3[i] * W_3 / W[i]
    R = 8.3144598                   # [kJ/mol K]
    T = 300                         # [K]
    p = 101325                      # [pa]
    n_tot = 1                       # [-]
    V_total = n_tot * R * T / p     # [m^3]
    # X_1,2,3 --> n_1,2,3
    n_1[i] = X_1[i] * n_tot
    n_2[i] = X_2[i] * n_tot
    n_3[i] = X_3[i] * n_tot
    # n_1,2,3, w_1,2,3, --> m_1,2,3
    m_1[i] = n_1[i] * W_1
    m_2[i] = n_2[i] * W_2
    m_3[i] = n_3[i] * W_3
    m_tot[i] = m_1[i] + m_2[i] + m_3[i]
    # n_1,2,3 --> m_total
    # rho = m_total / V
    rho[i] = m_tot[i] / 1000 / V_total  # g/m^3

    lambda_left_term = 0
    lambda_right_term = 0
    for lambda_i, X_i in zip([lambda_1, lambda_2, lambda_3], [X_1[i], X_2[i], X_3[i]]):
        lambda_left_term += X_i * lambda_i
        lambda_right_term +=X_i / lambda_i

    ave_lambda[i] = 0.5 * (lambda_left_term + 1/lambda_right_term)

    # model 1: Fick's
    # two scenario's: O2 is carrier or N2 is carrier
    # what about the point where  Y_O2 = Y_N2?
    if Y_2[i] > Y_3[i]:     # O2 is carrier
        d_n2o2_fick[i] = D_N2O2
        d_CH4o2_fick[i] = D_CH4O2
        d_o2n2_fick[i] = 0
        d_CH4n2_fick[i] = 0
        d_o2o2_fick[i] = D_O2O2
        d_n2n2_fick[i] = 0
    else:                   # N2 is carrier
        d_o2n2_fick[i] = D_O2N2
        d_CH4n2_fick[i] = D_CH4N2
        d_n2o2_fick[i] = 0
        d_CH4o2_fick[i] = 0
        d_o2o2_fick[i] = 0
        d_n2n2_fick[i] = D_N2N2

    # model 2: Wilke
    # get X'_j = X_j / (1 - X_i)
    # sum x'_j / D_ij for i =/= j
    # D_i^M = sum^-1
    # CH4 diff Wilke
    X_CH4_prime_o2[i] = X_2[i] / (1-X_1[i])
    X_CH4_prime_n2[i] = X_3[i] / (1-X_1[i])
    sum_x_CH4_prime = X_CH4_prime_o2[i] / D_CH4O2 + X_CH4_prime_n2[i] / D_CH4N2
    D_CH4_wilke[i] = 1/ sum_x_CH4_prime

    # o2 diff Wilke
    X_o2_prime_CH4[i] = X_1[i] / (1 - X_2[i])
    X_o2_prime_n2[i] = X_3[i] / (1 - X_1[i])
    sum_x_o2_prime = X_o2_prime_CH4[i] / D_CH4O2 + X_o2_prime_n2[i] / D_O2N2
    D_o2_wilke[i] = 1 / sum_x_o2_prime

    # CH4 diff Wilke
    X_n2_prime_CH4[i] = X_1[i] / (1 - X_3[i])
    X_n2_prime_o2[i] = X_2[i] / (1 - X_3[i])
    sum_x_n2_prime = X_n2_prime_CH4[i] / D_CH4N2 + X_n2_prime_o2[i] / D_O2N2
    D_n2_wilke[i] = 1 / sum_x_n2_prime

    # Le = 1
    cp_mix = Y_1[i] * cp_CH4 + Y_2[i] * cp_o2 + Y_3[i] * cp_n2
    D_Le_1[i] = ave_lambda[i] / (rho[i]*cp_mix)

    # Le = constant
    D_Le_const_CH4[i] = ave_lambda[i] / (Le_CH4 * rho[i] * cp_mix)
    D_Le_const_o2[i] = ave_lambda[i] / (Le_o2 * rho[i] * cp_mix)
    D_Le_const_n2[i] = ave_lambda[i] / (Le_n2 * rho[i] * cp_mix)

    if i == 50:
        print('ave lambda', ave_lambda[i])
        print(f'cp mix = {cp_mix}')

X_points *= 1000 # [m] -> [mm]
#plots
#species mass plot
fig, ax = plt.subplots()
ax.plot(X_points, Y_1, label='CH4')
ax.plot(X_points, Y_2, label='O2')
ax.plot(X_points, Y_3, label='N2')
ax.set_xlabel('x [mm]')
ax.set_ylabel('Y [-]')
ax.set_title('Species Mass Fraction over Length of Domain')
ax.grid()
ax.legend()
plt.savefig('figures/ch4/species_mass_fractions_ch4.pdf', bbox_inches='tight', pad_inches=0.2)

#species mole fractions
fig, ax = plt.subplots()
ax.plot(X_points, X_1, label='CH4')
ax.plot(X_points, X_2, label='O2', linestyle='dotted')
ax.plot(X_points, X_3, label='N2')
ax.set_xlabel('x [mm]')
ax.set_ylabel('X [-]')
ax.set_title('Species Mole Fraction Over Length Of Domain. ')
ax.grid()
ax.legend()
plt.savefig('figures/ch4/species_mole_fractions_ch4.pdf', bbox_inches='tight', pad_inches=0.2)


# mean molar mass
fig, ax = plt.subplots()
ax.plot(X_points, W)
ax.set_xlabel('x [mm]')
ax.set_ylabel('W [g/mol]')
ax.set_title('Mean Molar Mass Over Length Of Domain. ')
ax.grid()
plt.savefig('figures/ch4/mean_molar_mass_ch4.pdf', bbox_inches='tight', pad_inches=0.2)

#density
fig, ax = plt.subplots()
ax.plot(X_points, rho)
ax.set_xlabel('x [mm]')
ax.set_ylabel(r'$\rho$ [g/m3]')
ax.set_title('Mean Density Over Length Of Domain. ')
ax.grid()
plt.savefig('figures/ch4/mean_density_ch4.pdf', bbox_inches='tight', pad_inches=0.2)

# b) Thermal conductivity of the mixture (see appendix)
fig, ax = plt.subplots()
ax.plot(X_points, ave_lambda)
ax.set_xlabel('x [mm]')
ax.set_ylabel(r'$\lambda$ [W/(m K)]')
ax.set_title('Mean Lambda Over Length Of Domain. ')
ax.grid()
plt.savefig('figures/ch4/mean_lambda_ch4.pdf', bbox_inches='tight', pad_inches=0.2)




# c) Species diffusion coefficients predicted by the four models
## Model 1: Fick's
fig, ax = plt.subplots()
ax.plot(X_points[d_CH4n2_fick>0], d_CH4n2_fick[d_CH4n2_fick>0], label=r'$D_{CH_4N_2}$')
ax.plot(X_points[d_CH4o2_fick>0], d_CH4o2_fick[d_CH4o2_fick>0], label=r'$D_{CH_4O_2}$')
ax.plot(X_points[d_n2n2_fick>0], d_n2n2_fick[d_n2n2_fick>0], label=r'$D_{N_2N_2}$')
ax.plot(X_points[d_o2n2_fick>0], d_o2n2_fick[d_o2n2_fick>0], label=r'$D_{O_2N_2}$', linestyle='dotted')
ax.plot(X_points[d_o2o2_fick>0], d_o2o2_fick[d_o2o2_fick>0], label=r'$D_{O_2O_2}$')
ax.plot(X_points[d_n2o2_fick>0], d_n2o2_fick[d_n2o2_fick>0], label=r'$D_{N_2O_2}$', linestyle='dotted')
ax.set_xlabel('x [mm]')
ax.set_ylabel(r'$D_{ij}$ [m2/s]')
ax.set_title('Fick\'s Diffusion Coefficiencts\n Over Length Of Domain.')
ax.grid()
ax.legend()
plt.savefig('figures/fick_diff_coef_ch4.pdf', bbox_inches='tight', pad_inches=0.2)


## Model 2: Wilke
fig, ax = plt.subplots()
ax.plot(X_points, D_CH4_wilke, label=r'$D_{wilke,CH_4}$')
ax.plot(X_points, D_o2_wilke, label=r'$D_{wilke,O_2}$')
ax.plot(X_points, D_n2_wilke, label=r'$D_{wilke,N_2}$')
ax.set_xlabel('x [mm]')
ax.set_ylabel(r'$D_{wilke,i}$ [m2/s]')
ax.set_title('Wilke Diffusion Coefficients Over Length Of Domain. ')
ax.grid()
ax.legend()
plt.savefig('figures/wilke_diff_coef_ch4.pdf', bbox_inches='tight', pad_inches=0.2)



## Model 3: Le=1
fig, ax = plt.subplots()
ax.plot(X_points, D_Le_1)
ax.set_xlabel('x [mm]')
ax.set_ylabel(r'$D_{Le=1}$ [m2/s]')
ax.set_title('Le = 1 Diffusion Coefficient Over Length Of Domain. ')
ax.grid()
plt.savefig('figures/Le_1_diff_coef_ch4.pdf', bbox_inches='tight', pad_inches=0.2)

## Model 4: Le=const
fig, ax = plt.subplots()
ax.plot(X_points, D_Le_const_CH4, label=r'$D_{Le=const,CH_4}$')
ax.plot(X_points, D_Le_const_o2, label=r'$D_{Le=const,O_2}$')
ax.plot(X_points, D_Le_const_n2, label=r'$D_{Le=const,N_2}$')
ax.set_xlabel('x [mm]')
ax.set_ylabel(r'$D_{Le=const,i}$ [m2/s]')
ax.set_title('Le=const Diffusion Coefficients Over Length Of Domain. ')
ax.grid()
ax.legend()
plt.savefig('figures/Le_const_diff_coef_ch4.pdf', bbox_inches='tight', pad_inches=0.2)




# d) Continue with the first and fourth of the models introduced above. Compute the species mass fluxes
# predicted by these two models at 𝑥 = 0.5𝐿 (the midpoint). Comment on the differences [3 pts];
X_points /= 1000
# 1) retrieve Di at x = 0.5
# 2) retrieve rho at x = 0.5
# 3) gradient of Yi of not abundant species
### 3a) use the midpoint rule to approximate gradient of diffusive mass flux
# 4) calculate abundant species by using sum Yi Vi

# FICK CH4 species mass flux
# find dY/dx @ x=0.5 +- h using midpoint rule
# find Di @ x=0.5 +- h to determine for the diffusive mass flux gradient
# find rho @ x=0.5 +- h

def get_sp_m_flux_grad_non_ab(rho_arr, D_arr, Y_arr):
    mid_index = int((N-1)/2)
    dx = L/(N-1)
    dY_dx = (Y_arr[mid_index+1] - Y_arr[mid_index-1])/(2*dx)
    dY_dx_plus_1 = (Y_arr[mid_index+2] - Y_arr[mid_index])/(2*dx)
    dY_dx_min_1 = (Y_arr[mid_index] - Y_arr[mid_index-2])/(2*dx)
    # d2Y_dx2 = (dY_dx_plus_1 - dY_dx_min_1)/(2*dx)

    # get the mass flux grad
    J_x_min_h = rho_arr[mid_index-1] * D_arr[mid_index-1] * dY_dx_min_1
    J = rho_arr[mid_index] * D_arr[mid_index] * dY_dx * -1
    J_x_plus_h = rho_arr[mid_index+1] * D_arr[mid_index+1] * dY_dx_plus_1
    dJdx = (J_x_plus_h - J_x_min_h) / (2*dx)


    return -1*dJdx, J, J_x_min_h, J_x_plus_h

dx = L / (N-1)

d_rho_dt_fick_CH4, J_CH4, J_CH4_min_1, J_CH4_plus_1 = get_sp_m_flux_grad_non_ab(rho, d_CH4n2_fick, Y_1)
d_rho_dt_fick_o2, J_o2, J_o2_min_1, J_o2_plus_1 = get_sp_m_flux_grad_non_ab(rho, d_o2n2_fick, Y_2)

# use sum of YV=0
rhoYV_n2 = 0 - (J_CH4+J_o2)
rhoYV_n2_plus_1 = 0 - (J_CH4_plus_1+J_o2_plus_1)
rhoYV_n2_min_1 = 0 - (J_CH4_min_1+J_o2_min_1)
grad_J_n2 = -1 * (rhoYV_n2_plus_1 - rhoYV_n2_min_1)/(2*dx)

print(f'CH4 mass flux (fick) = {J_CH4:.4f} kg/s m^2')
print(f'O2 mass flux (fick) = {J_o2:.4f} kg/s m^2')
print(f'N2 mass flux (fick) = {rhoYV_n2:.4f} kg/s m^2')
# Wilke
dx = L / (N-1)

d_rho_dt_wilke_CH4, J_CH4_wilke, J_CH4_min_1_wilke, J_CH4_plus_1_wilke = get_sp_m_flux_grad_non_ab(rho, D_CH4_wilke, Y_1)
d_rho_dt_wilke_o2, J_o2_wilke, J_o2_min_1_wilke, J_o2_plus_1_wilke = get_sp_m_flux_grad_non_ab(rho, D_o2_wilke, Y_2)

# use sum of YV=0
rhoYV_n2_wilke = 0 - (J_CH4_wilke+J_o2_wilke)
rhoYV_n2_plus_1_wilke = 0 - (J_CH4_plus_1_wilke+J_o2_plus_1_wilke)
rhoYV_n2_min_1_wilke = 0 - (J_CH4_min_1_wilke+J_o2_min_1_wilke)
grad_J_n2 = -1 * (rhoYV_n2_plus_1_wilke - rhoYV_n2_min_1_wilke)/(2*dx)

print(f'CH4 mass flux (wilke) = {J_CH4_wilke:.4f} kg/s m^2')
print(f'O2 mass flux (wilke) = {J_o2_wilke:.4f} kg/s m^2')
print(f'N2 mass flux (wilke) = {rhoYV_n2_wilke:.4f} kg/s m^2')

# Le = 1
dx = L / (N-1)

d_rho_dt_Le1_CH4, J_CH4_Le1, J_CH4_min_1_Le1, J_CH4_plus_1_Le1 = get_sp_m_flux_grad_non_ab(rho, D_Le_1, Y_1)
d_rho_dt_Le1_o2, J_o2_Le1, J_o2_min_1_Le1, J_o2_plus_1_Le1 = get_sp_m_flux_grad_non_ab(rho, D_Le_1, Y_2)

# use sum of YV=0
rhoYV_n2_Le1 = 0 - (J_CH4_Le1+J_o2_Le1)
rhoYV_n2_plus_1_Le1 = 0 - (J_CH4_plus_1_Le1+J_o2_plus_1_Le1)
rhoYV_n2_min_1_Le1 = 0 - (J_CH4_min_1_Le1+J_o2_min_1_Le1)
grad_J_n2_Le1 = -1 * (rhoYV_n2_plus_1_Le1 - rhoYV_n2_min_1_Le1)/(2*dx)

print(f'CH4 mass flux (Le=1) = {J_CH4_Le1:.4f} kg/s m^2')
print(f'O2 mass flux (Le=1) = {J_o2_Le1:.4f} kg/s m^2')
print(f'N2 mass flux (Le=1) = {rhoYV_n2_Le1:.4f} kg/s m^2')

# Le = const CH4 mass flux
dx = L / (N-1)

d_rho_dt_Lec_CH4, J_CH4, J_CH4_min_1, J_CH4_plus_1 = get_sp_m_flux_grad_non_ab(rho, D_Le_const_CH4, Y_1)
d_rho_dt_Lec_o2, J_o2, J_o2_min_1, J_o2_plus_1 = get_sp_m_flux_grad_non_ab(rho, D_Le_const_o2, Y_2)

# use sum of YV=0
rhoYV_n2 = 0 - (J_CH4+J_o2)
rhoYV_n2_plus_1 = 0 - (J_CH4_plus_1+J_o2_plus_1)
rhoYV_n2_min_1 = 0 - (J_CH4_min_1+J_o2_min_1)
grad_J_n2 = -1 * (rhoYV_n2_plus_1 - rhoYV_n2_min_1)/(2*dx)

print(f'CH4 mass flux (Le=const) = {J_CH4:.4f} kg/s m^2')
print(f'O2 mass flux (Le=const) = {J_o2:.4f} kg/s m^2')
print(f'N2 mass flux (Le=const) = {rhoYV_n2:.4f} kg/s m^2')


# e) Explain how difference in hydrogen diffusive flux could have an impact on flame speed [5 pts].1

# Now consider the case with methane instead of hydrogen. The spatial profiles of the species molar
# fractions are identical to the previous case, but species 1 is now CH4. Compute and plot profiles in the
# domain of the following quantities:
# f) Species diffusion coefficients predicted by models 2) 3) and 4) [3 pts];
# g) Species mass fluxes predicted by the three models at the midpoint 𝑥 = 0.5𝐿 [3 pts];
# h) Describe and comment differences and similarities between the obtained results and the hydrogen
# case