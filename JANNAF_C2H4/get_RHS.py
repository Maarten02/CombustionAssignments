import numpy as np
from .get_cp import get_cp
from .get_jannaf import get_jannaf
from .get_cp_mix import get_cp_mix

def integrate_cp(T_left, T_right, h, phi, reac):
    #print('Tleft', T_left)
    #print('Tright', T_right)
    N = int((T_right - T_left) / h)
    h_real = (T_right - T_left) / N
    cp_vec = np.empty(N)
    for i, temp in enumerate(np.linspace(T_left, T_right, N)):

        cp_reac_mix, cp_prod_mix = get_cp_mix(phi, temp)
        if reac:
            cp_vec[i] = cp_prod_mix
        else:
            cp_vec[i] = cp_reac_mix

    stencil = 2 * np.ones(N)
    stencil[0] = 1
    stencil[-1] = 1

    integral = np.dot(stencil, cp_vec) * 0.5 * h_real
    return integral

def get_RHS(phi, T_ad):
    T_0 = 298.15
    T_reac = 298.15
    N = 200
    cp_reac_mix_tot = 0
    cp_prod_mix_tot = 0

    #reac_int = integrate_cp(T_0, T_reac, 3, phi, True)
    reac_int = 0
    prod_int = integrate_cp(T_0, T_ad, 0.5, phi, False)

    RHS = prod_int - reac_int

    return RHS


