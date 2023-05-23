import matplotlib.pyplot as plt
import numpy as np


"""Questions

1. How to compute density
2. fick's law, should we do D_NN
3. Le = 1 , do we use cp and lambda and density from mixture?
4. Le = 1, something wrong with dimensions? """



# Within the domain the mole fractions vary linearly. Compute and plot profiles in the domain of the
# following quantities
# a) Species mass and mole fractions, mean molar mass and density
# mean molar mass, W = sum X_k*W_k
# species mass fractions, Y_k  = X_k * W_k / W
# density, rho =
N = 101                             # number of points in the domain
L = 0.1 * 10**(-3)                  # length of domain in meters
X_points = np.linspace(0, L, N)     # [m] - the x coordinates
X_1 = np.linspace(0.4, 0, N)        # H2
X_2 = np.linspace(0.4, 0, N)        # 02
X_3 = np.linspace(0.2, 1, N)        # N2

lambda_1 = 0.17422                  # [W/m K]
lambda_2 = 0.025129                 # [W/m K]
lambda_3 = 0.020933                 # [W/m K]

W_1 = 2.016                         # [g/mol]
W_2 = 15.999*2                      # [g/mol]
W_3 = 28.0134                       # [g/mol]

Y_1 = np.empty(N)                   # H2 Mass fraction spatial variation
Y_2 = np.empty(N)                   # O2 ''   ''       ''      ''
Y_3 = np.empty(N)                   # N2 ''   ''       ''      ''
W = np.empty(N)                     # Mean Molar Mass
rho = np.empty(N)                   # Mean Mass Density

n_1 = np.empty(N)                   # H2 number of moles
n_2 = np.empty(N)                   # O2 number of moles
n_3 = np.empty(N)                   # N2 number of moles

m_1 = np.empty(N)                   # H2 mass
m_2 = np.empty(N)                   # O2 mass
m_3 = np.empty(N)                   # N2 mass

m_tot = np.empty(N)                 # total
ave_lambda = np.empty(N)

D_N2O2 = 2.06 * 10 ** (-5)
D_H2O2 = 7.88 * 10 ** (-5)

D_O2N2 = 2.06 * 10 ** (-5)
D_H2N2 = 7.47 * 10 ** (-5)

D_O2O2 = 2.07 * 10 ** (-5)
D_N2N2 = 2.04 * 10 ** (-5)


d_n2o2_fick = np.empty(N)
d_h2o2_fick = np.empty(N)
d_o2n2_fick = np.empty(N)
d_h2n2_fick = np.empty(N)
d_o2o2_fick = np.empty(N)
d_n2n2_fick = np.empty(N)
D_h2_wilke = np.empty(N)
D_o2_wilke = np.empty(N)
D_n2_wilke = np.empty(N)

X_n2_prime_h2 = np.empty(N)
X_n2_prime_o2 = np.empty(N)
X_o2_prime_n2 = np.empty(N)
X_o2_prime_h2 = np.empty(N)
X_h2_prime_n2 = np.empty(N)
X_h2_prime_o2 = np.empty(N)

cp_h2 = 14.31 * 1000                # [J/kg K]
cp_n2 = 1.040 * 1000                # [J/kg K]
cp_o2 = 0.918 * 1000                # [J/kg K]

Le_h2 = 0.3
Le_o2 = 1.11
Le_n2 = 1

D_Le_1 = np.empty(N)
D_Le_const_h2 = np.empty(N)
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
    rho[i] = m_tot[i]/ V_total

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
        d_h2o2_fick[i] = D_H2O2
        d_o2n2_fick[i] = 0
        d_h2n2_fick[i] = 0
        d_o2o2_fick[i] = D_O2O2
        d_n2n2_fick[i] = 0
    else:                   # N2 is carrier
        d_o2n2_fick[i] = D_O2N2
        d_h2n2_fick[i] = D_H2N2
        d_n2o2_fick[i] = 0
        d_h2o2_fick[i] = 0
        d_o2o2_fick[i] = 0
        d_n2n2_fick[i] = D_N2N2

    # model 2: Wilke
    # get X'_j = X_j / (1 - X_i)
    # sum x'_j / D_ij for i =/= j
    # D_i^M = sum^-1
    # h2 diff Wilke
    X_h2_prime_o2[i] = X_2[i] / (1-X_1[i])
    X_h2_prime_n2[i] = X_3[i] / (1-X_1[i])
    sum_x_h2_prime = X_h2_prime_o2[i] / D_H2O2 + X_h2_prime_n2[i] / D_H2N2
    D_h2_wilke[i] = 1/ sum_x_h2_prime

    # o2 diff Wilke
    X_o2_prime_h2[i] = X_1[i] / (1 - X_2[i])
    X_o2_prime_n2[i] = X_3[i] / (1 - X_1[i])
    sum_x_o2_prime = X_o2_prime_h2[i] / D_H2O2 + X_o2_prime_n2[i] / D_O2N2
    D_o2_wilke[i] = 1 / sum_x_o2_prime

    # h2 diff Wilke
    X_n2_prime_h2[i] = X_1[i] / (1 - X_3[i])
    X_n2_prime_o2[i] = X_2[i] / (1 - X_3[i])
    sum_x_n2_prime = X_n2_prime_h2[i] / D_H2N2 + X_n2_prime_o2[i] / D_O2N2
    D_n2_wilke[i] = 1 / sum_x_n2_prime

    # Le = 1
    cp_mix = Y_1[i] * cp_h2 + Y_2[i] * cp_o2 + Y_3[i] * cp_n2
    D_Le_1[i] = ave_lambda[i] / (rho[i]*cp_mix)

    # Le = constant
    D_Le_const_h2[i] = ave_lambda[i] / (Le_h2 * rho[i] * cp_mix)
    D_Le_const_o2[i] = ave_lambda[i] / (Le_o2 * rho[i] * cp_mix)
    D_Le_const_n2[i] = ave_lambda[i] / (Le_n2 * rho[i] * cp_mix)

