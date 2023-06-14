import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from bin.read_sma import read_sma
from bin.get_A import get_A
from bin.plotting import plot_A_vs_fblrg, plot_layout_2bi, plot_2bii, plot_2c

# ==========================================================================================================
# ======================================= Part 2Bi =========================================================
# ==========================================================================================================

x = 2.5
r_arr = [4.5, 5.25, 6, 6.75, 7.5, 8.25]

def make_scatter_plot(r_arr, x):
    fig, ax = plt.subplots()
    for r in r_arr:

        data = read_sma(x, r)
        data_with_A = get_A(data)
        fig, ax = plot_A_vs_fblrg(fig, ax, data_with_A, r)

    plot_layout_2bi(fig, ax, x)

make_scatter_plot(r_arr, x)


# ==========================================================================================================
# ======================================= Part 2Bii =========================================================
# ==========================================================================================================

def make_mean_plot(r_arr, x):

    first_iteration = True

    for r in r_arr:
        data = read_sma(x, r)
        new_data_with_A = get_A(data)

        if first_iteration:
            first_iteration = False
            data_with_A = new_data_with_A

        else:
            data_with_A = pd.concat([data_with_A, new_data_with_A], axis=0)


    bins = np.linspace(0, 1, 10) # TDOD: Decide till which FBLGR to go
    plot_2bii(data_with_A, bins, x)

make_mean_plot(r_arr, x)


# ===========================================================================================================
# ======================================= Part 2Biii =========================================================
# ===========================================================================================================

x_20 = 20
r_arr_20 = [0, 1.5, 3, 4.5, 6, 7.5, 9, 10.5, 12, 13.5, 15, 16.5, 18, 19.5, 21, 22.5, 24]

make_scatter_plot(r_arr_20, x_20)
make_mean_plot(r_arr_20, x_20)


# ===========================================================================================================
# ======================================= Part 2C =========================================================
# ===========================================================================================================

strains = np.linspace(100, 10000, 200)
z_ext = 0.31

def get_sdr(a, z):
    sdr = a / np.pi * np.exp(-2 * (erfinv(1 - 2*z)) ** 2)
    return sdr

sdr_arr = get_sdr(strains, z=z_ext)
plot_2c(strains, sdr_arr)

a_extinct = 9180 # [s^-1]

sdr_extinct = a_extinct / np.pi * np.exp(-2 * (erfinv(1-2*z_ext))**2)
t_chem = 1/a_extinct

print(f'Extinction Scalar Dissipation Rate = {sdr_extinct:.4f} [s^-1]')
#print(f'Inverse of critical strain rate = {1/a_extinct:.8f} [s]')
print(f'Chemical time scale = {t_chem:.8f} [s]')
