from read_chem1d import readchem1d
import numpy as np
import matplotlib.pyplot as plt
"""Questions
1. equivalence ratio is specified to be 0.6 both at the left and right boundary
2. The flame thickness; should this be total thickness, diffusion thickness or the thickness from temperature gradients?
3. what is consumption speed? (m/s) or mol/s  or kg/s?
Sc in slides: m/s
4. what is a normal order or magnitude for mass flux (unit: kg/m2 s)

"""
#a) For a methane/air case at equivalence ratio 0.6, compute the flamelet solution in Chem1d for strain
# rate values of 100 s-1, 200 s-1, 500 s-1, 1000 s-1, 5000 s-1 and 10000 s-1. Plot the peak reaction rate of
# water, consumption speed and flame thickness with varying strain. Use a logarithmic scale for the x-
# axis (strain). Explain the behaviour observed

# b) Now for the same conditions at strain rates, compute the solutions for hydrogen/air flamelets. Plot
# the results of peak reaction rate, consumption speed and flame thickness (add the curves on the same
# plots used for point a)). Comment on the differences

############################ Q3A/B - CONSUMPTION SPEED ##########################################
def get_consumption_speed(yiend_file, siend_file, fuel, db=True, _print=False):
    if fuel == 'CH4':
        M_fuel = 16.04 # [g/mol]
    elif fuel == "H2":
        M_fuel = 2.018
    else:
        raise Exception('Fuel not recognized')

    s, t, a = readchem1d(siend_file)
    y, t_y, a_y = readchem1d(yiend_file)

    fuel_col = a_y.index(fuel) - 1
    data = s[:, fuel_col]
    x_pos = s[:, 0]

    rho_col = a_y.index('Density') - 1
    rho_u = y[0, rho_col]                 # [g/cm^3] TODO: CHECK IF THIS IS THE CORRECT DENSITY
    Y_fu = y[0, fuel_col]                           # TODO: CHECK IF THIS THE CORRECT MIXTURE FRACTION

    if fuel == 'CH4' and db == True:
        fig_db, ax_db = plt.subplots()
        ax_db.semilogx(x_pos, data)
        ax_db.set_title('CH4 REAC RATE')
        strain = yiend_file[94:-4]
        fig_db.savefig(f'debug_CH4{strain}.jpg')

    # Integrate reaction rate on entire domain
    consumption_speed = 0
    for i in range(len(data) - 1):
        consumption_speed += (data[i] + data[i+1]) * 0.5 * (x_pos[i+1] - x_pos[i])

    consumption_speed *= M_fuel
    consumption_speed /= (rho_u * Y_fu)     # [cm/s]
    consumption_speed /= -100               # [m/s]

    if _print:
        print(f'Consumption speed integral = {consumption_speed:.10f} [m/s]')

    return consumption_speed

############# Q3A/B - PEAK H2O REACTION RATE ##########################################
def get_H2O_reac_rate(siend_file):
    s, t, a = readchem1d(siend_file)
    H2O_col = a.index('H2O') - 1
    H2O_reac_rate = np.max(s[:, H2O_col]) # VERIFY THAT REACTION RATES ARE +VE

    return H2O_reac_rate

############# Q3A/B - FLAME THICKNESSES ##########################################
flame_thickness_lst_H2 = [4.8316715E-01, 3.3908386E-01, 2.1110010E-01, 1.4724939E-01, 6.3644368E-02, 4.4218311E-02] # TODO: INSERT THE ACTUAL THICKNESSES
flame_thickness_lst_CH4 = [2.4763448E-02, 8.0425167E-02, 7.7352965E-02, 7.1996035E-02, 5.0697894E-02, 3.5856519E-02] # TODO: INSERT THE ACTUAL THICKNESSES


############# Q3A/B - PLOTTING ##########################################
fuels = ['CH4', 'H2']
project = r'C:/Users/maart/OneDrive/Documents/MSc/Combustion/CombustionAssignments/Assignment 2'
strains = [100, 200, 500, 1000, 5000, 10000]
fig_cs, ax_cs = plt.subplots()
fig_rr, ax_rr = plt.subplots()
fig_ft, ax_ft = plt.subplots()

