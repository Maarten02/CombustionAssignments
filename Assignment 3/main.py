import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from bin.read_sma import read_sma
from bin.get_A import get_A
from bin.plotting import plot_A_vs_fblrg, plot_layout_2bi, plot_2bii

# Raman Data: C:\Users\maart\OneDrive\Documents\MSc\Combustion\H3_Data\Raman Data H3 |FORMAT| HXXYYYYY.sma XX = x/d, r/D = YYY.YY
# Laser Doppler: C:\Users\maart\OneDrive\Documents\MSc\Combustion |FORMAT|

# ==========================================================================================================
# ======================================= Part 2Bi =========================================================
# ==========================================================================================================
# Consider the sets of single shot data along the radial coordinate at �/� = 2.5. Prepare a scatter plot
# of the DD parameter A as function of FBLGR and find the mixture fraction range where the DD
# effects appear. Is it at lean, stoichiometric or rich conditions?
# Hint: It is sufficient to consider the locations for which the mean temperature is higher than 600K,
# these are the locations with � = 4.5 mm, 5.25 mm, 6 mm, 6.75 mm, 7.5 mm and 8.25 mm. Prepare
# one plot with the data from all these files, giving a different color to the points of each of the
# datasets.
# So: x/d = 2.5, take 4.5 mm, 5.25 mm, 6 mm, 6.75 mm, 7.5 mm and 8.25 mm files, plot A as function of FBLGR
#
# Z^(i) = (Z_i - Z_i,2) / (Z_i,1 - Z_i,2)
# Z_i same as in part a ii
# Z_i,1 is the mass fraction of i in fuel stream ?
# Z_i,2_is the mass fraction of i in oxidiser stream ?
#
# A = Z^(H) – Z^(O) and
# B = Z^(H) – Z^(N)
W_H2 =
X_H2_1 =
X_H2_2 =

W_O2 =
X_O2_1 =
X_O2_2 =

W_N2 =
X_N2_1 =
X_N2_2 =

W_fuel =
W_air =

Z_H2_1 =
Z_O2_1 =
Z_N2_1 =

Z_H2_2 =
Z_O2_2 =
Z_N2_2 =

    plot_layout_2bi(fig, ax, x)

make_scatter_plot(r_arr, x)
# ==========================================================================================================
# ======================================= Part 2Bii =========================================================
# ==========================================================================================================
# For further analysis, continue with the datasets found relevant for DD in Part i). Divide the relevant
# FBLGR range in a number of bins (e.g. 10). In each bin compute the mean value of the DD
# parameter A. This quantity is called the “conditional mean”. Now plot the conditional mean as
# function of FBLGR mixture fraction. What do the obtained curves indicate in terms of DD?

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


    bins = np.linspace(0, 1, 10)
    plot_2bii(data_with_A, bins, x)

make_mean_plot(r_arr, x)

# ==========================================================================================================
# ======================================= Part 2Biii =========================================================
# ==========================================================================================================
# Now repeat what done in parts i) and ii) for �/� = 20. Is it true that the DD effect is much smaller
# at this axial location? How much smaller?
x_20 = 20
r_arr_20 = [0, 1.5, 3, 4.5, 6, 7.5, 9, 10.5, 12, 13.5, 15, 16.5, 18, 19.5, 21, 22.5, 24]

make_scatter_plot(r_arr_20, x_20)
make_mean_plot(r_arr_20, x_20)


# ==========================================================================
# ================================== OLD ===================================
# ==========================================================================
# data = read_sma(x, r)
# A_arr = np.empty(len(data))
# BFLGR = data['Z']
# for i, row in zip(range(len(data), data):
#     A_arr[i] = get_A(row)
#
# fig, ax = plt.subplots
#
# plot(BFLGR, A_arr)