X_points *= 1000 # [m] -> [mm]
#plots
#species mass plot
fig, ax = plt.subplots()
ax.plot(X_points, Y_1, label='H2')
ax.plot(X_points, Y_2, label='O2')
ax.plot(X_points, Y_3, label='N2')
ax.set_xlabel('x [mm]')
ax.set_ylabel('Y [-]')
ax.set_title('Species Mass Fraction over Length of Domain')
ax.grid()
ax.legend()
plt.savefig('figures/species_mass_fractions.pdf')

#species mole fractions
fig, ax = plt.subplots()
ax.plot(X_points, X_1, label='H2')
ax.plot(X_points, X_2, label='O2', linestyle='dotted')
ax.plot(X_points, X_3, label='N2')
ax.set_xlabel('x [mm]')
ax.set_ylabel('X [-]')
ax.set_title('Species Mole Fraction Over Length Of Domain. ')
ax.grid()
ax.legend()
plt.savefig('figures/species_mole_fractions.pdf')


# mean molar mass
fig, ax = plt.subplots()
ax.plot(X_points, W)
ax.set_xlabel('x [mm]')
ax.set_ylabel('W [g/mol]')
ax.set_title('Mean Molar Mass Over Length Of Domain. ')
ax.grid()
plt.savefig('figures/mean_molar_mass.pdf')

#density
fig, ax = plt.subplots()
ax.plot(X_points, rho)
ax.set_xlabel('x [mm]')
ax.set_ylabel(r'$\rho$ [kg/m3]')
ax.set_title('Mean Density Over Length Of Domain. ')
ax.grid()
plt.savefig('figures/mean_density.pdf')

# b) Thermal conductivity of the mixture (see appendix)
fig, ax = plt.subplots()
ax.plot(X_points, ave_lambda)
ax.set_xlabel('x [mm]')
ax.set_ylabel(r'$\lambda$ [W/(m K)]')
ax.set_title('Mean Lambda Over Length Of Domain. ')
ax.grid()
plt.savefig('figures/mean_lambda.pdf')




# c) Species diffusion coefficients predicted by the four models
## Model 1: Fick's
fig, ax = plt.subplots()
ax.plot(X_points[d_h2n2_fick>0], d_h2n2_fick[d_h2n2_fick>0], label=r'$D_{H_2N_2}$')
ax.plot(X_points[d_h2o2_fick>0], d_h2o2_fick[d_h2o2_fick>0], label=r'$D_{H_2O_2}$')
ax.plot(X_points[d_n2n2_fick>0], d_n2n2_fick[d_n2n2_fick>0], label=r'$D_{N_2N_2}$')
ax.plot(X_points[d_o2n2_fick>0], d_o2n2_fick[d_o2n2_fick>0], label=r'$D_{O_2N_2}$', linestyle='dotted')
ax.plot(X_points[d_o2o2_fick>0], d_o2o2_fick[d_o2o2_fick>0], label=r'$D_{O_2O_2}$')
ax.plot(X_points[d_n2o2_fick>0], d_n2o2_fick[d_n2o2_fick>0], label=r'$D_{N_2O_2}$', linestyle='dotted')
ax.set_xlabel('x [mm]')
ax.set_ylabel(r'$D_{ij}$ [m2/s]')
ax.set_title('Fick\'s Diffusion Coefficiencts\n Over Length Of Domain.')
ax.grid()
ax.legend()
plt.savefig('figures/fick_diff_coef.pdf', bbox_inches='tight', pad_inches=0.2)


## Model 2: Wilke
fig, ax = plt.subplots()
ax.plot(X_points, D_h2_wilke, label=r'$D_{wilke,H_2}$')
ax.plot(X_points, D_o2_wilke, label=r'$D_{wilke,O_2}$')
ax.plot(X_points, D_n2_wilke, label=r'$D_{wilke,N_2}$')
ax.set_xlabel('x [mm]')
ax.set_ylabel(r'$D_{wilke,i}$ [m2/s]')
ax.set_title('Wilke Diffusion Coefficients Over Length Of Domain. ')
ax.grid()
ax.legend()
plt.savefig('figures/wilke_diff_coef.pdf')



