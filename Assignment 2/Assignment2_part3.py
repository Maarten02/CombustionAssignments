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

########################################################################################################################
########################################## FUNCTIONS ###################################################################
########################################################################################################################

def get_consumption_speed(yiend_file, siend_file, fuel, db=True, _print=False):
    if fuel == 'CH4':
        M_fuel = 16.04 # [g/mol]
    elif fuel == "H2":
        M_fuel = 2.018
    else:
        raise Exception('Fuel not recognized')

    s, t, a = readchem1d(siend_file)
    y, t_y, a_y = readchem1d(yiend_file)

    fuel_col_s = a.index(fuel) - 1
    fuel_col_y = a_y.index(fuel) - 1
    data = s[:, fuel_col_s]
    x_pos = s[:, 0]

    rho_col = a_y.index('Density') - 1
    rho_u = y[0, rho_col]                 # [g/cm^3] TODO: CHECK IF THIS IS THE CORRECT DENSITY
    Y_fu = y[0, fuel_col_y]                        # TODO: CHECK IF THIS THE CORRECT MIXTURE FRACTION

    if fuel == 'CH4' and db == True:
        fig_db, ax_db = plt.subplots()
        ax_db.plot(x_pos, data)
        ax_db.set_title('CH4 REAC RATE')
        strain = yiend_file[94:-4]
        fig_db.savefig(f'./debug/debug_CH4{strain}.jpg')

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
def get_H2O_reac_rate(siend_file, fuel, db=False):
    s, t, a = readchem1d(siend_file)
    x_pos = s[:,0]
    H2O_col = a.index('H2O') - 1
    H2O_reac_rate = np.max(s[:, H2O_col]) # TODO: VERIFY THAT REACTION RATES ARE +VE

    if db == True:
        fig_db, ax_db = plt.subplots()
        ax_db.plot(x_pos, s[:,H2O_col])
        ax_db.set_title(f'H2O REAC RATE {fuel}')
        if fuel == 'CH4':
            strain = siend_file[94:-4]
        else:
            strain = siend_file[92:-4]
        fig_db.savefig(f'./debug/debug_H2O_{strain}_{fuel}.jpg')

    return H2O_reac_rate

########################################################################################################################
#AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA - GET TEMP VS. MIXFRAC - BBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBB#
########################################################################################################################
#a) For a methane/air case at equivalence ratio 0.6, compute the flamelet solution in Chem1d for strain
# rate values of 100 s-1, 200 s-1, 500 s-1, 1000 s-1, 5000 s-1 and 10000 s-1. Plot the peak reaction rate of
# water, consumption speed and flame thickness with varying strain. Use a logarithmic scale for the x-
# axis (strain). Explain the behaviour observed

# b) Now for the same conditions at strain rates, compute the solutions for hydrogen/air flamelets. Plot
# the results of peak reaction rate, consumption speed and flame thickness (add the curves on the same
# plots used for point a)). Comment on the differences


############# Q3A/B - FLAME THICKNESSES ##########################################
flame_thickness_lst_H2 = [4.8316715E-01, 3.3908386E-01, 2.1110010E-01, 1.4724939E-01, 6.3644368E-02, 4.4218311E-02]
flame_thickness_lst_CH4 = [2.4763448E-02, 8.0425167E-02, 7.7352965E-02, 7.1996035E-02, 5.0697894E-02, 3.5856519E-02]


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
        H2O_reac_rate = get_H2O_reac_rate(siend_file, fuel)
        consumption_speed_lst.append(cons_spd)
        H2O_reac_rate_lst.append(H2O_reac_rate)

    ax_cs.semilogx(strains, consumption_speed_lst, label=fuel, marker='.')
    ax_rr.semilogx(strains, H2O_reac_rate_lst, label=fuel, marker='.')
    ax_ft.semilogx(strains, ftl, label=fuel, marker='.')

ax_cs.set_xlabel('Strain Rate [$s^{-1}$]')
ax_cs.set_ylabel('Consumption Speed ($S_c$) [$m/s$]')
ax_cs.set_title('Consumption speed vs. Strain rate')
ax_cs.grid()
ax_cs.legend()
fig_cs.savefig('./figures/strain_vs_consspeed.pdf', bbox_inches='tight', pad_inches=0.2)

ax_rr.set_xlabel('Strain Rate [$s^{-1}$]')
ax_rr.set_ylabel('H2O Reaction Rate [$mole/cm^3 s$]')
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



