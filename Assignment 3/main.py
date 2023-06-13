import numpy as np
from bin.read_sma import read_sma

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

def get_Z_i(row, species):
    # species i in fuel stream (Z_i,1)


    # species i in oxidiser stream (Z_i,2)
    # oxidiser Air 21% X O2 + 79% X n2


    return row[]