import numpy as np
from .get_cp import get_cp
from .get_jannaf import get_jannaf

def get_LHS_ethylene(phi):
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

    W_reac = X_c2h4_reac * W_c2h4 + X_o2_reac * W_o2 + X_n2_reac * W_n2
    W_prod = X_c2h4_prod * W_c2h4 + X_o2_prod * W_o2 + X_n2_prod * W_n2 + X_co2 * W_co2 + X_h2o * W_h2o

    Y_c2h4_reac = X_c2h4_reac * W_c2h4 / W_reac
    Y_o2_reac = X_o2_reac * W_o2 / W_reac
    Y_n2_reac = X_n2_reac * W_n2 / W_reac
    Y_c2h4_prod = X_c2h4_prod * W_c2h4 / W_prod
    Y_o2_prod = X_o2_prod * W_o2 / W_prod
    Y_n2_prod = X_n2_prod * W_n2 / W_prod
    Y_co2 = X_co2 * W_co2 / W_prod
    Y_h2o = X_h2o * W_h2o / W_prod

    h0_c2h4 = 52.10 / W_c2h4 * 10**3 #kj/mol to j/g
    h0_o2 = 0
    h0_n2 = 0
    h0_co2 = -393.509 / W_co2 * 10**3
    h0_h2o = -241.818 / W_h2o * 10**3

    LHS = (Y_c2h4_reac - Y_c2h4_prod)*h0_c2h4 + (Y_o2_reac - Y_o2_prod)*h0_o2 + \
          (Y_n2_reac - Y_n2_prod)*h0_n2 - Y_co2*h0_co2 - Y_h2o*h0_h2o

    return LHS