########################################################################################################################
#CCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCC - MARKSTEIN - CCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCC#
########################################################################################################################
#c) Compute the Markstein length ℒ = − 𝑑𝑠𝑐/𝑑𝐾, where 𝐾 is the stretch rate and 𝑠𝑐 is the consumption
# speed, for the two mixtures of points a) and b). Explain the differences observed in the results.

fig_ml, ax_ml = plt.subplots()
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
        ml = d_cs / (2 * step) * -1
        ml_arr.append(ml)

    ax_ml.semilogx(strains, ml_arr, label=fuel, marker='.')

ax_ml.set_xlabel('Strain Rate [$s^{-1}$]')
ax_ml.set_ylabel('Markstein Length [$m$]')  # TODO: VERIFY UNIT
ax_ml.set_title('Markstein Length vs. Strain rate')
ax_ml.grid()
ax_ml.legend()
fig_ml.savefig('./figures/strain_vs_markstein.pdf', bbox_inches='tight', pad_inches=0.2)



########################################################################################################################
#DDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDD - GET TEMP VS. MIXFRAC - DDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDD#
########################################################################################################################
# d) Now for the same strain rates compute, non-premixed flamelets in a methane to air opposite jet
# configuration. Plot the peak reaction rate of water, and the stoichiometric scalar dissipation rate of
# mixture fraction versus strain. Now also plot the variation of flame temperature versus mixture fraction
# for the different strain rates. Comment on

strains = [100, 200, 500, 1000, 5000, 10000]
scalar_dissi_rate_ch4 = [2.6507542E-21, 6.6435559E-22, 7.0121529E-23, 2.4917503E-17, 1.5002759E-14, 3.5299822E-14] # VS strain


fig_sdr, ax_sdr = plt.subplots() # SDR vs. Strain
fig_rr_2, ax_rr_2 = plt.subplots()  # The reaction rate of water vs. Strain
fig_temp, ax_temp = plt.subplots()  # temp vs. mixFrac for different Strainrates


consumption_speed_lst = []
H2O_reac_rate_lst = []

folder = project + '/CH4_non_premixed'
for strain in strains:


    yiend_file = folder + '/yi_ch4_' + str(strain) + '.dat'
    siend_file = folder + '/si_ch4_' + str(strain) + '.dat'

    H2O_reac_rate = get_H2O_reac_rate(siend_file, 'CH4')
    H2O_reac_rate_lst.append(H2O_reac_rate)

    y, t, a = readchem1d(yiend_file)

    temp_col = a.index('Temp') - 1
    fuel_col = a.index('CH4') - 1
    nitro_col = a.index('N2') - 1
    oxy_col = a.index('O2') - 1

    temp = y[:,temp_col]

    deno = y[:, fuel_col] + y[:, oxy_col] + y[:, nitro_col]
    mixfrac = y[:,fuel_col] / deno

    ax_temp.plot(mixfrac, temp, label=f'$a$ = {strain} [$s^{-1}$]')

ax_sdr.semilogx(strains, scalar_dissi_rate_ch4, marker='.')
ax_sdr.set_xlabel('Strain rate [$s^{-1}$]')
ax_sdr.set_ylabel('Scalar Dissipation Rate [$s^{-1}$]')
ax_sdr.set_title('Scalar Dissipation Rate vs. Strain rate')
ax_sdr.grid()
fig_sdr.savefig('./figures/strain_vs_sdr_NONPM.pdf', bbox_inches='tight', pad_inches=0.2)

ax_rr_2.semilogx(strains, H2O_reac_rate_lst, marker='.')
ax_rr_2.set_xlabel('Strain rate [$s^{-1}$]')
ax_rr_2.set_ylabel('Peak water reaction rate [$mol/cm^3 s$]')
ax_rr_2.set_title('Peak water reaction rate vs. strain rate')
ax_rr_2.grid()
fig_rr_2.savefig('./figures/strain_vs_water_NONPM.pdf', bbox_inches='tight', pad_inches=0.2)

ax_temp.set_xlabel('Mixture Fraction [-]')
ax_temp.set_ylabel('Flame temperature [$K$]')
ax_temp.set_title('Flame temperature vs. Mixture Fraction for different strain rates')
ax_temp.grid()
ax_temp.legend()
fig_temp.savefig('./figures/mixfrac_vs_temp_NONPM.pdf', bbox_inches='tight', pad_inches=0.2)



# TODO: FIGURE OUT WHAT STOICHIOMETRIC SCALAR DISSIPATION RATE IS
# TODO: GET FLAME TEMP (FROM CHEM1D??)