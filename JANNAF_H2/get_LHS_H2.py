import numpy as np
from .get_cp import get_cp
from .get_jannaf import get_jannaf

def get_LHS_h2(phi):
    W_h2 = 2.016
    W_o2 = 31.999
    W_n2 = 28.01
    W_h2o = 18.01528

    X_h2_reac = 1
    X_o2_reac = 0.5 / phi
    X_n2_reac = 0.5 / phi * 3.76
    X_h2_prod = 0
    X_o2_prod = 0
    X_n2_prod = 0.5 / phi * 3.76
    X_h2o = 1

    if phi > 1:
        X_h2_prod = 1 - 1 / phi
        X_h2o = 1 / phi

    if phi < 1:
        X_o2_prod = (1 / phi - 1) * 0.5

    W_reac = X_h2_reac * W_h2 + X_o2_reac * W_o2 + X_n2_reac * W_n2
    W_prod = X_h2_prod * W_h2 + X_o2_prod * W_o2 + X_n2_prod * W_n2 + X_h2o * W_h2o

    Y_h2_reac = X_h2_reac * W_h2 / W_reac
    Y_o2_reac = X_o2_reac * W_o2 / W_reac
    Y_n2_reac = X_n2_reac * W_n2 / W_reac
    Y_h2_prod = X_h2_prod * W_h2 / W_prod
    Y_o2_prod = X_o2_prod * W_o2 / W_prod
    Y_n2_prod = X_n2_prod * W_n2 / W_prod
    Y_h2o = X_h2o * W_h2o / W_prod

    h0_h2 = 0
    h0_o2 = 0
    h0_n2 = 0
    h0_h2o = -241.81/ W_h2o *10**3 #kj/mol to j/g

    LHS = (Y_h2_reac - Y_h2_prod)*h0_h2 + (Y_o2_reac - Y_o2_prod)*h0_o2 + \
          (Y_n2_reac - Y_n2_prod)*h0_n2 - Y_h2o*h0_h2o

    return LHS
