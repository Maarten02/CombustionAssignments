import numpy as np
from .get_cp import get_cp
from .get_jannaf import get_jannaf

def get_cp_mix(phi, temp):
    W_c2h4 = 28.05
    W_o2 = 31.999
    W_n2 = 28.01
    W_h2o = 18.01528
    W_co2 = 44.01

    n_tot_reac = 1 + 3 / phi + 3 / phi * 3.76
    n_c2h4_reac = 1
    n_o2_reac = 3 / phi
    n_n2_reac = 3 / phi * 3.76
    n_c2h4_prod = 0
    n_o2_prod = 0
    n_n2_prod = 3 / phi * 3.76
    n_co2 = 2
    n_h2o = 2
    n_tot_prod = 3 * 3.76 + 2 + 2
    if phi > 1:
        n_c2h4_prod = 1 - 1 / phi
        n_co2 = 2 / phi
        n_h2o = 2 / phi
        n_tot_prod = 1 - 1 / phi + 3 / phi * 3.76 + 2 / phi + 2 / phi
    if phi < 1:
        n_o2_prod = (1 / phi - 1) * 3
        n_tot_prod = (1 / phi - 1) * 3 + 3 / phi * 3.76 + 2 + 2

    X_c2h4_reac = n_c2h4_reac / n_tot_reac
    X_o2_reac = n_o2_reac / n_tot_reac
    X_n2_reac = n_n2_reac / n_tot_reac
    X_c2h4_prod = n_c2h4_prod / n_tot_prod
    X_o2_prod = n_o2_prod / n_tot_prod
    X_n2_prod = n_n2_prod / n_tot_prod
    X_co2 = n_co2 / n_tot_prod
    X_h2o = n_h2o / n_tot_prod

    W_reac = X_c2h4_reac*W_c2h4 + X_o2_reac*W_o2 + X_n2_reac*W_n2
    W_prod = X_c2h4_prod*W_c2h4 + X_o2_prod*W_o2 + X_n2_prod*W_n2 + X_co2*W_co2 + X_h2o*W_h2o

    Y_c2h4_reac = X_c2h4_reac * W_c2h4/W_reac
    Y_o2_reac = X_o2_reac * W_o2/W_reac
    Y_n2_reac = X_n2_reac * W_n2/W_reac
    Y_c2h4_prod = X_c2h4_prod * W_c2h4/W_prod
    Y_o2_prod = X_o2_prod * W_o2/W_prod
    Y_n2_prod = X_n2_prod * W_n2/W_prod
    Y_co2 = X_co2 * W_co2/W_prod
    Y_h2o = X_h2o * W_h2o/W_prod

    compounds, coefs1, coefs2 = get_jannaf()
    cp_list = np.empty(len(compounds))
    for i, (coef1, coef2) in enumerate(zip(coefs1, coefs2)):
        cp_list[i] = get_cp(coef1, coef2, temp)

    #                  W_H2,  W_O2,   W_N2,  W_CO2, W_H2O, W_C2H4
    w_list = np.array([2.016, 31.999, 28.01, 44.01, 18.01528, 28.05]) # [g/mol]
    R = 8.314  # J/mol K
    R_bar = R / w_list  # kJ/kg K = [J/mol K] / [g/mol]
    #print('C2H4 R bar = ', R_bar)

    #cp_h2 = cp_list[0]*R_bar[0]
    cp_o2 = cp_list[1]*R_bar[1] # [kJ/kg K] = [-] * [kJ/kg K]
    cp_n2 = cp_list[2]*R_bar[2] # [kJ/kg K] = [-] * [kJ/kg K]
    cp_co2 = cp_list[3]*R_bar[3] # [kJ/kg K] = [-] * [kJ/kg K]
    cp_h2o = cp_list[4]*R_bar[4] # [kJ/kg K] = [-] * [kJ/kg K]
    cp_c2h4 = cp_list[5]*R_bar[5] # [kJ/kg K] = [-] * [kJ/kg K]
    cp_reac_mix = Y_c2h4_reac*cp_c2h4 + Y_o2_reac*cp_o2 + Y_n2_reac*cp_n2
    cp_prod_mix = Y_c2h4_prod*cp_c2h4 + Y_o2_prod*cp_o2 + Y_n2_prod*cp_n2 + Y_co2*cp_co2 + Y_h2o*cp_h2o

    return cp_reac_mix, cp_prod_mix # kJ/kg K | kJ/kg K




