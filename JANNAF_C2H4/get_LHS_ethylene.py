import numpy as np
from .get_cp import get_cp
from .get_jannaf import get_jannaf

def get_LHS_ethylene(phi):
    W_c2h4 = 28.05
    W_o2 = 31.999
    W_n2 = 28.01
    W_h2o = 18.01528
    W_co2 = 44.01

    X_c2h4_reac = 1
    X_o2_reac = 3 / phi
    X_n2_reac = 3 / phi * 3.76
    X_c2h4_prod = 0
    X_o2_prod = 0
    X_n2_prod = 3 / phi * 3.76
    X_co2 = 2
    X_h2o = 2
    if phi > 1:
        X_c2h4_prod = 1 - 1 / phi
        X_co2 = 2 / phi
        X_h2o = 2 / phi

    if phi < 1:
        X_o2_prod = (1 / phi - 1) * 3

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

    h0_c2h4 = 52.10/W_c2h4 *10**3 #kj/mol to j/g
    h0_o2 = 0
    h0_n2 = 0
    h0_co2 = -393.5/W_co2 *10**3
    h0_h2o = -241.81/ W_h2o *10**3

    LHS = (Y_c2h4_reac - Y_c2h4_prod)*h0_c2h4 + (Y_o2_reac -Y_o2_prod)*h0_o2 + \
          (Y_n2_reac- Y_n2_prod)*h0_n2 - Y_co2*h0_co2 - Y_h2o*h0_h2o

    return LHS