## Model 3: Le=1
fig, ax = plt.subplots()
ax.plot(X_points, D_Le_1)
ax.set_xlabel('x [mm]')
ax.set_ylabel(r'$D_{Le=1}$ [m2/s]')
ax.set_title('Le = 1 Diffusion Coefficient Over Length Of Domain. ')
ax.grid()
plt.savefig('figures/Le_1_diff_coef.pdf')

## Model 4: Le=const
fig, ax = plt.subplots()
ax.plot(X_points, D_Le_const_h2, label=r'$D_{Le=const,H_2}$')
ax.plot(X_points, D_Le_const_o2, label=r'$D_{Le=const,O_2}$')
ax.plot(X_points, D_Le_const_n2, label=r'$D_{Le=const,N_2}$')
ax.set_xlabel('x [mm]')
ax.set_ylabel(r'$D_{Le=const,i}$ [m2/s]')
ax.set_title('Le=const Diffusion Coefficients Over Length Of Domain. ')
ax.grid()
ax.legend()
plt.savefig('figures/Le_const_diff_coef.pdf')




# d) Continue with the first and fourth of the models introduced above. Compute the species mass fluxes
# predicted by these two models at 𝑥 = 0.5𝐿 (the midpoint). Comment on the differences [3 pts];
X_points /= 1000
# 1) retrieve Di at x = 0.5
# 2) retrieve rho at x = 0.5
# 3) gradient of Yi of not abundant species
### 3a) use the midpoint rule to approximate gradient of diffusive mass flux
# 4) calculate abundant species by using sum Yi Vi

# FICK H2 species mass flux
# find dY/dx @ x=0.5 +- h using midpoint rule
# find Di @ x=0.5 +- h to determine for the diffusive mass flux gradient
# find rho @ x=0.5 +- h

def get_sp_m_flux_grad_non_abundant(rho_arr, D_arr, Y_arr):
    mid_index = int((N-1)/2)
    dx = L/(N-1)
    dY_dx = (Y_arr[mid_index+1] - Y_arr[mid_index-1])/(2*dx)
    dY_dx_plus_1 = (Y_arr[mid_index+2] - Y_arr[mid_index])/(2*dx)
    dY_dx_min_1 = (Y_arr[mid_index] - Y_arr[mid_index-2])/(2*dx)
    # d2Y_dx2 = (dY_dx_plus_1 - dY_dx_min_1)/(2*dx)

    # get the mass flux grad
    J_x_min_h = rho_arr[mid_index-1] * D_arr[mid_index-1] * dY_dx_min_1
    J = rho_arr[mid_index] * D_arr[mid_index] * dY_dx
    J_x_plus_h = rho_arr[mid_index+1] * D_arr[mid_index+1] * dY_dx_plus_1
    dJdx = (J_x_plus_h - J_x_min_h) / (2*dx)


    return -1*dJdx, J, J_x_min_h, J_x_plus_h

d_rho_dt_fick_h2, J_h2, J_h2_min_1, J_h2_plus_1 = get_sp_m_flux_grad_non_abundant(rho, d_h2n2_fick, Y_1)
d_rho_dt_fick_o2, J_o2, J_o2_min_1, J_o2_plus_1 = get_sp_m_flux_grad_non_abundant(rho, d_o2n2_fick, Y_2)

# use sum of YV=0
dx = L / (N-1)
rhoYV_n2 = 0 - (J_h2+J_o2)
rhoYV_n2_plus_1 = 0 - (J_h2_plus_1+J_o2_plus_1)
rhoYV_n2_min_1 = 0 - (J_h2_min_1+J_o2_min_1)
grad_J_n2 = -1 * (rhoYV_n2_plus_1 - rhoYV_n2_min_1)/(2*dx)

print(f'h2 mass flux = {d_rho_dt_fick_h2:.2f} kg/s m2')
print(f'o2 mass flux = {d_rho_dt_fick_o2:.2f} kg/s m2')
print(f'n2 mass flux = {grad_J_n2:.2f} kg/s m2')
# FICK 02 species mass flux

# FICK N2 species mass flux


# Le = const H2 mass flux



# e) Explain how difference in hydrogen diffusive flux could have an impact on flame speed [5 pts].1

# Now consider the case with methane instead of hydrogen. The spatial profiles of the species molar
# fractions are identical to the previous case, but species 1 is now CH4. Compute and plot profiles in the
# domain of the following quantities:
# f) Species diffusion coefficients predicted by models 2) 3) and 4) [3 pts];
# g) Species mass fluxes predicted by the three models at the midpoint 𝑥 = 0.5𝐿 [3 pts];
# h) Describe and comment differences and similarities between the obtained results and the hydrogen
# case