import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from bin.read_sma import read_sma
from bin.get_A import get_A
from bin.plotting import plot_A_vs_fblrg, plot_layout_2bi, plot_2bii, plot_2c


# TODO - PART 1:
# [ ] add reasoning for item 5
# [ ] elaborate item 3

# TODO - PART 2:
# [ ] read the 2Ai paper and write down explanation
# [ ] do part 2Di --> draw line, maybe consult literature
# [ ] do part 2Dii --> find explanation why flamelet SDR is much higher




# ==========================================================================================================
# ======================================= Part 2Bi =========================================================
# ==========================================================================================================

x = 2.5
r_arr = [4.5, 5.25, 6, 6.75, 7.5, 8.25]

def make_scatter_plot(r_arr, x, short=False, N=20):
    fig, ax = plt.subplots()
    for r in r_arr:

        data = read_sma(x, r)
        data_with_A = get_A(data)
        fig, ax = plot_A_vs_fblrg(fig, ax, data_with_A, r, short, N)

    plot_layout_2bi(fig, ax, x)

make_scatter_plot(r_arr, x)


# ==========================================================================================================
# ======================================= Part 2Bii ========================================================
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
# ======================================= Part 2Biii ========================================================
# ===========================================================================================================

x_20 = 20
r_arr_20 = [0, 1.5, 3, 4.5, 6, 7.5, 9, 10.5, 12, 13.5, 15, 16.5, 18, 19.5, 21, 22.5, 24]

make_scatter_plot(r_arr_20, x_20, short=True, N=30)
make_mean_plot(r_arr_20, x_20)


# =========================================================================================================
# ======================================= Part 2C =========================================================
# =========================================================================================================

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

# # EQ 1.2  - INCOMPLETE
# \frac{\partial}{\partial t}\left(\bar{\rho} \tilde{v}_j\right)+\frac{\partial}{\partial x_i}\left(\bar{\rho} \tilde{v}_i \tilde{v}_j\right)=\left[-\frac{\partial \bar{p}}{\partial x_j}+\frac{\partial \bar{\tau}_{i j}}{\partial x_i}+\bar{\rho} g_j\right]+\frac{\partial}{\partial x_i}\left[\mu_t\left(\frac{\partial \tilde{v}_i}{\partial x_j}+\frac{\partial \tilde{v}_j}{\partial x_i}\right)-\frac{2}{3} \delta_{i j}\left(\bar{\rho} \tilde{k}+\mu_t \frac{\partial \tilde{v}_k}{\partial x_k}\right)\right]
#
# # EQ  1.3
# \begin{aligned}
# & \frac{\partial}{\partial t}(\bar{\rho} \tilde{k})+\frac{\partial}{\partial x_i}\left(\bar{\rho} \tilde{v}_i \tilde{k}\right)=\frac{\partial}{\partial x_i}\left(\mu+\frac{\mu_t}{\sigma_k}\right) \frac{\partial}{\partial x_i} \tilde{k}+P_k-\bar{\rho} \tilde{\varepsilon} \\
# & P_k=-\bar{\rho} \widetilde{v_i " v_j "} \frac{\partial \tilde{v}_i}{\partial x_j}=\left[\mu_t\left(\frac{\partial \tilde{v}_i}{\partial x_j}+\frac{\partial \tilde{v}_j}{\partial x_i}\right)-\frac{2}{3} \delta_{i j}\left(\bar{\rho} \tilde{k}+\mu_t \frac{\partial \tilde{v}_k}{\partial x_k}\right)\right] \frac{\partial \tilde{v}_i}{\partial x_j}
# \end{aligned}
#
# # EQ 1.4
#
# \frac{\partial}{\partial t}(\bar{\rho} \tilde{\varepsilon})+\frac{\partial}{\partial x_i}(\bar{\rho} \tilde{v} \tilde{\varepsilon} \tilde{\varepsilon})=\frac{\partial}{\partial x_i}\left(\mu+\frac{\mu_t}{\sigma_{\varepsilon}}\right) \frac{\partial}{\partial x_i} \tilde{\varepsilon}+\frac{\tilde{\varepsilon}}{\tilde{k}}\left(C_{\varepsilon_1} P_k-C_{\varepsilon_2} \bar{\rho} \tilde{\varepsilon}\right)
#
# # EQ 1.5
# \frac{\partial}{\partial t} \bar{\rho} \tilde{Z}+\frac{\partial}{\partial x_i}(\bar{\rho} \tilde{v} \tilde{Z})=\frac{\partial}{\partial x_i}\left(\bar{\rho} \bar{D}_{e f f} \frac{\partial}{\partial x_i} \tilde{Z}\right)
#
# # EQ 1.6
# \frac{\partial}{\partial t} \bar{\rho} \widetilde{Z^{\prime 2}}+\frac{\partial}{\partial x_i}\left(\bar{\rho} \tilde{v}_i \widetilde{Z^{\prime \prime 2}}\right)=\frac{\partial}{\partial x_i}\left(\bar{\rho} \bar{D}_{e f f} \frac{\partial}{\partial x_i} \widetilde{Z^{\prime 2}}\right)+2 \bar{\rho} \bar{D}_{e f f} \frac{\partial \tilde{Z}}{\partial x_i} \frac{\partial \tilde{Z}}{\partial x_i}-C_\phi \bar{\rho} \frac{\varepsilon}{k} \widetilde{Z^{\prime 2}}
#
# # EQ 1.7 - INCOMPLETE
# \frac{\partial}{\partial t} \bar{\rho} \tilde{Y}_c+\frac{\partial}{\partial x_i}\left(\bar{\rho} \tilde{v}_i \tilde{Y}_c\right)=\frac{\partial}{\partial x_i}\left(\bar{\rho} \bar{D}_{e f f, c} \frac{\partial}{\partial x_i} \tilde{Y}_c\right)+\bar{\rho} \tilde{S}_c
#
# # EQ 1.8
# \frac{\partial}{\partial t} \bar{\rho} \widetilde{Y_c^{\prime \prime 2}}+\frac{\partial}{\partial x_i}\left(\bar{\rho} \tilde{v}_i \widetilde{Y_c^{\prime \prime 2}}\right)=\frac{\partial}{\partial x_i}\left(\bar{\rho} \bar{D}_{e f f, c} \frac{\partial}{\partial x_i} \widetilde{Y_c^{\prime \prime 2}}\right)+2 \bar{\rho} \bar{D}_{e f f, c} \frac{\partial \tilde{Y}_c}{\partial x_i} \frac{\partial \tilde{Y}_c}{\partial x_i}-C_\phi \bar{\rho} \frac{\varepsilon}{k} \widetilde{Y_c^{\prime \prime 2}}+\bar{\rho}\left(\widetilde{S_c Y_c}-\widetilde{S_c} \widetilde{Y_c}\right)
#
# # EQ 1.9
# \bar{\rho}=\overline{\left(\frac{\bar{M}}{R T}\right)} p_{r e f}
#
# # EQ 1.10
# \tilde{Y}_k=\int_0^1 \int_0^1 Y_k^{f g m}(z, c) \tilde{P}_Z(z) \tilde{P}_c(c) d z d c