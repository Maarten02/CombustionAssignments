import numpy as np
from .get_cp import get_cp
from .get_jannaf import get_jannaf

def get_cp_mix(phi, temp):
    W_h2 = 2.016
    W_o2 = 31.999
    W_h2o = 18.01528
    W_n2 = 28.01

    X_h2_reac = 1
    X_o2_reac = 0.5/ phi
    X_n2_reac = 0.5 / phi * 3.76
    X_o2_prod = 0
    X_h2_prod = 0
    X_n2_prod = 0.5 / phi * 3.76
    X_h2o = 1
    if phi > 1:
        X_h2_prod = 1 - 1/phi
        X_h2o = 1/phi

    if phi < 1:
        X_o2_prod = (1/phi - 1)*0.5

    W_reac = X_h2_reac*W_h2 + X_o2_reac*W_o2 + X_n2_reac*W_n2
    W_prod = X_h2_prod*W_h2 + X_o2_prod*W_o2 + X_n2_prod*W_n2 + X_h2o*W_h2o

    Y_h2_reac = X_h2_reac * W_h2/W_reac
    Y_o2_reac = X_o2_reac * W_o2/W_reac
    Y_n2_reac = X_n2_reac * W_n2/W_reac
    Y_h2_prod = X_h2_prod * W_h2/W_prod
    Y_o2_prod = X_o2_prod * W_o2/W_prod
    Y_n2_prod = X_n2_prod * W_n2/W_prod
    Y_h2o = X_h2o * W_h2o/W_prod

    compounds, coefs1, coefs2 = get_jannaf()
    cp_list = np.empty(len(compounds))
    for i,(coef1, coef2) in enumerate(zip(coefs1, coefs2)):
        cp_list[i] = get_cp(coef1, coef2, temp)

    #                  W_H2,  W_O2,   W_N2,  W_CO2, W_H2O,    W_C2H4
    w_list = np.array([2.016, 31.999, 28.01, 44.01, 18.01528, 28.05])
    R = 8.314  # /mol
    R_bar = R / w_list  # /g

    cp_h2 = cp_list[0]*R_bar[0]
    cp_o2 = cp_list[1]*R_bar[1]
    cp_n2 = cp_list[2]*R_bar[2]
    cp_h2o = cp_list[4]*R_bar[4]

    cp_reac_mix = Y_h2_reac*cp_h2 + Y_o2_reac*cp_o2 + Y_n2_reac*cp_n2
    cp_prod_mix = Y_h2_prod*cp_h2 + Y_o2_prod*cp_o2 + Y_n2_prod*cp_n2 + Y_h2o*cp_h2o

    return cp_reac_mix, cp_prod_mix




