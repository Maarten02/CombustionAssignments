import numpy as np
from ..JANNAF_H2.get_cp import get_cp
from ..JANNAF_H2.get_jannaf import get_jannaf

def intcph2(phi, T0, Tad, Tr):
    W_h2 = 2.016
    W_o2 = 31.999
    W_h2o = 18.01528
    W_n2 = 28.01

    n_tot_reac = 1 + 0.5/phi + 0.5/phi*3.76
    n_h2_reac = 1
    n_o2_reac = 0.5 / phi
    n_n2_reac = 0.5 / phi * 3.76
    n_o2_prod = 0
    n_h2_prod = 0
    n_n2_prod = 0.5 / phi * 3.76
    n_h2o = 1
    n_tot_prod = 1 + 0.5*3.76
    if phi > 1:
        n_h2_prod = 1 - 1 / phi
        n_h2o = 1 / phi
        n_tot_prod = 1/phi + 1 - 1/phi + 0.5/phi * 3.76
    if phi < 1:
        n_o2_prod = (1 / phi - 1) * 0.5
        n_tot_prod = (1/phi - 1) * 0.5 + 1 + 0.5/phi * 3.76

    X_h2_reac = n_h2_reac / n_tot_reac
    X_o2_reac = n_o2_reac / n_tot_reac
    X_n2_reac = n_n2_reac / n_tot_reac
    X_o2_prod = n_o2_prod / n_o2_prod
    X_h2_prod = n_h2_prod / n_tot_prod
    X_n2_prod = n_n2_prod / n_tot_prod
    X_h2o = n_h2o / n_tot_prod

    W_reac = X_h2_reac * W_h2 + X_o2_reac * W_o2 + X_n2_reac * W_n2
    W_prod = X_h2_prod * W_h2 + X_o2_prod * W_o2 + X_n2_prod * W_n2 + X_h2o * W_h2o

    Y_h2_reac = X_h2_reac * W_h2 / W_reac
    Y_o2_reac = X_o2_reac * W_o2 / W_reac
    Y_n2_reac = X_n2_reac * W_n2 / W_reac
    Y_h2_prod = X_h2_prod * W_h2 / W_prod
    Y_o2_prod = X_o2_prod * W_o2 / W_prod
    Y_n2_prod = X_n2_prod * W_n2 / W_prod
    Y_h2o = X_h2o * W_h2o / W_prod

    compounds, coefs1, coefs2 = get_jannaf()


    #                  W_H2,  W_O2,   W_N2,  W_CO2, W_H2O, W_C2H4
    w_list = np.array([2.016, 31.999, 28.01, 44.01, 18.01528, 28.05]) # [g/mol]
    R = 8.314  # J/mol K
    R_bar = R / w_list  # kJ/kg K = [J/mol K] / [g/mol]

    massfracs_r = [Y_h2_reac, Y_o2_reac, Y_n2_reac, 0, 0, 0]
    massfracs_p = [Y_h2_prod, Y_o2_prod, Y_n2_prod, 0, Y_h2o, 0]

    #print('C2H4 R bar = ', R_bar)

    #cp_h2 = cp_list[0]*R_bar[0]
    # cp_o2 = cp_list[1]*R_bar[1] # [kJ/kg K] = [-] * [kJ/kg K]
    # cp_n2 = cp_list[2]*R_bar[2] # [kJ/kg K] = [-] * [kJ/kg K]
    # cp_co2 = cp_list[3]*R_bar[3] # [kJ/kg K] = [-] * [kJ/kg K]
    # cp_h2o = cp_list[4]*R_bar[4] # [kJ/kg K] = [-] * [kJ/kg K]
    # cp_c2h4 = cp_list[5]*R_bar[5] # [kJ/kg K] = [-] * [kJ/kg K]


    # ===============INTEGRATION======================

    intR = 0
    intP = 0

    # ===============PRODUCTS======================
    # ====== integrate reactants: T0 -> 1000 ======
    # ===============PRODUCTS======================

    if Tr >= 1000:
        Tr_mid = 1000
        stop = False
    else:
        Tr_mid = Tr
        stop = True

    reac_ids = [0, 1, 2]
    acoefs_reac_lt = [0, 0, 0, 0, 0]

    for id in reac_ids:
        for i, coef in enumerate(coefs2[id,:5]):
            acoefs_reac_lt[i] += coef * massfracs_r[id] * R_bar[id]

    for i, supcoef_lt in enumerate(acoefs_reac_lt):
        intR += supcoef_lt / (i+1) * (Tr_mid ** (i+1) - T0 ** (i+1))

    # ====== integrate reactants: 1000 -> T1 ONLY IF Tr => 1000 ======
    if not stop:
        reac_ids = [0, 1, 2]
        acoefs_reac_ht = [0, 0, 0, 0, 0]

        for id in reac_ids:
            for i, coef in enumerate(coefs1[id, :5]):
                acoefs_reac_ht[i] += coef * massfracs_r[id] * R_bar[id]

        for i, supcoef_ht in enumerate(acoefs_reac_ht):
            intR += supcoef_ht / (i + 1) * (Tr ** (i + 1) - Tr_mid ** (i + 1))

    # ===============PRODUCTS======================
    # ====== integrate products: T0 -> 1000 =======
    # ===============PRODUCTS======================


    if Tad >= 1000:
        Tad_mid = 1000
        stop = False
    else:
        Tad_mid = Tad
        stop = True

    prod_ids = [0, 1, 2, 4]
    acoefs_prod_lt = [0, 0, 0, 0, 0]

    for id in prod_ids:
        for i, coef in enumerate(coefs2[id, :5]):
            acoefs_prod_lt[i] += coef * massfracs_p[id] * R_bar[id]

    for i, supcoef_lt in enumerate(acoefs_prod_lt):
        intP += supcoef_lt / (i + 1) * (Tad_mid ** (i + 1) - T0 ** (i + 1))

    # ====== integrate products: 1000 -> T1 ONLY IF Tad => 1000 ======
    if not stop:
        prod_ids = [0, 1, 2, 4]
        acoefs_prod_ht = [0, 0, 0, 0, 0]

        for id in prod_ids:
            for i, coef in enumerate(coefs1[id, :5]):
                acoefs_prod_ht[i] += coef * massfracs_p[id] * R_bar[id]

        for i, supcoef_ht in enumerate(acoefs_prod_ht):
            intP += supcoef_ht / (i + 1) * (Tad ** (i + 1) - Tad_mid ** (i + 1))

    return intP, intR