for fuel, ftl in zip(fuels, [flame_thickness_lst_CH4, flame_thickness_lst_H2]):

    consumption_speed_lst = []
    H2O_reac_rate_lst = []

    folder = project + '/' + fuel
    for strain in strains:
        yiend_file = folder + '/yi_' + fuel.lower() + '_' + str(strain) + '.dat'
        siend_file = folder + '/si_' + fuel.lower() + '_' + str(strain) + '.dat'

        cons_spd = get_consumption_speed(yiend_file, siend_file, fuel)
        H2O_reac_rate = get_H2O_reac_rate(siend_file)
        consumption_speed_lst.append(cons_spd)
        H2O_reac_rate_lst.append(H2O_reac_rate)

    ax_cs.semilogx(strains, consumption_speed_lst, label=fuel)
    ax_rr.semilogx(strains, H2O_reac_rate_lst, label=fuel)
    ax_ft.semilogx(strains, ftl, label=fuel)

ax_cs.set_xlabel('Strain Rate [$s^{-1}$]')
ax_cs.set_ylabel('Consumption Speed ($S_c$) [$m/s$]')
ax_cs.set_title('Consumption speed vs. Strain rate')
ax_cs.grid()
ax_cs.legend()
fig_cs.savefig('./figures/strain_vs_consspeed.pdf', bbox_inches='tight', pad_inches=0.2)

ax_rr.set_xlabel('Strain Rate [$s^{-1}$]')
ax_rr.set_ylabel('H2O Reaction Rate [$mole/m^3 s$]')
ax_rr.set_title('H2O reaction rate vs. Strain rate')
ax_rr.grid()
ax_rr.legend()
fig_rr.savefig('./figures/strain_vs_h2o_rr.pdf', bbox_inches='tight', pad_inches=0.2)

ax_ft.set_xlabel('Strain Rate [$s^{-1}$]')
ax_ft.set_ylabel('Flame Thickness [$m$]')  # TODO: VERIFY UNIT
ax_ft.set_title('Flame Thickness vs. Strain rate')
ax_ft.grid()
ax_ft.legend()
fig_ft.savefig('./figures/strain_vs_flame_thick.pdf', bbox_inches='tight', pad_inches=0.2)



#c) Compute the Markstein length ℒ = − 𝑑𝑠𝑐/𝑑𝐾, where 𝐾 is the stretch rate and 𝑠𝑐 is the consumption
# speed, for the two mixtures of points a) and b). Explain the differences observed in the results.
fig_ml, ax_ml = plt.subplots()
#fuels = ['H2']
for fuel in fuels:

    ml_arr = []
    folder = project + '/' + fuel + '_markenstein'

    for strain in strains:
        step = 1
        d_cs = 0
        for h in [1, -1]:
            yiend_file = folder + '/yi_' + fuel.lower() + '_' + str(int(strain+h*step)) + '.dat'
            siend_file = folder + '/si_' + fuel.lower() + '_' + str(int(strain+h*step)) + '.dat'

            cons_spd = get_consumption_speed(yiend_file, siend_file, fuel, db=False)
            d_cs += cons_spd * h
        ml = d_cs / (2 * step)
        ml_arr.append(ml)

    ax_ml.semilogx(strains, ml_arr, label=fuel)

ax_ml.set_xlabel('Strain Rate [$s^{-1}$]')
ax_ml.set_ylabel('Markstein Length [$m$]')  # TODO: VERIFY UNIT
ax_ml.set_title('Flame Thickness vs. Strain rate')
ax_ml.grid()
ax_ml.legend()
fig_ml.savefig('./figures/strain_vs_markstein.pdf', bbox_inches='tight', pad_inches=0.2)

# d) Now for the same strain rates compute, non-premixed flamelets in a methane to air opposite jet
# configuration. Plot the peak reaction rate of water, and the stoichiometric scalar dissipation rate of
# mixture fraction versus strain. Now also plot the variation of flame temperature versus mixture fraction
# for the different strain rates. Comment on

# TODO: FIGURE OUT WHAT STOICHIOMETRIC SCALAR DISSIPATION RATE IS
# TODO: GET FLAME TEMP (FROM CHEM1D??)