def get_cp(coef1, coef2, temp):

    T_low = 200
    T_mid = 1000
    T_high = 3500

    if temp < T_low or temp > T_high:
        raise Exception('Temperature out of range')

    elif temp < T_mid:
        coef = coef2

    else:
        coef = coef1

    cp_bar_Ru = 0
    for i in range(5):
        cp_bar_Ru += temp ** i * coef[i]

    return cp_bar_Ru
